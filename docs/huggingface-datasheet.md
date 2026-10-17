# Dataset datasheet draft — not published

**Status:** Planning metadata only; this file does not describe a released training dataset.  
**Snapshot date:** 2026-10-17  
**Canonical repository:** https://github.com/Francois-EF-WebOps/BabelGlobalKreole  
**Machine-readable catalog:** https://github.com/Francois-EF-WebOps/BabelGlobalKreole/blob/main/catalog.json

## Purpose

Provide a transparent description for any future dataset package derived from BabelGlobalKreole. The framework is a source-linked interoperability layer, not a single language model corpus and not a claim that Creoles form one language.

## Current contents

- 19 accepted catalogue-level language records with inspected Glottolog identifiers and source records; APiCS records are linked where their pages were inspected.
- 1 accepted, sourced variety record (Martinican Creole); the 24 unsupported duplicate variety records were removed.
- 50 source metadata records, including Glottolog and APiCS pages; a source link does not imply permission for training or speech generation.
- 14 external resource cards with per-resource verification and rights notes.
- 6 evaluation cases.
- 1 sourced lexical entry, 3 sourced grammar claims, and 1 organizing concept record.

Counts are repository snapshot values; consult `catalog.json` for generated counts and record-file hashes.

## Data provenance and inclusion

Language claims require source records and precise source locations. Candidates that lack a distinct, sourced catalogue record are listed in `docs/language-coverage.md` rather than being represented as data. Third-party source text is not mirrored under the link-first policy. The single lexical entry and grammar claims are short, attributed paraphrases/metadata from APiCS material licensed CC BY 4.0; AI training, speech generation and synthetic-data permissions remain unknown. No private ChatGPT history has been incorporated.

## Rights and consent

There is no single blanket license for all linked source materials. Rights and permitted operations must be evaluated per source and per operation. Unknown AI-use permissions remain unknown. Community consent is distinct from legal licensing. The repository's code license does not grant rights in third-party datasets, recordings, dictionaries, lyrics, or community-held knowledge.

## Intended and prohibited uses

Potential uses include discovery, provenance-aware retrieval, schema testing, and evaluation of citation/abstention behaviour. The current snapshot is not suitable as a comprehensive linguistic training corpus, benchmark of language proficiency, or authority for unsourced translation and etymology.

Do not train, fine-tune, generate speech, redistribute source content, or create synthetic data from a linked resource unless the exact operation is permitted and any required consent is established.

## Known limitations

- Coverage is highly incomplete and mostly provisional.
- 19 catalogue-level records have verified Glottocodes and ISO 639-3 identifiers from inspected Glottolog pages; these identifiers do not validate every possible lexifier, substrate, variety or community-preference claim.
- ISO 639-3 and Gallica resource pages were not accessible during the latest check and remain unverified.
- No held-out benchmark, human validation study, production API, or MCP server is claimed.
- This draft must be reviewed against a pinned release before any dataset package is published.
