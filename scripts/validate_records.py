#!/usr/bin/env python3
"""Offline schema, JSONL, format, and negative-fixture validation."""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from dataset_registry import load_dataset_registry
from record_integrity import register_record_id

ROOT = Path(__file__).resolve().parents[1]
errors = []
format_checker = FormatChecker()
schema_paths = sorted(ROOT.rglob("*.schema.json"))
schemas = {}
schemas_by_path = {}
for path in schema_paths:
    relative_schema = path.relative_to(ROOT).as_posix()
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        if not isinstance(schema.get("$id"), str) or not schema["$id"].startswith("https://"):
            errors.append(f"{relative_schema}: missing absolute HTTPS $id")
        if not isinstance(schema.get("schema_version"), str) or not schema["schema_version"]:
            errors.append(f"{relative_schema}: missing schema_version")
        schemas[path.name] = schema
        schemas_by_path[relative_schema] = schema
    except Exception as exc:
        errors.append(f"{relative_schema}: invalid schema: {exc}")

manifest, datasets, registry_errors = load_dataset_registry(ROOT)
errors.extend(registry_errors)
records_checked = 0
accepted_records = []
seen_record_ids = {}
for dataset in datasets:
    relative_path = dataset["path"]
    path = ROOT / relative_path
    schema = schemas_by_path.get(dataset["schema"])
    if schema is None:
        errors.append(f"{relative_path}: missing or invalid schema {dataset['schema']}")
        continue
    validator = Draft202012Validator(schema, format_checker=format_checker)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{relative_path}: cannot read dataset as UTF-8: {exc}")
        continue

    for line_no, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{relative_path}:{line_no}: invalid JSON: {exc}")
            continue
        records_checked += 1
        duplicate_location = register_record_id(item, seen_record_ids, relative_path, line_no)
        if duplicate_location:
            previous_path, previous_line = duplicate_location
            record_id = next(
                (item.get(key) for key in (
                    "variety_id", "language_id", "source_id", "entry_id", "lex_id",
                    "rule_id", "case_id", "concept_id", "work_id", "id",
                ) if isinstance(item.get(key), str)),
                None,
            )
            errors.append(
                f"{relative_path}:{line_no}: duplicate record ID {record_id}; "
                f"first seen at {previous_path}:{previous_line}"
            )
        if isinstance(item, dict) and item.get("record_status") == "accepted":
            if not item.get("source_ids"):
                errors.append(f"{relative_path}:{line_no}: accepted record must have at least one source_id")
            else:
                accepted_records.append((relative_path, line_no, item))
        for issue in validator.iter_errors(item):
            location = ".".join(str(part) for part in issue.absolute_path) or "<root>"
            errors.append(f"{relative_path}:{line_no}:{location}: {issue.message}")

# Accepted records resolve only against the registered source dataset.
source_dataset_id = manifest.get("source_dataset_id") if isinstance(manifest, dict) else None
source_dataset = next((item for item in datasets if item["id"] == source_dataset_id), None)
source_records = {}
if source_dataset:
    source_path = ROOT / source_dataset["path"]
    try:
        for line_no, line in enumerate(source_path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                source = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{source_dataset['path']}:{line_no}: invalid source JSON: {exc}")
                continue
            if isinstance(source, dict) and source.get("source_id"):
                if source["source_id"] in source_records:
                    errors.append(
                        f"{source_dataset['path']}:{line_no}: duplicate source_id {source['source_id']}"
                    )
                else:
                    source_records[source["source_id"]] = source
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{source_dataset['path']}: cannot read source dataset: {exc}")


def collect_source_ids(value):
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "source_ids" and isinstance(child, list):
                found.extend(item for item in child if isinstance(item, str))
            else:
                found.extend(collect_source_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(collect_source_ids(child))
    return found


for relative_path, line_no, record in accepted_records:
    for source_id in sorted(set(collect_source_ids(record))):
        source = source_records.get(source_id)
        if source is None:
            errors.append(f"{relative_path}:{line_no}: accepted record references unknown source_id {source_id}")
            continue
        for field in ("canonical_url", "accessed_date", "relevant_location"):
            if not source.get(field):
                errors.append(f"{relative_path}:{line_no}: source {source_id} lacks required evidence field {field}")
        if source.get("review_status") not in {"inspected", "rights-checked", "approved-for-use"}:
            errors.append(f"{relative_path}:{line_no}: source {source_id} is not inspected or rights-checked")
        if source.get("rights_status") != "verified-permitted":
            errors.append(f"{relative_path}:{line_no}: source {source_id} lacks verified permitted reuse rights")

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
    schema = schemas.get(schema_path.name)
    if schema is None:
        continue
    validator = Draft202012Validator(schema, format_checker=format_checker)
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
print(
    f"VALIDATION PASSED: {len(schema_paths)} JSON Schemas checked; "
    f"{records_checked} registered JSONL records validated; "
    f"{len(datasets)} registered datasets checked; "
    f"{fixtures_checked} negative fixtures rejected; format checking enabled."
)
