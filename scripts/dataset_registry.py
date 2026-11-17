"""Authoritative discovery and policy for repository JSONL datasets."""
import json
from pathlib import Path

REGISTRY_RELATIVE_PATH = "registry/datasets.json"
DISCOVERY_ROOTS = ("data", "evaluation/test-cases")
REQUIRED_FIELDS = {
    "id", "path", "schema", "record_family", "catalog_key",
    "quality_checks", "retrieval",
}


def discover_jsonl_paths(root):
    """Return every JSONL file in the repository's canonical dataset roots."""
    root = Path(root)
    found = set()
    for relative_root in DISCOVERY_ROOTS:
        base = root / relative_root
        if base.exists():
            found.update(
                path.relative_to(root).as_posix()
                for path in base.rglob("*.jsonl")
                if path.is_file()
            )
    return found


def _safe_relative_path(value):
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def load_dataset_registry(root):
    """Load the manifest and report missing, duplicate, unsafe or unregistered paths."""
    root = Path(root)
    manifest_path = root / REGISTRY_RELATIVE_PATH
    errors = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {}, [], [f"{REGISTRY_RELATIVE_PATH}: cannot read valid JSON: {exc}"]

    if not isinstance(manifest, dict) or manifest.get("registry_version") != 1:
        return {}, [], [f"{REGISTRY_RELATIVE_PATH}: registry_version must be 1"]
    datasets = manifest.get("datasets")
    if not isinstance(datasets, list) or not datasets:
        return manifest, [], [f"{REGISTRY_RELATIVE_PATH}: datasets must be a non-empty array"]

    seen_ids = set()
    seen_paths = set()
    valid_entries = []
    for index, entry in enumerate(datasets):
        label = f"{REGISTRY_RELATIVE_PATH}:datasets[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label}: dataset entry must be an object")
            continue
        missing = sorted(REQUIRED_FIELDS - set(entry))
        if missing:
            errors.append(f"{label}: missing fields: {', '.join(missing)}")
            continue

        dataset_id = entry["id"]
        relative_path = entry["path"]
        schema_path = entry["schema"]
        if not isinstance(dataset_id, str) or not dataset_id.strip():
            errors.append(f"{label}: id must be a non-empty string")
            continue
        if dataset_id in seen_ids:
            errors.append(f"{label}: duplicate dataset id {dataset_id}")
        seen_ids.add(dataset_id)

        if not _safe_relative_path(relative_path) or not relative_path.endswith(".jsonl"):
            errors.append(f"{label}: path must be a safe repository-relative .jsonl path")
            continue
        if relative_path in seen_paths:
            errors.append(f"{label}: duplicate dataset path {relative_path}")
        seen_paths.add(relative_path)

        if not _safe_relative_path(schema_path) or not schema_path.endswith(".schema.json"):
            errors.append(f"{label}: schema must be a safe repository-relative .schema.json path")
            continue
        if not (root / schema_path).is_file():
            errors.append(f"{label}: schema file is missing: {schema_path}")
        if not (root / relative_path).is_file():
            errors.append(f"{label}: dataset file is missing: {relative_path}")
        if not isinstance(entry["record_family"], str) or not entry["record_family"]:
            errors.append(f"{label}: record_family must be a non-empty string")
        if not isinstance(entry["catalog_key"], str) or not entry["catalog_key"]:
            errors.append(f"{label}: catalog_key must be a non-empty string")
        if not isinstance(entry["quality_checks"], bool):
            errors.append(f"{label}: quality_checks must be boolean")
        if not isinstance(entry["retrieval"], bool):
            errors.append(f"{label}: retrieval must be boolean")
        if entry["retrieval"] and not relative_path.startswith("data/"):
            errors.append(f"{label}: only data/ datasets may be retrieval-enabled")
        valid_entries.append(entry)

    discovered = discover_jsonl_paths(root)
    for relative_path in sorted(discovered - seen_paths):
        errors.append(f"{relative_path}: JSONL dataset is not registered in {REGISTRY_RELATIVE_PATH}")
    for relative_path in sorted(seen_paths - discovered):
        errors.append(f"{relative_path}: registered dataset is outside canonical discovery roots")

    source_id = manifest.get("source_dataset_id")
    if source_id not in seen_ids:
        errors.append(f"{REGISTRY_RELATIVE_PATH}: source_dataset_id does not identify a registered dataset")
    elif not any(
        entry.get("id") == source_id and entry.get("record_family") == "source"
        for entry in valid_entries
    ):
        errors.append(f"{REGISTRY_RELATIVE_PATH}: source_dataset_id must identify a source record dataset")

    catalog_paths = manifest.get("catalog_paths")
    if not isinstance(catalog_paths, dict):
        errors.append(f"{REGISTRY_RELATIVE_PATH}: catalog_paths must be an object")
    else:
        for entry in valid_entries:
            if entry.get("catalog_key") not in catalog_paths:
                errors.append(
                    f"{REGISTRY_RELATIVE_PATH}: missing catalog_paths entry for {entry.get('catalog_key')}"
                )

    return manifest, valid_entries, errors
