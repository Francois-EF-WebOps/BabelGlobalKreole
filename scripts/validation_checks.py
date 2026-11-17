#!/usr/bin/env python3
"""Focused repository, JSONL hygiene, and draft-content checks."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yaml", ".yml", ".py", ".txt", ".cff", ".xml"}
DRAFT_MARKERS = re.compile(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER(?:S)?)\b", re.IGNORECASE)
URL_PATTERN = re.compile(r"""https?://[^\s<>()"']+""")
DRAFT_CONTENT_ROOTS = {
    "README.md", "CONTRIBUTING.md", "AGENTS.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "docs", "agents", "applications", "demo",
}


def _under_root(relative, roots):
    path = Path(relative)
    return any(
        relative == root or root in path.parts[:len(Path(root).parts)]
        for root in roots
    )


def should_scan_draft_content(relative):
    """Only scan maintained prose; never scan issue-form metadata or tooling."""
    return Path(relative).suffix.lower() in {".md", ".txt"} and _under_root(
        relative, DRAFT_CONTENT_ROOTS
    )


def check_draft_content(files):
    errors = []
    for relative, content in files:
        if should_scan_draft_content(relative) and DRAFT_MARKERS.search(content):
            errors.append(f"{relative}: contains an unfinished drafting marker")
    return errors


def check_jsonl_text(relative, content):
    """Check JSONL syntax and empty-value hygiene; schemas remain authoritative."""
    errors = []
    for line_no, line in enumerate(content.splitlines(), 1):
        if not line.strip():
            errors.append(f"{relative}:{line_no}: blank JSONL line")
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{relative}:{line_no}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(record, dict) or not record:
            errors.append(f"{relative}:{line_no}: record must be a non-empty JSON object")
            continue

        status = record.get("record_status")
        source_ids = record.get("source_ids")
        if status == "accepted" and not source_ids:
            errors.append(f"{relative}:{line_no}: accepted record has empty source_ids")
        if status != "draft" and "source_ids" in record and not source_ids:
            errors.append(f"{relative}:{line_no}: non-draft record has empty source_ids")

        def walk(value, trail=""):
            if value is None:
                errors.append(f"{relative}:{line_no}: null value at {trail or '<root>'}")
            elif isinstance(value, str) and not value.strip():
                errors.append(f"{relative}:{line_no}: empty string at {trail or '<root>'}")
            elif isinstance(value, list):
                if not value and not (trail == "source_ids" and status == "draft"):
                    errors.append(f"{relative}:{line_no}: empty array at {trail or '<root>'}")
                for index, child in enumerate(value):
                    walk(child, f"{trail}[{index}]")
            elif isinstance(value, dict):
                for key, child in value.items():
                    walk(child, f"{trail}.{key}" if trail else key)

        walk(record)
    return errors


def check_repository_files(root, tracked_paths):
    """Check tracked-file existence/size and URL tracking parameters."""
    errors = []
    for relative in filter(None, tracked_paths):
        path = root / relative
        if not path.is_file():
            errors.append(f"{relative}: tracked path is missing")
            continue
        if path.stat().st_size == 0:
            errors.append(f"{relative}: zero-byte tracked file")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in URL_PATTERN.finditer(content):
            url = match.group(0).rstrip(".,;]")
            if any(
                key.lower().startswith("utm_")
                for key, _ in parse_qsl(urlsplit(url).query, keep_blank_values=True)
            ):
                errors.append(f"{relative}: URL contains a tracking parameter")
    return errors


def _tracked_paths(root):
    result = subprocess.run(
        ["git", "ls-files"], cwd=root, check=True, capture_output=True, text=True
    )
    return result.stdout.splitlines()


def run_check(name):
    errors = []
    if name in {"repository", "all"}:
        try:
            errors.extend(check_repository_files(ROOT, _tracked_paths(ROOT)))
        except Exception as exc:
            print(f"ERROR: cannot check tracked files: {exc}", file=sys.stderr)
            return 2

    if name in {"jsonl", "all"}:
        for base in (ROOT / "data",):
            if not base.exists():
                continue
            for path in sorted(base.rglob("*.jsonl")):
                try:
                    errors.extend(
                        check_jsonl_text(
                            path.relative_to(ROOT).as_posix(),
                            path.read_text(encoding="utf-8"),
                        )
                    )
                except UnicodeDecodeError:
                    errors.append(f"{path.relative_to(ROOT)}: file is not UTF-8")

    if name in {"drafts", "all"}:
        try:
            tracked = _tracked_paths(ROOT)
        except Exception as exc:
            print(f"ERROR: cannot enumerate tracked files: {exc}", file=sys.stderr)
            return 2
        candidates = []
        for relative in tracked:
            if should_scan_draft_content(relative):
                try:
                    candidates.append(
                        (relative, (ROOT / relative).read_text(encoding="utf-8"))
                    )
                except (OSError, UnicodeDecodeError):
                    errors.append(f"{relative}: cannot read draft-scan content as UTF-8")
        errors.extend(check_draft_content(candidates))

    if errors:
        print(f"{name.upper()} CHECK FAILED")
        print("\n".join(errors))
        return 1
    print(f"{name.upper()} CHECK PASSED")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--repository", action="store_const", const="repository", dest="check")
    group.add_argument("--jsonl", action="store_const", const="jsonl", dest="check")
    group.add_argument("--drafts", action="store_const", const="drafts", dest="check")
    group.add_argument("--all", action="store_const", const="all", dest="check")
    args = parser.parse_args(argv)
    return run_check(args.check)


if __name__ == "__main__":
    raise SystemExit(main())
