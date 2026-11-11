"""Regression checks for provenance drift and editorial status claims."""

import copy
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "arsenal.py"
SPEC = importlib.util.spec_from_file_location("arsenal", SCRIPT)
arsenal = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(arsenal)


def minimal_catalog():
    """Small synthetic schema fixture, independent of curated project choices."""
    commit, blob = "a" * 40, "b" * 40
    sources = []
    for repo, kind in (("example/skills", "skill-collection"), ("example/tool", "tool")):
        sources.append({"repo": repo, "url": f"https://github.com/{repo}",
                        "commit": commit, "license": "Synthetic license note",
                        "note": "Synthetic source", "kind": kind})
    skill_path = "skills/example/SKILL.md"
    evidence_path = "references/example.md"
    return {
        "schema_version": 2, "as_of": "2026-11-11", "snapshot": "synthetic-fixture",
        "sources": sources,
        "skills": [{"id": 1, "repo": "example/skills", "path": skill_path,
                    "commit": commit, "blob_sha": blob,
                    "url": f"https://github.com/example/skills/blob/{commit}/{skill_path}",
                    "name": "Example skill", "category": "Cyber", "purpose": "Example task",
                    "requires": "Example input", "note": "Synthetic entry", "tags": ["example"],
                    "review_level": "entry-overview", "read": False, "runtime_tested": False}],
        "evidence": [{"repo": "example/skills", "path": evidence_path, "blob_sha": blob,
                      "url": f"https://github.com/example/skills/blob/{commit}/{evidence_path}"}],
        "tools": [{"repo": "example/tool", "name": "Example tool", "group": "Example group",
                   "purpose": "Example task", "requires": "Example input", "note": "Synthetic tool",
                   "url": f"https://github.com/example/tool/tree/{commit}",
                   "review_level": "readme-overview", "runtime_tested": False}],
    }


