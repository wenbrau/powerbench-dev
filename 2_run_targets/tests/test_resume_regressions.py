"""Offline regressions for bank identity and interrupted batch collection."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "2_run_targets"), str(ROOT / "common")]
# Imports parse CLI arguments and read a key; no real key or network is needed here.
with patch.dict(os.environ, {"OR_KEY": "offline-test"}), patch.object(
        sys, "argv", ["test", "--reasoning", "off", "--bank",
                      str(ROOT / "current/banks/dataset3_full_504.v6r2.jsonl"),
                      "--out", "/tmp/unused-resume-test.jsonl"]):
    import run_targets_pinned as runner
    import run_capability_probe as probe
import batch_client as bc

TARGET = "anthropic/claude-haiku-4.5"
USAGE = {"completion_tokens_details": {"reasoning_tokens": 0}, "cost": 0}
ROW = dict(id="test-1", pair_id="test", lang="en", mode="harmless_empowerment",
           domain="Rank", context="Work", scale="individual", standing="low",
           prompt="Synthetic test request.")


def cached_batch(directory, rows):
    led = bc.Ledger(str(directory / "run.batches.json"))
    requests = [{"custom_id": bc.custom_id(TARGET, r["id"]), "body": {}} for r in rows]
    entry = led.intent(TARGET, TARGET, "off", 1, requests, 16000)
    led.confirm(entry, "paid-batch", "completed")
    cache = str(directory / "run.batchresults")
    bc.cache_results(cache, "paid-batch", [
        {"custom_id": req["custom_id"], "response": {"status_code": 200, "body": {
            "choices": [{"message": {"content": "B"}, "finish_reason": "stop"}],
            "usage": USAGE, "provider": "Anthropic"}}} for req in requests])
    return led, cache


class ResumeTests(unittest.TestCase):
    def test_target_checkpoint_does_not_call_judge(self):
        with patch.object(runner, "judge", side_effect=AssertionError("Judge called before save")):
            row = runner.build_row(TARGET, ROW, "off", "Answer", USAGE, "Anthropic", 1,
                                   False, grade=False)
        self.assertEqual(row["response"], "Answer")
        self.assertTrue(row["reasoning_ok"])
        self.assertEqual(row["refuse"], -1)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        network = patch.object(bc, "_request", side_effect=AssertionError("Network prohibited"))
        network.start()
        self.addCleanup(network.stop)

    def test_bank_extension_rejects_system_and_condition_changes(self):
        old = self.directory / "old.jsonl"
        new = self.directory / "new.jsonl"
        original = {**ROW, "system_prompt": "<user_context>USA</user_context>",
                    "condition": "us_cn", "user_nationality": "American"}
        old.write_text(json.dumps(original) + "\n")
        for change in [{"system_prompt": "<user_context>China</user_context>"},
                       {"condition": "cn_us"}, {"user_nationality": "Chinese"}]:
            with self.subTest(change=change):
                new.write_text(json.dumps({**original, **change}) + "\n")
                with patch.multiple(runner, BANK=str(new), ARM="off", BATCH=False):
                    with self.assertRaises(SystemExit):
                        runner._validate_meta({"bank": str(old), "transport": "sync"})

    def test_fallback_timeout_stays_pending_until_reconciled(self):
        for match in [None, {"id": "accepted-after-timeout", "status": "validating"}]:
            with self.subTest(match=match):
                led = bc.Ledger(str(self.directory / ("found.json" if match else "unknown.json")))
                reqs = runner.batch_requests(TARGET, [ROW], "off", 16000)
                with patch.object(runner, "_provider_block_accepted", {}), \
                     patch.object(bc, "submit", side_effect=[bc.SubmitRejected("provider"),
                                                            bc.AmbiguousSubmit("timeout")]), \
                     patch.object(bc, "reconcile", return_value=match):
                    try:
                        runner.submit_chunk(led, TARGET, "off", 1, reqs, 16000)
                    except (SystemExit, bc.AmbiguousSubmit):
                        pass
                pending = bc.Ledger(led.path).outstanding()
                self.assertEqual(len(pending), 1)
                self.assertEqual(pending[0]["batch_id"], match["id"] if match else None)

    def test_target_resume_does_not_rebuy_harvested_rows(self):
        led, cache = cached_batch(self.directory, [ROW])
        written = []
        with patch.multiple(runner, BATCH_LEDGER=led.path, BATCH_CACHE=cache), \
             patch.object(runner, "judge", return_value=(0, 0, 0, {})), \
             patch.object(bc, "submit", side_effect=AssertionError("Recovered row was repurchased")):
            runner.run_batched([TARGET], {TARGET: "off"}, {ROW["id"]: ROW},
                               [(TARGET, ROW)], written.append, skip=set())
        self.assertEqual([r["id"] for r in written], ["test-1"])
        self.assertFalse(bc.Ledger(led.path).outstanding())

    def test_probe_resume_skips_written_rows_and_does_not_rebuy_recovered_rows(self):
        first = dict(id="test-1", prompt="Synthetic question", source="gpqa_diamond",
                     subject="physics", n_options=4, answer="B", options=["a", "b", "c", "d"])
        second = {**first, "id": "test-2"}
        bank = self.directory / "bank.jsonl"
        bank.write_text("".join(json.dumps(r) + "\n" for r in [first, second]))
        led, _ = cached_batch(self.directory, [first, second])
        out = self.directory / "run.jsonl"
        saved = probe.row_from(TARGET, first, "off", "B", USAGE, "Anthropic", 1, False)
        out.write_text(json.dumps(saved) + "\n")
        done = {(TARGET, first["id"]): saved}
        with patch.multiple(probe, BANK=str(bank), OUT=str(out), TARGETS=[TARGET], ONLY=None,
                            ARM="off", BATCH=True, DRY=False, REPARSE=False, LIMIT=None,
                            NO_PROGRESS=True), \
             patch.object(probe, "load_done", return_value=done), \
             patch.object(probe, "batch_approved", return_value={TARGET}), \
             patch.object(probe, "confirm_plan"), \
             patch.object(bc, "check_batch_endpoint", return_value={"ok": True, "reason": "offline"}), \
             patch.object(bc, "submit", side_effect=AssertionError("Recovered row was repurchased")):
            probe.main()
        self.assertEqual([json.loads(l)["id"] for l in out.read_text().splitlines()],
                         ["test-1", "test-2"])
        self.assertFalse(bc.Ledger(led.path).outstanding())


if __name__ == "__main__":
    unittest.main()
