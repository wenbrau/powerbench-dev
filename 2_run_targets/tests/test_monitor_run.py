"""The monitor must count saved results without changing or exposing transcripts."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "monitor_run", Path(__file__).resolve().parents[1] / "monitor_run.py")
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


class MonitorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.out = self.root / "run.jsonl"
        self.process = self.root / "process.json"
        self.process.write_text(json.dumps({"models": ["vendor/a", "vendor/b"],
                                            "status": "running", "pid": 42, "started": 100}))
        self.reader = monitor.RunMonitor(self.out, self.process, expected=2,
                                         alive=lambda _: True)

    def row(self, id="1", **changes):
        return {"target": "vendor/a", "id": id, "empty": False,
                "reasoning_ok": True, "refuse": 0, "harmful": 0,
                "judge_reasoning_ok": True, "judge_error": None,
                "response": "PRIVATE TRANSCRIPT", "usage": {"cost": .01}, **changes}

    def append(self, row):
        with self.out.open("a") as f:
            f.write(json.dumps(row) + "\n")

    def test_partial_line_is_not_lost_or_counted_early(self):
        raw = json.dumps(self.row())
        self.out.write_text(raw[:40])
        self.assertEqual(self.reader.snapshot(now=200)["done"], 0)
        with self.out.open("a") as f:
            f.write(raw[40:] + "\n")
        state = self.reader.snapshot(now=210)
        self.assertEqual(state["done"], 1)
        self.assertNotIn("PRIVATE TRANSCRIPT", json.dumps(state))
        self.assertEqual(self.reader.snapshot(now=211)["done"], 1)

    def test_duplicates_do_not_inflate_progress_and_quality_is_separate(self):
        self.append(self.row())
        self.append(self.row())
        self.append(self.row("2", judge_error="failed", refuse=-1))
        state = self.reader.snapshot(now=200)
        self.assertEqual((state["done"], state["checked"], state["issues"]), (2, 1, 1))
        self.assertEqual(state["duplicates"], 1)
        self.assertEqual(state["models"][1]["done"], 0)

    def test_stopped_process_is_not_reported_as_running_or_complete(self):
        self.append(self.row())
        self.reader.alive = lambda _: False
        self.assertEqual(self.reader.snapshot(now=200)["phase"], "stopped")
        self.process.write_text(json.dumps({"models": ["vendor/a", "vendor/b"],
                                            "status": "exited", "exit_code": 0}))
        self.assertEqual(self.reader.snapshot(now=210)["phase"], "incomplete")

    def test_rotation_replaces_counts_and_malformed_rows_are_visible(self):
        self.append(self.row())
        self.reader.snapshot(now=200)
        self.out.unlink()
        self.out.write_text("not json\n")
        state = self.reader.snapshot(now=210)
        self.assertEqual(state["done"], 0)
        self.assertEqual(state["malformed"], 1)

    def test_complete_with_issues_is_distinct_from_clean_completion(self):
        for target in ("vendor/a", "vendor/b"):
            for id in ("1", "2"):
                self.append(self.row(id, target=target))
        self.assertEqual(self.reader.snapshot(now=200)["phase"], "complete")
        self.append(self.row("1", empty=True, target="vendor/a"))
        self.assertEqual(self.reader.snapshot(now=210)["phase"], "review")

    def test_rate_uses_observed_changes_not_old_rows_as_new_work(self):
        self.append(self.row())
        self.assertIsNone(self.reader.snapshot(now=200)["eta_seconds"])
        self.append(self.row("2"))
        state = self.reader.snapshot(now=260)
        self.assertEqual(state["rate_per_minute"], 1)
        self.assertEqual(state["eta_seconds"], 120)

    def test_recovery_status_is_separate_and_detects_a_stopped_process(self):
        self.out.with_suffix(".recovery.status.json").write_text(json.dumps({
            "status": "running", "pid": 84, "total": 3, "recovered": 1,
            "remaining": 2, "target_remaining": 1, "secret": "DO NOT SERVE"}))
        state = self.reader.snapshot(now=200)
        self.assertEqual(state["recovery"]["recovered"], 1)
        self.assertEqual(state["recovery"]["status"], "running")
        self.assertNotIn("DO NOT SERVE", json.dumps(state))
        self.reader.alive = lambda _: False
        self.assertEqual(self.reader.snapshot(now=210)["recovery"]["status"], "stopped")


if __name__ == "__main__":
    unittest.main()
