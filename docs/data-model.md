# Data model and identifiers

Use stable opaque lowercase IDs with type prefixes: `lex-...`, `grm-...`, `src-...`, `evl-...`, `con-...`. Do not encode mutable spellings, definitions or statuses in IDs; never recycle retired IDs.

## Record families
Language/variety, concept, lexical entry, grammar rule, source, linguistic claim, evaluation case, application/integration, decision/change record.

## Invariants
- One record represents one scoped item or assertion.
- Relationships use stable IDs.
- Missing values stay missing or explicitly unresolved; never fabricate data to satisfy a schema.
- Evidence, rights and review statuses are separate.
- Variants are represented explicitly, not overwritten.
- Every release snapshot declares framework/schema versions, record IDs, build date and validation result.

## Formats
Markdown for policy, YAML for registries, JSON for records, JSONL/CSV for bulk exchange. No database is required for the initial release.

## Compatibility
Non-breaking changes add optional fields or clarify semantics without invalidating accepted records. Removing/renaming fields, changing requiredness or changing field meaning is breaking and requires a major schema version and migration instructions.
