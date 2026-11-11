"""Boundary and false-positive regression cases for the original detector."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/detection_lab.py"
SPEC = importlib.util.spec_from_file_location("detection_lab", SCRIPT)
detector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(detector)


def event(number, second, actor="a", action="object_access", outcome="denied", detail="object-1"):
    record = {
        "event_id": str(number), "timestamp": f"2026-11-11T10:{second // 60:02}:{second % 60:02}Z",
        "actor": actor, "action": action, "outcome": outcome,
    }
    record["object_id" if action == "object_access" else "request_id"] = detail
    return record


def document(events):
    return {"schema_version": 1, "events": events}


class DetectionTests(unittest.TestCase):
    def test_committed_expected_alerts_match_new_calculation(self):
        data = json.loads((ROOT / "examples/events.json").read_text(encoding="utf-8"))
        expected = json.loads((ROOT / "examples/expected-alerts.json").read_text(encoding="utf-8"))
        self.assertEqual(detector.detect(data)["alerts"], expected)
        self.assertEqual(detector.detect(data), detector.detect(data))

    def test_window_includes_exact_boundary_and_excludes_one_second_outside(self):
        self.assertEqual(len(detector.detect(document([event(1, 0), event(2, 30), event(3, 60)]))["alerts"]), 1)
        self.assertEqual(detector.detect(document([event(1, 0), event(2, 30), event(3, 61)]))["alerts"], [])

    def test_legitimate_lookalikes_and_group_boundaries(self):
        cases = [event(1, 0), event(2, 5, outcome="allowed"), event(3, 10, actor="b"), event(4, 20)]
        self.assertEqual(detector.detect(document(cases))["alerts"], [])
        replay = [event(n, n, action="replay_check", detail=f"request-{n}") for n in range(3)]
        self.assertEqual(detector.detect(document(replay))["alerts"], [])
        replay[2]["request_id"] = replay[1]["request_id"] = replay[0]["request_id"]
        self.assertEqual(detector.detect(document(replay))["alerts"][0]["rule"], "rejected_replay_burst")

    def test_continuous_burst_is_suppressed_then_rearms(self):
        cases = [event(n, second) for n, second in enumerate([0, 10, 20, 30, 100, 110, 120])]
        alerts = detector.detect(document(cases))["alerts"]
        self.assertEqual([a["event_ids"] for a in alerts], [["0", "1", "2"], ["4", "5", "6"]])

    def test_missing_data_duplicate_ids_bad_dates_and_order_are_rejected(self):
        missing = json.loads((ROOT / "examples/missing-data.json").read_text(encoding="utf-8"))
        with self.assertRaisesRegex(detector.DetectionError, "missing object_id"):
            detector.detect(missing)
        for broken in (
            document([event(1, 2), event(2, 1)]), document([event(1, 1), event(1, 2)]),
            document([dict(event(1, 1), timestamp="2026-02-30T10:00:00Z")]),
            document([dict(event(1, 1), timestamp="2026-11-11T10:00:00+00:00")]),
            document([dict(event(1, 1), action="unexpected")]),
        ):
            with self.subTest(data=broken), self.assertRaises(detector.DetectionError):
                detector.detect(broken)

    def test_empty_input_and_invalid_configuration(self):
        self.assertEqual(detector.detect(document([]))["alerts"], [])
        with self.assertRaises(detector.DetectionError):
            detector.detect({"schema_version": True, "events": []})
        for kwargs in ({"threshold": 1}, {"threshold": True}, {"window_seconds": 0}):
            with self.assertRaises(detector.DetectionError):
                detector.detect(document([]), **kwargs)

    def test_cli_matches_fixture_and_reports_mismatch_or_invalid_input(self):
        base = [sys.executable, str(SCRIPT), "--input", str(ROOT / "examples/events.json")]
        good = subprocess.run(base + ["--expect", str(ROOT / "examples/expected-alerts.json")], capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertTrue(json.loads(good.stdout)["expectations_match"])
        with tempfile.TemporaryDirectory() as directory:
            expected = Path(directory) / "expected.json"
            expected.write_text("[]", encoding="utf-8")
            bad = subprocess.run(base + ["--expect", str(expected)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1)
            self.assertFalse(json.loads(bad.stdout)["expectations_match"])
        invalid = subprocess.run([sys.executable, str(SCRIPT), "--input", str(ROOT / "examples/missing-data.json")], capture_output=True, text=True)
        self.assertEqual(invalid.returncode, 2)
        self.assertNotIn("alerts", json.loads(invalid.stdout))


if __name__ == "__main__":
    unittest.main()
