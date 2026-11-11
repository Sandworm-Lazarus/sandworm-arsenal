"""Keep published privacy evidence reproducible and honest about failures."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "check_privacy_fixtures.py"


class PrivacyEvidenceTests(unittest.TestCase):
    def run_report(self, *args):
        return subprocess.run([sys.executable, str(RUNNER), *map(str, args)],
                              capture_output=True, text=True, encoding="utf-8", timeout=10)

    def test_committed_evidence_matches_fresh_execution(self):
        result = self.run_report("--check-report", ROOT / "examples/privacy-guard-results.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_tampered_report_fails_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            fresh = self.run_report()
            self.assertEqual(fresh.returncode, 0, fresh.stderr)
            data = json.loads(fresh.stdout)
            data["source_sha256"]["guard"] = "0" * 64
            path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            checked = self.run_report("--check-report", path)
            self.assertEqual(checked.returncode, 1)
            self.assertEqual(checked.stdout, "")

    def test_failed_expectation_cannot_produce_a_passing_claim_or_payload_leak(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixtures.json"
            raw = "synthetic-person@example.invalid"
            path.write_text(json.dumps({"cases": [{"id": "expected-failure", "mode": "text",
                "input": raw, "expected_output": raw}]}), encoding="utf-8")
            checked = self.run_report("--fixtures", path)
            self.assertEqual(checked.returncode, 1)
            data = json.loads(checked.stdout)
            self.assertFalse(data["all_passed"])
            self.assertEqual(data["cases_passed"], 0)
            self.assertNotIn(raw, checked.stdout + checked.stderr)

    def test_invalid_fixture_contract_fails_without_echoing_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixtures.json"
            sentinel = "synthetic-private-payload-do-not-echo"
            path.write_text(json.dumps({"cases": [{"id": "invalid-contract", "mode": "text",
                "input": sentinel, "sensitive_fields": sentinel}]}), encoding="utf-8")
            checked = self.run_report("--fixtures", path)
            self.assertEqual(checked.returncode, 2)
            self.assertEqual(checked.stdout, "")
            self.assertNotIn(sentinel, checked.stderr)


if __name__ == "__main__":
    unittest.main()
