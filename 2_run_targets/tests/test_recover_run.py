import importlib.util
import json
from pathlib import Path
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

spec = importlib.util.spec_from_file_location(
    "recover_run", Path(__file__).resolve().parents[1] / "recover_run.py")
recovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.row = {"target": "vendor/model", "id": "one", "response": "Existing answer",
                    "empty": False, "reasoning_ok": True, "reasoning_arm": "off",
                    "refuse": -1, "harmful": -1, "judge_error": "timeout", "usage": {"cost": 1}}
        self.info = {"judge_reasoning_ok": True, "judge_error": None}
        self.runner = SimpleNamespace(call=Mock(side_effect=AssertionError("Target repurchased")),
                                      judge=Mock(return_value=(0, 1, 0, self.info)))
        self.journal = []

    def recover(self, row):
        return recovery.recover_one(row, {"prompt": "Original request"}, self.runner,
                                    lambda stage, r: self.journal.append((stage, r)),
                                    threading.Semaphore(1), threading.Lock())

    def test_judge_only_preserves_paid_response_and_target_metadata(self):
        result = self.recover(self.row)
        self.assertTrue(recovery.clean(result))
        self.assertEqual(result["response"], self.row["response"])
        self.assertEqual(result["usage"], self.row["usage"])
        self.runner.call.assert_not_called()
        self.assertEqual([stage for stage, _ in self.journal], ["judge"])

    def test_valid_rows_make_no_calls(self):
        row = {**self.row, **self.info, "refuse": 0, "harmful": 1}
        self.assertIs(self.recover(row), row)
        self.runner.call.assert_not_called()
        self.runner.judge.assert_not_called()

    def test_target_saved_before_judge_failure_and_reused_on_resume(self):
        self.runner.call = Mock(return_value=("New answer", {}, "Vendor", False))
        self.runner.messages_for = Mock(return_value=[])
        checkpoint = {**self.row, "response": "New answer"}
        self.runner.build_row = Mock(return_value=checkpoint)
        self.runner.judge.side_effect = RuntimeError("process interrupted")
        with self.assertRaises(RuntimeError):
            self.recover({**self.row, "empty": True, "response": ""})
        self.assertEqual(self.journal, [("target", checkpoint)])
        self.assertFalse(self.runner.build_row.call_args.kwargs["grade"])
        self.runner.judge.side_effect = None
        self.assertTrue(recovery.clean(self.recover(checkpoint)))
        self.assertEqual(self.runner.call.call_count, 1)

    def test_merge_preserves_valid_rows_exactly_and_rejects_external_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            original = Path(folder) / "original.jsonl"
            source = Path(folder) / "run.jsonl"
            good = {**self.row, **self.info, "id": "two", "refuse": 0, "harmful": 1}
            good_bytes = (json.dumps(good, separators=(",", ":")) + "\n").encode()
            original.write_bytes((json.dumps(self.row) + "\n").encode() + good_bytes)
            source.write_bytes(original.read_bytes())
            latest = {recovery.key(self.row): self.recover(self.row), recovery.key(good): good}
            checksum = recovery.merge_repairs(source, original, latest, recovery.digest(source))
            self.assertTrue(source.read_bytes().endswith(good_bytes))
            self.assertTrue(all(recovery.clean(r) for r in recovery.read_rows(source).values()))
            source.write_bytes(source.read_bytes() + b"\n")
            with self.assertRaises(RuntimeError):
                recovery.merge_repairs(source, original, latest, checksum)

    def test_replay_recovers_target_and_discards_only_incomplete_final_line(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "events.jsonl"
            data = (json.dumps({"stage": "target", "row": self.row}) + "\n").encode()
            path.write_bytes(data + b'{"stage":')
            original = {recovery.key(self.row): {**self.row, "empty": True}}
            self.assertEqual(recovery.replay(path, original)[recovery.key(self.row)], self.row)
            self.assertEqual(path.read_bytes(), data)


if __name__ == "__main__":
    unittest.main()
