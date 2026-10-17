#!/usr/bin/env python3
"""Offline schema, JSONL, format, and negative-fixture validation."""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
errors = []
format_checker = FormatChecker()
schema_paths = sorted(ROOT.rglob("*.schema.json"))
schemas = {}
for path in schema_paths:
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        if not isinstance(schema.get("$id"), str) or not schema["$id"].startswith("https://"):
            errors.append(f"{path.relative_to(ROOT)}: missing absolute HTTPS $id")
        if not isinstance(schema.get("schema_version"), str) or not schema["schema_version"]:
            errors.append(f"{path.relative_to(ROOT)}: missing schema_version")
        schemas[path.name] = schema
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid schema: {exc}")

record_schema_by_parent = {
    "lexicon": "lexical-entry.schema.json",
    "concepts": "concept.schema.json",
    "sources": "source-record.schema.json",
    "languages": "language.schema.json",
    "varieties": "variety.schema.json",
    "grammar": "grammar-rule.schema.json",
    "resources": "resource-card.schema.json",
    "test-cases": "evaluation-case.schema.json",
}
records_checked = 0
accepted_records = []
record_paths = sorted((ROOT / "data").rglob("*.jsonl")) + sorted((ROOT / "evaluation" / "test-cases").glob("*.jsonl"))
for path in record_paths:
    schema_name = record_schema_by_parent.get(path.parent.name)
    schema = schemas.get(schema_name) if schema_name else None
    if schema_name and schema is None:
        errors.append(f"{path.relative_to(ROOT)}: missing schema {schema_name}")
        continue
    if schema is None:
        errors.append(f"{path.relative_to(ROOT)}: no schema mapping for JSONL directory")
        continue
    validator = Draft202012Validator(schema, format_checker=format_checker)
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}:{line_no}: invalid JSON: {exc}")
            continue
        records_checked += 1
        if item.get("record_status") == "accepted":
            if not item.get("source_ids"):
                errors.append(f"{path.relative_to(ROOT)}:{line_no}: accepted record must have at least one source_id")
            else:
                accepted_records.append((path.relative_to(ROOT).as_posix(), line_no, item))
        for issue in validator.iter_errors(item):
            location = ".".join(str(p) for p in issue.absolute_path) or "<root>"
            errors.append(f"{path.relative_to(ROOT)}:{line_no}:{location}: {issue.message}")

# Every accepted record must resolve to source records with a URL, access date,
# and precise location. This prevents a non-empty but dangling source_ids array
# from passing validation.
source_path = ROOT / "data" / "sources" / "sources.jsonl"
source_records = {}
if source_path.exists():
    for line_no, line in enumerate(source_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            source = json.loads(line)
            if source.get("source_id"):
                source_records[source["source_id"]] = source
        except Exception:
            pass
for relative, line_no, record in accepted_records:
    for source_id in record.get("source_ids", []):
        source = source_records.get(source_id)
        if source is None:
            errors.append(f"{relative}:{line_no}: accepted record references unknown source_id {source_id}")
            continue
        for field in ("canonical_url", "accessed_date", "relevant_location"):
            if not source.get(field):
                errors.append(f"{relative}:{line_no}: source {source_id} lacks required evidence field {field}")

# Every schema must have an intentionally invalid fixture; CI must fail if any
# fixture is accidentally accepted or missing.
negative_dir = ROOT / "tests" / "negative"
fixtures_checked = 0
for schema_path in schema_paths:
    fixture_path = negative_dir / f"{schema_path.name}.invalid.json"
    if not fixture_path.exists():
        errors.append(f"missing negative fixture: {fixture_path.relative_to(ROOT)}")
        continue
    try:
        instance = json.loads(fixture_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{fixture_path.relative_to(ROOT)}: invalid fixture JSON: {exc}")
        continue
    validator = Draft202012Validator(schemas[schema_path.name], format_checker=format_checker)
    if not list(validator.iter_errors(instance)):
        errors.append(f"{fixture_path.relative_to(ROOT)}: negative fixture unexpectedly passed {schema_path.name}")
    else:
        fixtures_checked += 1

registry = ROOT / "registry" / "projects.yaml"
if not registry.exists():
    errors.append("missing registry/projects.yaml")
if not (ROOT / "agents" / "consumer-answer.schema.json").exists():
    errors.append("missing consumer answer schema")

if errors:
    print("VALIDATION FAILED")
    print("\n".join(errors))
    sys.exit(1)
print(f"VALIDATION PASSED: {len(schema_paths)} JSON Schemas checked; {records_checked} JSONL records validated; {fixtures_checked} negative fixtures rejected; format checking enabled.")
