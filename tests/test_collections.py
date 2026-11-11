"""Exercise focused generation from a future snapshot in disposable directories."""

import collections
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HUB = Path(__file__).resolve().parents[1]
FUTURE_DATE = "2031-04-06"
FUTURE_SNAPSHOT = FUTURE_DATE + "-generation-regression"
COLLECTION_CATEGORIES = {
    "sandworm-ai-toolbox": (),
    "sandworm-agent-skills": ("Agent / Context",),
    "sandworm-cyber-arsenal": ("Cyber", "AI Security", "Reverse / DFIR"),
    "sandworm-llm-lab": ("AI Engineering",),
    "sandworm-dev-playbooks": ("Engineering", "Cloud / DevOps", "Web / Frontend"),
}
TOOL_GROUPS = {
    "sandworm-ai-toolbox": {
        "Personal agents", "Agent frameworks", "Visual workflows", "Local inference",
        "Chat workspaces", "Agent memory", "Browser automation", "Document ingestion",
        "RAG & vector search", "Voice & audio", "Image workflows", "Coding agents",
        "Training & fine-tuning", "Observability", "Model gateways", "MCP development",
        "AI application SDKs", "Privacy & data handling",
    },
    "sandworm-agent-skills": {
        "Personal agents", "Agent frameworks", "Agent memory", "Browser automation",
        "Voice & audio", "MCP development", "AI application SDKs",
    },
    "sandworm-cyber-arsenal": {
        "Skill review", "Secrets", "Containers / IaC", "Supply chain", "CI security",
        "Code analysis", "MCP development", "Privacy & data handling",
    },
    "sandworm-llm-lab": {
        "Local inference", "RAG & vector search", "Training & fine-tuning",
        "Observability", "Model gateways", "AI application SDKs",
    },
    "sandworm-dev-playbooks": {
        "Visual workflows", "Chat workspaces", "Document ingestion", "Image workflows",
        "Coding agents", "API testing", "AI application SDKs",
    },
}
EXTRA_TOOLS = {
    "sandworm-ai-toolbox": {"confident-ai/deepeval", "vibrantlabsai/ragas"},
    "sandworm-cyber-arsenal": {
        "NVIDIA/SkillEvaluator", "microsoft/PyRIT", "NVIDIA/garak", "promptfoo/promptfoo",
        "UKGovernmentBEIS/inspect_ai",
    },
    "sandworm-llm-lab": {"confident-ai/deepeval", "vibrantlabsai/ragas"},
}
PRIVACY_COLLECTIONS = {"sandworm-cyber-arsenal", "sandworm-dev-playbooks"}
PRIVACY_FILES = (
    "scripts/privacy_guard.py", "tests/test_privacy_guard.py", "docs/privacy-guard.md",
    "examples/privacy-fixtures.json",
)
REPORT_FILES = ("scripts/check_privacy_fixtures.py", "examples/privacy-guard-results.json")
CHECKOUT = "actions/checkout@11d5960a326750d5838078e36cf38b85af677262"


def generate(hub, output):
    return subprocess.run(
        [sys.executable, str(hub / "scripts/build_collections.py"), "--output-root", str(output)],
        capture_output=True, text=True, encoding="utf-8", timeout=60,
    )


def repository_bytes(root):
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*") if path.is_file()}


class CollectionGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.hub = cls.root / "hub"
        cls.hub.mkdir()
        for filename in ("scripts/build_collections.py", "scripts/arsenal.py", "LICENSE", ".gitignore"):
            destination = cls.hub / filename
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HUB / filename, destination)
        for folder in ("playbooks", "templates"):
            shutil.copytree(HUB / folder, cls.hub / folder)
        cls.data = json.loads((HUB / "catalog/arsenal.json").read_text(encoding="utf-8"))
        cls.data["as_of"] = FUTURE_DATE
        cls.data["snapshot"] = FUTURE_SNAPSHOT
        (cls.hub / "catalog").mkdir()
        (cls.hub / "catalog/arsenal.json").write_text(
            json.dumps(cls.data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        # Deliberately tiny fixtures isolate packaging from privacy-filter behavior.
        fixture_files = {
            "scripts/privacy_guard.py": '"""Synthetic packaging fixture."""\n',
            "tests/test_privacy_guard.py": '"""Synthetic packaging test fixture."""\n',
            "docs/privacy-guard.md": "# Synthetic packaging documentation\n",
            "scripts/check_privacy_fixtures.py": '"""Synthetic report-runner packaging fixture."""\n',
            "examples/privacy-guard-results.json": '{"packaging_fixture": true}\n',
        }
        for filename, content in fixture_files.items():
            path = cls.hub / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        shutil.copyfile(HUB / "examples/privacy-fixtures.json", cls.hub / "examples/privacy-fixtures.json")
        cls.outputs = [cls.root / "first", cls.root / "second"]
        for output in cls.outputs:
            result = generate(cls.hub, output)
            if result.returncode:
                raise AssertionError(f"Generator failed: {result.stdout}\n{result.stderr}")

    def test_future_snapshot_partition_and_exact_provenance_subsets(self):
        assigned = []
        for name, categories in COLLECTION_CATEGORIES.items():
            with self.subTest(collection=name):
                root = self.outputs[0] / name
                subset = json.loads((root / "catalog/arsenal.json").read_text(encoding="utf-8"))
                self.assertEqual(subset["as_of"], FUTURE_DATE)
                self.assertEqual(subset["snapshot"], FUTURE_SNAPSHOT + "-" + name)
                self.assertEqual(subset["collection"]["source_snapshot"], FUTURE_SNAPSHOT)
                self.assertEqual(subset["collection"]["name"], name)
                expected_skills = [s for s in self.data["skills"] if s["category"] in categories]
                expected_tools = [t for t in self.data["tools"]
                                  if t["group"] in TOOL_GROUPS[name]
                                  or t["repo"] in EXTRA_TOOLS.get(name, set())]
                self.assertEqual(subset["skills"], expected_skills)
                self.assertEqual(subset["tools"], expected_tools)
                repos = {s["repo"] for s in expected_skills} | {t["repo"] for t in expected_tools}
                for field in ("sources", "evidence"):
                    self.assertEqual(subset[field], [item for item in self.data[field] if item["repo"] in repos])
                assigned.extend(s["id"] for s in subset["skills"])
                check = subprocess.run(
                    [sys.executable, str(root / "scripts/arsenal.py"), "check"],
                    capture_output=True, text=True, encoding="utf-8", timeout=30,
                )
                self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual(collections.Counter(assigned), collections.Counter(s["id"] for s in self.data["skills"]))
        self.assertTrue(all(count == 1 for count in collections.Counter(assigned).values()))

    def test_deterministic_repositories_and_scoped_privacy_ci(self):
        for name in COLLECTION_CATEGORIES:
            with self.subTest(collection=name):
                first, second = (output / name for output in self.outputs)
                self.assertEqual(repository_bytes(first), repository_bytes(second))
                workflow = (first / ".github/workflows/validate.yml").read_text(encoding="utf-8")
                self.assertIn(CHECKOUT, workflow)
                self.assertIn("contents: read", workflow)
                self.assertIn("persist-credentials: false", workflow)
                self.assertIn("python3 scripts/arsenal.py check", workflow)
                readme = (first / "README.md").read_text(encoding="utf-8")
                for filename in PRIVACY_FILES[:3] + REPORT_FILES:
                    if name in PRIVACY_COLLECTIONS:
                        self.assertEqual((first / filename).read_bytes(), (self.hub / filename).read_bytes())
                    else:
                        self.assertFalse((first / filename).exists())
                if name in PRIVACY_COLLECTIONS:
                    self.assertEqual((first / PRIVACY_FILES[3]).read_bytes(), (self.hub / PRIVACY_FILES[3]).read_bytes())
                    self.assertIn("python3 scripts/privacy_guard.py json --sensitive-field customer_name", readme)
                    self.assertIn("python3 -m unittest discover -s tests -p 'test_privacy_guard.py' -v", workflow)
                    self.assertIn("python3 scripts/check_privacy_fixtures.py --check-report examples/privacy-guard-results.json", workflow)
                else:
                    self.assertNotIn("privacy_guard.py", workflow)
        manifests = []
        for output in self.outputs:
            manifest = json.loads((output / "collections-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual({item["name"] for item in manifest}, set(COLLECTION_CATEGORIES))
            for item in manifest:
                self.assertEqual(item.pop("path"), str(output / item["name"]))
            manifests.append(manifest)
        self.assertEqual(*manifests)

    def test_partial_optional_bundles_fail_before_writing_outputs(self):
        for removed in ("tests/test_privacy_guard.py", "examples/privacy-guard-results.json"):
            with self.subTest(missing=removed):
                hub = self.root / ("partial-" + Path(removed).stem)
                shutil.copytree(self.hub, hub)
                (hub / removed).unlink()
                output = hub.parent / (hub.name + "-output")
                result = generate(hub, output)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Incomplete optional bundle", result.stderr)
                self.assertIn(removed, result.stderr)
                self.assertFalse(output.exists())

    def test_absent_optional_utility_retains_catalog_only_generation(self):
        hub = self.root / "without-utility"
        shutil.copytree(self.hub, hub)
        for filename in PRIVACY_FILES[:3] + REPORT_FILES:
            (hub / filename).unlink()
        output = self.root / "without-utility-output"
        result = generate(hub, output)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name in PRIVACY_COLLECTIONS:
            root = output / name
            self.assertTrue((root / "examples/privacy-fixtures.json").is_file())
            self.assertFalse((root / "scripts/privacy_guard.py").exists())
            self.assertNotIn("privacy_guard.py", (root / ".github/workflows/validate.yml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
