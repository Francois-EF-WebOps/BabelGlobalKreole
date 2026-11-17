# Repository validation

The validation workflow separates schema-level data correctness from repository hygiene.

## Checks

- **Schema and provenance:** Run python scripts/validate_records.py to validate JSON Schemas, JSONL records, identifiers, negative fixtures, and evidence requirements for accepted records.
- **Repository integrity:** Run python scripts/validation_checks.py --repository to check tracked files for missing or zero-byte content and detect URL tracking parameters without printing full URLs.
- **Canonical dataset JSONL hygiene:** Run python scripts/validation_checks.py --jsonl to reject malformed or blank lines, non-object or empty records, inappropriate null or empty values, and missing source IDs on accepted records. Empty source_ids remains permitted for draft records.
- **Draft-content scan:** Run python scripts/validation_checks.py --drafts to check maintained Markdown and text content in project documentation and application areas. It deliberately does not scan GitHub issue-form YAML, source code, schemas, or JSONL values; issue-form field hint text is user guidance, not unfinished project content.
- **Internal links:** Run python scripts/check_internal_links.py to check local Markdown targets.
- **Regression tests:** Run python -m unittest discover -s tests/validation -v for validation rules and python -m unittest discover -s tests/retrieval -v for offline retrieval behaviour.
- **Catalog reproducibility:** Run python scripts/generate_catalog.py to regenerate the catalog; CI checks that generation leaves no diff.

## Run the complete local sequence

    python -m pip install -r requirements-dev.txt
    python scripts/validate_records.py
    python scripts/validation_checks.py --repository
    python scripts/validation_checks.py --jsonl
    python scripts/validation_checks.py --drafts
    python scripts/check_internal_links.py
    python -m unittest discover -s tests/validation -v
    python -m unittest discover -s tests/retrieval -v
    python scripts/generate_catalog.py
    git diff --exit-code -- catalog.json

## Limitations

These checks establish repository-level consistency and reproducibility in CI. They do not establish production-scale operation, external service availability, real-user adoption, or deployment readiness.