class CatalogSchemaTests(unittest.TestCase):
    def assert_invalid(self, data, field):
        errors = arsenal.validate_catalog(data)
        self.assertTrue(errors)
        self.assertTrue(any(field in error for error in errors), errors)
        # Invalid metadata must stop check before it touches generated documents.
        self.assertEqual(arsenal.check(data), errors)

    def test_minimal_catalog_variants_support_all_consumers(self):
        for variant in ("combined", "skill-only", "tool-only"):
            with self.subTest(variant=variant):
                data = minimal_catalog()
                if variant == "skill-only":
                    data["tools"] = []
                    data["sources"] = data["sources"][:1]
                elif variant == "tool-only":
                    data["skills"] = []
                    data["evidence"] = []
                    data["sources"] = data["sources"][1:]
                self.assertEqual(arsenal.validate_catalog(data), [])
                self.assertEqual(len(arsenal.search(data, "example", repo="EXAMPLE/SKILLS")), len(data["skills"]))
                self.assertEqual(len(arsenal.search_tools(data, "example", group="EXAMPLE GROUP")), len(data["tools"]))
                self.assertEqual(len(arsenal.rendered_files(data)), 4)
                self.assertEqual(arsenal.stats(data)["Skill entries"], len(data["skills"]))

    def test_catalog_root_must_be_an_object(self):
        for value in (None, [], "catalog", 2, True):
            with self.subTest(value=value):
                self.assert_invalid(value, "Catalog must be an object")

    def test_required_root_metadata_is_checked(self):
        for field in ("schema_version", "as_of", "snapshot"):
            for value in (None, [], {}, 0, True, "", " "):
                with self.subTest(field=field, value=value):
                    data = minimal_catalog()
                    data[field] = value
                    self.assert_invalid(data, field)
            with self.subTest(field=field, missing=True):
                data = minimal_catalog()
                del data[field]
                self.assert_invalid(data, field)
        for field, value in (("schema_version", 2.0), ("as_of", "2026-02-30")):
            with self.subTest(field=field, value=value):
                data = minimal_catalog()
                data[field] = value
                self.assert_invalid(data, field)

    def test_required_arrays_cannot_be_omitted_or_retyped(self):
        for field in ("sources", "skills", "evidence", "tools"):
            for value in (None, {}, "array", 1, False):
                with self.subTest(field=field, value=value):
                    data = minimal_catalog()
                    data[field] = value
                    self.assert_invalid(data, field)
            with self.subTest(field=field, missing=True):
                data = minimal_catalog()
                del data[field]
                self.assert_invalid(data, field)

    def test_array_records_must_be_objects(self):
        for field in ("sources", "skills", "evidence", "tools"):
            for value in (None, [], "record", 1, False):
                with self.subTest(field=field, value=value):
                    data = minimal_catalog()
                    data[field][0] = value
                    self.assert_invalid(data, f"{field}[0]")

    def test_required_record_text_is_checked_before_consumers(self):
        fields = {
            "sources": ("repo", "url", "commit", "license", "note", "kind"),
            "skills": ("repo", "path", "commit", "blob_sha", "url", "name", "purpose",
                       "requires", "note", "category", "review_level"),
            "evidence": ("repo", "path", "url", "blob_sha"),
            "tools": ("repo", "name", "group", "purpose", "requires", "note", "url", "review_level"),
        }
        for collection, required in fields.items():
            for field in required:
                for value in (None, [], {}, 1, 1.5, True, "", " "):
                    with self.subTest(collection=collection, field=field, value=value):
                        data = minimal_catalog()
                        data[collection][0][field] = value
                        self.assert_invalid(data, f"{collection}[0].{field}")
                with self.subTest(collection=collection, field=field, missing=True):
                    data = minimal_catalog()
                    del data[collection][0][field]
                    self.assert_invalid(data, f"{collection}[0].{field}")

    def test_entry_ids_must_be_positive_integers(self):
        for value in (None, True, 1.0, "1", 0, -1, [], {}):
            with self.subTest(value=value):
                data = minimal_catalog()
                data["skills"][0]["id"] = value
                self.assert_invalid(data, "ID")

    def test_tags_must_contain_nonempty_strings(self):
        for value in (None, {}, "example", [], [None], [{}], [""], [" "]):
            with self.subTest(value=value):
                data = minimal_catalog()
                data["skills"][0]["tags"] = value
                self.assert_invalid(data, "tags")

    def test_optional_provenance_types_are_checked(self):
        for field in ("license_url", "readme_url", "license_blob_sha", "readme_blob_sha"):
            for value in ([], {}, 1, True, "", " "):
                with self.subTest(field=field, value=value):
                    data = minimal_catalog()
                    data["sources"][0][field] = value
                    self.assert_invalid(data, field)
        for collection in ("sources", "skills", "evidence", "tools"):
            for value in (None, [], {}, 1, "2026-02-30"):
                with self.subTest(collection=collection, reviewed_at=value):
                    data = minimal_catalog()
                    data[collection][0]["reviewed_at"] = value
                    self.assert_invalid(data, "reviewed_at")
        data = minimal_catalog()
        for field in ("license_url", "readme_url", "license_blob_sha", "readme_blob_sha"):
            data["sources"][0][field] = None
        self.assertEqual(arsenal.validate_catalog(data), [])

    def test_execution_and_read_flags_require_exact_booleans(self):
        for collection, field in (("skills", "read"), ("skills", "runtime_tested"), ("tools", "runtime_tested")):
            for value in (None, 0, "false", [], {}):
                with self.subTest(collection=collection, field=field, value=value):
                    data = minimal_catalog()
                    data[collection][0][field] = value
                    self.assertTrue(arsenal.validate_catalog(data))

    def test_evidence_paths_cannot_escape_the_repository(self):
        for path in ("/outside.md", "../outside.md", "references/../../outside.md"):
            with self.subTest(path=path):
                data = minimal_catalog()
                evidence = data["evidence"][0]
                evidence["path"] = path
                evidence["url"] = f"https://github.com/example/skills/blob/{data['sources'][0]['commit']}/{path}"
                self.assert_invalid(data, "evidence path")

    def test_cli_rejects_observed_bad_catalogs_before_any_command(self):
        fixtures = []
        data = minimal_catalog()
        data["tools"][0]["purpose"] = ["not", "text"]
        fixtures.append(data)
        data = minimal_catalog()
        del data["sources"][0]["note"]
        fixtures.append(data)
        data = minimal_catalog()
        del data["evidence"]
        fixtures.append(data)
        for index, data in enumerate(fixtures):
            for command in (["search", ""], ["tools"], ["show", "1"], ["stats"], ["check"], ["render"]):
                with self.subTest(fixture=index, command=command):
                    stderr = io.StringIO()
                    with mock.patch.object(arsenal, "read_catalog", return_value=data), \
                            mock.patch.object(sys, "argv", [str(SCRIPT), *command]), \
                            contextlib.redirect_stderr(stderr):
                        self.assertEqual(arsenal.main(), 1)
                    self.assertTrue(stderr.getvalue())
                    self.assertNotIn("Traceback", stderr.getvalue())


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(arsenal.read_catalog())

    def test_tool_only_collection_is_supported(self):
        self.data["skills"] = []
        self.data["evidence"] = []
        self.data["sources"] = [s for s in self.data["sources"] if s["kind"] == "tool"]
        self.assertEqual(arsenal.validate_catalog(self.data), [])

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

    def test_overview_cannot_claim_complete_entry_read(self):
        entry = next(e for e in self.data["skills"] if e["review_level"] == "entry-overview")
        entry["read"] = True
        self.assertTrue(any("matching scope" in e for e in arsenal.validate_catalog(self.data)))

    def test_tool_register_rejects_revision_drift(self):
        self.data["tools"][0]["url"] = "https://github.com/example/tool/tree/main"
        self.assertTrue(any("Tool revision mismatch" in e for e in arsenal.validate_catalog(self.data)))

    def test_cli_emits_json_and_honors_repository_filter(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "search", "", "--repo", "cloudflare/skills", "--json"], capture_output=True, text=True, check=True)
        entries = json.loads(result.stdout)
        self.assertTrue(entries)
        self.assertTrue(all(e["repo"] == "cloudflare/skills" for e in entries))

    def test_cli_unknown_id_is_an_error(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "show", "-1"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("No entry", result.stderr)

    def test_tool_search_filters_group_and_handles_thai(self):
        result = arsenal.search_tools(self.data, "เสียง", "voice & audio")
        self.assertTrue(result)
        self.assertTrue(all(t["group"] == "Voice & audio" for t in result))

    def test_tools_cli_json_and_unknown_group(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "tools", "", "--group", "Personal agents", "--json"], capture_output=True, text=True, check=True)
        self.assertEqual({t["repo"] for t in json.loads(result.stdout)}, {"NousResearch/hermes-agent", "letta-ai/letta-code"})
        bad = subprocess.run([sys.executable, str(SCRIPT), "tools", "--group", "does-not-exist"], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)

    def test_missing_and_escaping_local_links_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[missing](absent.md) [outside](../outside.md)", encoding="utf-8")
            self.assertEqual(len(arsenal.local_link_errors(root)), 2)

    def test_malformed_link_targets_return_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[bad URL](https://[) [bad file](%00.md)", encoding="utf-8")
            self.assertEqual(len(arsenal.local_link_errors(root)), 2)


if __name__ == "__main__":
    unittest.main()
