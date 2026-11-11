#!/usr/bin/env python3
"""Run each authored standalone project's tests in its own process."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"ai-toolbox", "agent-skills", "cyber-arsenal", "llm-lab", "dev-playbooks"}


def main():
    try:
        data = json.loads((ROOT / "originals/manifest.json").read_text(encoding="utf-8"))
        projects = data["projects"]
        if data["schema_version"] != 1 or len(projects) != len(EXPECTED):
            raise ValueError("Invalid original project register")
        if {p["slug"] for p in projects} != EXPECTED:
            raise ValueError("Original project set differs")
        rows = []
        for project in projects:
            slug = project["slug"]
            base = ROOT / "originals" / slug
            if project["collection"] != "sandworm-" + slug:
                raise ValueError("Original collection identity differs")
            script = Path(project["script"])
            if (script.is_absolute() or ".." in script.parts or not (base / script).is_file()
                    or not (base / "docs/original-tool.md").is_file()
                    or not list((base / "tests").glob("test_*.py"))):
                raise ValueError("Original project is incomplete")
            result = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"],
                cwd=base, capture_output=True, text=True, encoding="utf-8", timeout=120,
            )
            rows.append({"collection": project["collection"], "passed": result.returncode == 0})
            sys.stderr.write(project["collection"] + ":\n" + result.stdout + result.stderr)
        print(json.dumps({"scope": "Original offline utility tests; no upstream tools run",
                          "all_passed": all(row["passed"] for row in rows),
                          "projects": rows}, ensure_ascii=False, indent=2))
        return 0 if all(row["passed"] for row in rows) else 1
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
        print("Cannot verify original project register or complete the test process.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
