#!/usr/bin/env python3
"""Reject empty tracked files, obvious drafting markers, and incomplete data records."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yaml", ".yml", ".py", ".txt", ".cff"}
DRAFT_MARKERS = re.compile(r"\b(?:TODO|TBD|FIXME)\b", re.IGNORECASE)
errors = []

try:
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True,
        capture_output=True, text=True
    ).stdout.split("\0")
except Exception as exc:
    print(f"ERROR: cannot enumerate tracked files: {exc}")
    sys.exit(2)

for relative in filter(None, tracked):
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"{relative}: tracked path is missing")
        continue
    if path.stat().st_size == 0:
        errors.append(f"{relative}: zero-byte file")
        continue
    if path.suffix.lower() not in TEXT_SUFFIXES:
        continue
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if DRAFT_MARKERS.search(content):
        errors.append(f"{relative}: contains TODO/TBD/FIXME marker")

# Empty arrays are forbidden in data records except source_ids on draft records.
# Evaluation cases are test descriptions and may intentionally contain empty inputs.
for path in sorted((ROOT / "data").rglob("*.jsonl")):
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            errors.append(f"{path.relative_to(ROOT)}:{line_no}: blank JSONL line")
            continue
        try:
            record = json.loads(line)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}:{line_no}: invalid JSON: {exc}")
            continue
        record_status = record.get("record_status")
        source_ids = record.get("source_ids")
        if record_status == "accepted" and not source_ids:
            errors.append(f"{path.relative_to(ROOT)}:{line_no}: accepted record has empty source_ids")
        if record_status != "draft" and "source_ids" in record and not source_ids:
            errors.append(f"{path.relative_to(ROOT)}:{line_no}: non-draft record has empty source_ids")
        def walk(value, trail=""):
            if isinstance(value, list):
                if not value and not (trail == "source_ids" and record_status == "draft"):
                    errors.append(f"{path.relative_to(ROOT)}:{line_no}: empty array at {trail or '<root>'}")
                for index, child in enumerate(value):
                    walk(child, f"{trail}[{index}]")
            elif isinstance(value, dict):
                for key, child in value.items():
                    walk(child, f"{trail}.{key}" if trail else key)
        walk(record)

if errors:
    print("NO-PLACEHOLDERS CHECK FAILED")
    print("\n".join(errors))
    sys.exit(1)
print("NO-PLACEHOLDERS CHECK PASSED: tracked files are non-empty; no TODO/TBD/FIXME markers; data records have no empty arrays except source_ids on draft records.")
