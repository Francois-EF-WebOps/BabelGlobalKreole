# Data model and identifiers

Use stable opaque lowercase IDs with type prefixes. The canonical prefixes are:

| Prefix | Record type |
|---|---|
| `lng-` | Language |
| `var-` | Language variety |
| `src-` | Source |
| `lex-` | Lexical entry |
| `grm-` | Grammar rule |
| `evl-` | Evaluation case |
| `con-` | Concept |

Additional record types may receive prefixes only through a documented schema and decision. Do not encode mutable spellings, definitions or statuses in IDs; never recycle retired IDs. Schema patterns and validator mappings must agree with this table.

## Record families

Language/variety, concept, lexical entry, grammar rule, source, linguistic claim, evaluation case, application/integration, resource card, creative work, decision/change record.

## Invariants

- One record represents one scoped item or assertion.
- Relationships use stable IDs.
- Missing values stay missing or explicitly unresolved; never fabricate data to satisfy a schema.
- Evidence, rights, community consent and review statuses are separate.
- A verified external identifier requires a checked date and source IDs.
- Variants are represented explicitly, not overwritten.
- Every lexical or grammar claim has source IDs and a precise source location; source records describe provenance rather than substitute for locations.
- Every release snapshot declares framework/schema versions, record IDs, build date, validation result and reproducible hashes.

## Formats

Markdown for policy, YAML for registries, JSON for individual records, JSONL/CSV for bulk exchange. No database is required for the initial release.

## Compatibility

Non-breaking changes add optional fields or clarify semantics without invalidating accepted records. Removing/renaming fields, changing requiredness or changing field meaning is breaking and requires a major schema version and migration instructions. Every schema must carry a stable `$id` and `schema_version`; schema versions are explicit data, not inferred from a filename.
