# Repository validation

The validation workflow uses one authoritative dataset registry at `registry/datasets.json`. The registry declares each canonical JSONL file, its schema, record family, catalog count key, and whether it participates in repository quality checks or retrieval.

## Dataset registry

- Every JSONL file under `data/` and `evaluation/test-cases/` must be registered.
- Every registered dataset must exist and point to an existing schema.
- Unknown, missing, duplicate or unsafe dataset paths fail closed.
- Evaluation fixtures are included in catalog counts but are not loaded by retrieval and are excluded from the stricter canonical-data hygiene check.
- Adding a dataset requires one manifest entry; validation, catalog generation and retrieval consume the same registry.

## Checks

- **Schema and provenance:** Run `python scripts/validate_records.py` to validate JSON Schemas, all registered JSONL records, identifiers, negative fixtures, and evidence requirements for accepted records.
- **Repository integrity:** Run `python scripts/validation_checks.py --repository` to check tracked files for missing or zero-byte content and detect URL tracking parameters without printing full URLs.
- **Canonical dataset JSONL hygiene:** Run `python scripts/validation_checks.py --jsonl` to apply JSONL syntax and empty-value hygiene to registry entries marked `quality_checks: true`. Evaluation fixtures remain schema-validated but are excluded from this stricter policy.
- **Draft-content scan:** Run `python scripts/validation_checks.py --drafts` to check maintained Markdown and text content in project documentation and application areas. It deliberately does not scan GitHub issue-form YAML, source code, schemas, or JSONL values.
- **Internal links:** Run `python scripts/check_internal_links.py` to check local Markdown targets.
- **Regression tests:** Run `python -m unittest discover -s tests/validation -v` for validation rules and registry behavior, and `python -m unittest discover -s tests/retrieval -v` for offline retrieval behavior.
- **Catalog reproducibility:** Run `python scripts/generate_catalog.py` to regenerate counts and record hashes from the registry; CI checks that generation leaves no diff.

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

The registry establishes consistent dataset discovery and declared processing policy. It does not establish production-scale operation, external service availability, real-user adoption, or deployment readiness.
