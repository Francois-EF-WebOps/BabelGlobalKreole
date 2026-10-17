#!/usr/bin/env python3
"""Offline, read-only retrieval demo. Never treats drafts or unsourced records as evidence."""
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
ANSWER_SCHEMA_PATH = ROOT / "agents" / "consumer-answer.schema.json"
VERSION_PATH = ROOT / "VERSION"
DATA_ROOT = ROOT / "data"


def load_records(data_root=DATA_ROOT):
    records = []
    for path in sorted(Path(data_root).rglob("*.jsonl")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSONL: {exc}") from exc
            item["_repository_path"] = path.relative_to(Path(data_root)).as_posix()
            records.append(item)
    return records


def record_id(record):
    for key in ("variety_id", "language_id", "source_id", "entry_id", "lex_id", "rule_id", "case_id", "concept_id", "work_id", "id"):
        value = record.get(key)
        if isinstance(value, str) and value.startswith(("lng-", "var-", "src-", "lex-", "grm-", "evl-", "con-", "wrk-", "res-")):
            return value
    return None


def searchable_text(record):
    fields = ("name", "title", "lemma", "label", "language_id", "variety_id", "source_id", "id")
    return " ".join(str(record.get(key, "")) for key in fields).casefold()


def build_answer(query, records, framework_version=None):
    query = query.strip()
    version = framework_version or "unknown"
    if not query:
        answer = {
            "answer_status": "abstained",
            "answer": "No query was supplied. Provide a record ID or a name present in repository metadata.",
            "claims": [],
            "sources": [],
            "uncertainties": ["Empty query."],
            "rights_notes": ["This offline demo searches repository metadata only and does not authorize reuse of source content."],
            "framework_version": version,
        }
        return validate_answer(answer)

    source_map = {r.get("source_id"): r for r in records if r.get("source_id")}
    q = query.casefold()
    matches = [r for r in records if record_id(r) and (record_id(r).casefold() == q or q in searchable_text(r))]
    if not matches:
        answer = {
            "answer_status": "abstained",
            "answer": f"No matching repository record was found for {query!r}.",
            "claims": [],
            "sources": [],
            "uncertainties": ["The repository contains no matching record; no external source was fetched by this offline demo."],
            "rights_notes": ["No source content was retrieved or reproduced."],
            "framework_version": version,
        }
        return validate_answer(answer)

    supported = []
    draft_matches = []
    for record in matches:
        ids = record.get("source_ids")
        if record.get("record_status") != "accepted" or not isinstance(ids, list) or not ids:
            draft_matches.append(record)
            continue
        if any(
            source_id not in source_map
            or not source_map[source_id].get("canonical_url")
            or not source_map[source_id].get("accessed_date")
            or not source_map[source_id].get("relevant_location")
            for source_id in ids
        ):
            draft_matches.append(record)
            continue
        supported.append(record)

    if not supported:
        names = [str(r.get("name") or r.get("title") or r.get("lemma") or r.get("form") or record_id(r)) for r in draft_matches]
        answer = {
            "answer_status": "abstained",
            "answer": "Matching metadata exists, but none of the matching records is eligible evidence: records must be accepted and have non-empty source_ids resolving to source records. Matches: " + ", ".join(names),
            "claims": [],
            "sources": [],
            "uncertainties": ["Matching records are draft/proposed or have missing/empty/unresolved source_ids. They were not cited as evidence."],
            "rights_notes": ["Source links and metadata do not grant permission to copy, redistribute, train on, or synthesize source content."],
            "framework_version": version,
        }
        return validate_answer(answer)

    claims = []
    citations = {}
    for record in supported:
        rid = record_id(record)
        name = str(record.get("name") or record.get("title") or rid)
        evidence = record.get("evidence_status")
        allowed = {"attested", "scholarly_analysis", "comparative_observation", "proposed_convergence", "creative_coinage", "application_canon", "disputed", "undecided", "retracted"}
        if evidence not in allowed:
            evidence = record.get("label") if record.get("label") in allowed else "undecided"
        claims.append({
            "claim": f"Repository record {rid} is named {name!r}; this reports stored metadata, not an independent linguistic conclusion.",
            "record_ids": [rid],
            "evidence_labels": [evidence],
        })
        for source_id in record["source_ids"]:
            source = source_map[source_id]
            location = source.get("relevant_location")
            if location:
                citations[source_id] = {
                    "source_id": source_id,
                    "location": str(location),
                    "citation": f"{source.get('title', source_id)} — {source.get('canonical_url', '')}",
                }
    answer = {
        "answer_status": "partial",
        "answer": f"Found {len(supported)} accepted repository record(s) matching {query!r}. The statements below summarize stored metadata only.",
        "claims": claims,
        "sources": list(citations.values()),
        "uncertainties": ["This demo does not independently re-evaluate source content; check the cited source location and record scope before relying on a claim."],
        "rights_notes": ["Citations are not reuse permissions. The demo does not return source text; follow each source record's rights and AI-use fields."],
        "framework_version": version,
    }
    return validate_answer(answer)


def validate_answer(answer):
    schema = json.loads(ANSWER_SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(answer), key=lambda e: list(e.absolute_path))
    if errors:
        detail = "; ".join(f"{'.'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in errors)
        raise ValueError(f"Consumer answer schema validation failed: {detail}")
    return answer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="", help="Record ID or text query")
    args = parser.parse_args()
    version = VERSION_PATH.read_text(encoding="utf-8").strip()
    answer = build_answer(args.query, load_records(), version)
    print(json.dumps(answer, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
