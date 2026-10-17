"""Helpers for stable record identity checks."""

RECORD_ID_KEYS = (
    "variety_id",
    "entry_id",
    "rule_id",
    "case_id",
    "concept_id",
    "work_id",
    "source_id",
    "language_id",
    "lex_id",
    "id",
)


def extract_record_id(record):
    """Return the canonical record ID, preferring a record's own ID over parent links."""
    return next(
        (record.get(key) for key in RECORD_ID_KEYS if isinstance(record.get(key), str)),
        None,
    )


def register_record_id(record, seen, path, line_no):
    """Register an ID; return its first location if the ID is already present."""
    record_id = extract_record_id(record)
    if not record_id:
        return None
    if record_id in seen:
        return seen[record_id]
    seen[record_id] = (path, line_no)
    return None
