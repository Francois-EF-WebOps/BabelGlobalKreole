#!/usr/bin/env python3
"""Offline validation of schemas and versioned JSONL records."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("VALIDATION FAILED: install requirements-dev.txt (jsonschema dependency).")
    sys.exit(2)

schema_paths = sorted(ROOT.rglob("*.schema.json"))
schemas = {}
for path in schema_paths:
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        schemas[path.name] = schema
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid schema: {exc}")

record_schema_by_parent = {
    "lexicon": "lexical-entry.schema.json",
    "sources": "source-record.schema.json",
    "test-cases": "evaluation-case.schema.json",
}
records_checked = 0
jsonl_paths = sorted(list((ROOT / "data").rglob("*.jsonl")) +
                      list((ROOT / "evaluation" / "test-cases").glob("*.jsonl")))
for path in jsonl_paths:
    schema_name = record_schema_by_parent.get(path.parent.name)
    schema = schemas.get(schema_name) if schema_name else None
    if schema_name and schema is None:
        errors.append(f"{path.relative_to(ROOT)}: missing schema {schema_name}")
        continue
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}:{line_no}: invalid JSON: {exc}")
            continue
        records_checked += 1
        if schema is not None:
            validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
            for issue in validator.iter_errors(item):
                location = ".".join(str(p) for p in issue.absolute_path) or "<root>"
                errors.append(f"{path.relative_to(ROOT)}:{line_no}:{location}: {issue.message}")

registry = ROOT / "registry" / "projects.yaml"
if not registry.exists():
    errors.append("missing registry/projects.yaml")
if not (ROOT / "agents" / "consumer-answer.schema.json").exists():
    errors.append("missing consumer answer schema")

if errors:
    print("VALIDATION FAILED")
    print("\n".join(errors))
    sys.exit(1)
print(f"VALIDATION PASSED: {len(schema_paths)} JSON Schemas checked; {records_checked} JSONL records validated.")
