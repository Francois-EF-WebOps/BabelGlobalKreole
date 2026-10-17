"""Read-only record access and evidence/rights gates for the MCP server."""
import json
from pathlib import Path

from scripts.record_integrity import extract_record_id

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"
CONTENT_FIELDS = {
    "form", "definition", "examples", "counterexamples", "pronunciation",
    "statement", "autonyms", "notes",
}


def load_records(data_root=DATA_ROOT):
    records = []
    for path in sorted(Path(data_root).rglob("*.jsonl")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            item = json.loads(line)
            item["_repository_path"] = path.relative_to(Path(data_root)).as_posix()
            item["_line"] = line_no
            records.append(item)
    return records


def source_index(records):
    return {record["source_id"]: record for record in records if record.get("source_id")}


def evidence_eligibility(record, sources):
    """Only accepted records with resolvable, dated, located sources can be evidence."""
    ids = record.get("source_ids")
    if record.get("record_status") != "accepted" or not isinstance(ids, list) or not ids:
        return False, "Record is not accepted or has no source IDs."
    for source_id in ids:
        source = sources.get(source_id)
        if source is None:
            return False, f"Source ID {source_id} does not resolve."
        if not all(source.get(key) for key in ("canonical_url", "accessed_date", "relevant_location")):
            return False, f"Source ID {source_id} lacks a URL, access date, or precise location."
    return True, "Accepted record has resolvable source metadata."


def safe_record_view(record, sources):
    """Return record metadata without exposing content whose retrieval is not allowed."""
    view = {key: value for key, value in record.items() if not key.startswith("_")}
    eligible, reason = evidence_eligibility(record, sources)
    view["evidence_eligible"] = eligible
    view["evidence_note"] = reason
    ai_use = record.get("ai_use")
    retrieval = ai_use.get("retrieval") if isinstance(ai_use, dict) else None
    if retrieval != "allowed":
        for field in CONTENT_FIELDS:
            view.pop(field, None)
        view["content_withheld"] = True
        view["content_withheld_reason"] = (
            "Retrieval permission is not explicitly allowed for this record; only metadata is returned."
        )
    else:
        view["content_withheld"] = False
    return view


def search_records(query, records=None, limit=10):
    records = records if records is not None else load_records()
    sources = source_index(records)
    q = query.strip().casefold()
    if not q:
        return {"query": query, "results": [], "abstained": True, "reason": "Empty query."}
    try:
        limit = max(1, min(int(limit), 50))
    except (TypeError, ValueError):
        limit = 10
    matches = []
    for record in records:
        rid = extract_record_id(record)
        if not rid:
            continue
        ai_use = record.get("ai_use")
        can_search_content = isinstance(ai_use, dict) and ai_use.get("retrieval") == "allowed"
        searchable = []
        for key, value in record.items():
            if key.startswith("_") or key in {"source_ids", "ai_use"}:
                continue
            if key in CONTENT_FIELDS and not can_search_content:
                continue
            searchable.append(str(value))
        haystack = " ".join(searchable).casefold()
        if q in rid.casefold() or q in haystack:
            matches.append({
                "record_id": rid,
                "path": record.get("_repository_path"),
                "line": record.get("_line"),
                "record": safe_record_view(record, sources),
            })
    # Prefer eligible evidence records so a prefix of draft matches cannot hide them.
    matches.sort(key=lambda item: not item["record"]["evidence_eligible"])
    matches = matches[:limit]
    eligible_found = any(item["record"]["evidence_eligible"] for item in matches)
    return {
        "query": query,
        "results": matches,
        "abstained": not eligible_found,
        "reason": (
            "No accepted, source-resolved evidence record matched; draft/provisional matches are metadata only."
            if not eligible_found
            else "At least one accepted record has resolvable source metadata; inspect each record's evidence note and rights fields."
        ),
    }

def get_record(record_id, records=None):
    records = records if records is not None else load_records()
    sources = source_index(records)
    for record in records:
        if extract_record_id(record) == record_id:
            return {
                "record_id": record_id,
                "path": record.get("_repository_path"),
                "line": record.get("_line"),
                "record": safe_record_view(record, sources),
            }
    return {"record_id": record_id, "found": False, "evidence_eligible": False, "reason": "No repository record matches this ID."}


def get_catalog():
    return json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
