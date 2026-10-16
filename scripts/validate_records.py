#!/usr/bin/env python3
"""Offline structural checks; standard library only."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
errors = []
schemas = list((ROOT / "schemas").glob("*.schema.json"))
for path in schemas:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{path}: unexpected schema dialect")
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
for path in sorted((ROOT / "evaluation" / "test-cases").glob("*.jsonl")):
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except Exception as exc:
            errors.append(f"{path}:{line_no}: invalid JSONL: {exc}")
            continue
        for key in ("case_id", "test_type", "input", "expected_property", "severity"):
            if key not in item:
                errors.append(f"{path}:{line_no}: missing {key}")
        if item.get("severity") not in {"blocker", "high", "medium", "low"}:
            errors.append(f"{path}:{line_no}: invalid severity")
if not (ROOT / "registry" / "projects.yaml").exists():
    errors.append("missing project registry")
if errors:
    print("VALIDATION FAILED\n" + "\n".join(errors))
    sys.exit(1)
print(f"VALIDATION PASSED: {len(schemas)} schema JSON files and starter JSONL cases parsed.")
print("Note: this is not a full JSON Schema validator.")
