#!/usr/bin/env python3
"""Generate a deterministic record catalog with counts and SHA-256 hashes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD_ROOTS = [ROOT / "data", ROOT / "evaluation" / "test-cases"]
record_files = sorted({p for base in RECORD_ROOTS if base.exists() for p in base.rglob("*.jsonl")})
counts = {
    "lexical_entries": 0,
    "source_records": 0,
    "language_records": 0,
    "variety_records": 0,
    "grammar_rules": 0,
    "resource_cards": 0,
    "evaluation_cases": 0,
}
for path in record_files:
    rel = path.relative_to(ROOT).as_posix()
    count = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    if rel.startswith("data/lexicon/"):
        counts["lexical_entries"] += count
    elif rel.startswith("data/sources/"):
        counts["source_records"] += count
    elif rel.startswith("data/languages/"):
        counts["language_records"] += count
    elif rel.startswith("data/varieties/"):
        counts["variety_records"] += count
    elif rel.startswith("data/grammar/"):
        counts["grammar_rules"] += count
    elif rel.startswith("data/resources/"):
        counts["resource_cards"] += count
    elif rel.startswith("evaluation/test-cases/"):
        counts["evaluation_cases"] += count

hashes = {
    path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
    for path in record_files
}
schemas = sorted(
    p.relative_to(ROOT).as_posix()
    for base in [ROOT / "schemas", ROOT / "agents"]
    for p in base.glob("*.schema.json")
)
catalog = {
    "catalog_version": 1,
    "framework": "Babel / Global (K)Creole",
    "framework_version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
    "status": "bootstrap",
    "record_counts": counts,
    "record_paths": {
        "lexical_entries": "data/lexicon/",
        "source_records": "data/sources/",
        "language_records": "data/languages/languages.jsonl",
        "variety_records": "data/varieties/varieties.jsonl",
        "grammar_rules": "data/grammar/",
        "resource_cards": "data/resources/resources.jsonl",
        "evaluation_cases": "evaluation/test-cases/",
    },
    "record_file_hashes": hashes,
    "schemas": schemas,
    "catalog_generator": "scripts/generate_catalog.py",
    "note": "Generated deterministically from current JSONL record files. Counts describe records stored in this repository, not global language coverage.",
}
(ROOT / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(f"CATALOG GENERATED: {len(record_files)} JSONL files; {sum(counts.values())} records; SHA-256 hashes written.")
