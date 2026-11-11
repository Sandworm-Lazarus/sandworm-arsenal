"""Regression checks for provenance drift and editorial status claims."""

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "arsenal.py"
SPEC = importlib.util.spec_from_file_location("arsenal", SCRIPT)
arsenal = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(arsenal)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(arsenal.read_catalog())

    def test_moving_link_is_rejected(self):
        entry = self.data["skills"][0]
        entry["url"] = entry["url"].replace(entry["commit"], "main")
        self.assertTrue(any("Pinned URL mismatch" in e for e in arsenal.validate_catalog(self.data)))

    def test_duplicate_origin_is_rejected(self):
        entry = copy.deepcopy(self.data["skills"][0])
        entry["id"] = 999
        self.data["skills"].append(entry)
        self.assertTrue(any("Duplicate entry path" in e for e in arsenal.validate_catalog(self.data)))

    def test_unsupported_execution_claim_is_rejected(self):
        self.data["skills"][0]["runtime_tested"] = True
        self.assertTrue(any("source-reviewed, untested" in e for e in arsenal.validate_catalog(self.data)))

    def test_search_supports_casefold_and_thai_category_filter(self):
        self.assertEqual(arsenal.search(self.data, "MEMORY"), arsenal.search(self.data, "memory"))
        results = arsenal.search(self.data, "สิทธิ์", "AI Security")
        self.assertTrue(results)
        self.assertTrue(all(e["category"] == "AI Security" for e in results))

    def test_missing_and_escaping_local_links_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[missing](absent.md) [outside](../outside.md)", encoding="utf-8")
            self.assertEqual(len(arsenal.local_link_errors(root)), 2)


if __name__ == "__main__":
    unittest.main()
