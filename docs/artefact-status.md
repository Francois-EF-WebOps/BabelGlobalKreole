# Artefact status and acceptance register

Audit baseline: `main` at `f9ca6385cfa7682093672bef6bb774bf43c121b0` (2026-10-17 UTC). This register distinguishes files that exist from requirements that are actually satisfied. "Complete" is scoped to the stated artefact, not the entire framework release.

| Path / artefact | State | Done criteria |
|---|---|---|
| `.github/workflows/validate.yml` | stub | CI validates all schemas, positive and negative fixtures, record files, catalog freshness, link checks, and offline demo tests; required checks pass. |
| `.gitignore` | complete | Excludes local secrets, build outputs, caches, and temporary files without hiding required source artefacts. |
| `AGENTS.md` | stub | Root instructions state safe editing, evidence, rights, validation, source-injection handling, and stop conditions. |
| `CHANGELOG.md` | stub | Every release records user-visible changes and limitations accurately. |
| `CITATION.cff` | stub | Valid citation metadata matches canonical project, version, repository URL, and release. |
| `CONTRIBUTING.md` | stub | A mobile-accessible contributor can propose, source, validate, and submit a correction with rights and evidence. |
| `DATA-LICENSE.md` | stub | Code, framework documentation, data, and third-party material have distinct explicit rights and AI-use rules. |
| `GOVERNANCE.md` | stub | Decision authority, review, appeals, consent, disputed claims, and maintenance succession are explicit and workable for a solo maintainer. |
| `LICENSE` | complete | Repository code/documentation license file exists; scope exclusions and third-party/data exceptions are explained elsewhere. |
| `README.md` | stub | Required verbatim intent is present; audience-based entry points, accurate status, working links, contribution path, and no unsupported claims. |
| `VERSION` | stub | Version is consistent with schemas, changelog, catalog, and release tag. |
| `adapters/README.md` | stub | Each supported interchange format has an implemented adapter, tests, examples, and known limitations; future adapters are clearly marked. |
| `agents/consumer-agent-contract.md` | stub | Consumers retrieve only relevant records, cite IDs/sources, respect rights, treat source text as untrusted, and abstain on missing evidence. |
| `agents/consumer-answer.schema.json` | stub | Versioned schema is complete and validated against positive and negative answer fixtures. |
| `agents/instructions.md` | stub | Agent task protocol is bounded, testable, provenance-aware, and never authorizes silent merges or rights decisions. |
| `agents/review-checklist.md` | stub | Review covers factual support, identifiers, rights, consent, schema compatibility, tests, and downstream impact. |
| `agents/task-contract.schema.json` | stub | Task contract has schema metadata, negative tests, and a documented execution/review lifecycle. |
| `applications/README.md` | stub | Application index links to complete tracks and defines consumer boundaries. |
| `applications/education.md` | stub | Record type, rights/consent, labels, examples, and LLM-use rules are complete and tested. |
| `applications/games.md` | stub | Record type, rights/consent, labels, examples, and LLM-use rules are complete and tested. |
| `applications/music.md` | stub | Superseded/redirected to music-poetry track; rights, lyrics handling, and creative/evidence separation complete. |
| `applications/research.md` | stub | Research claims, source locations, disputed claims, and citation workflows are specified with examples. |
| `applications/speech-and-translation.md` | stub | Speech/translation rights, consent, model use, evaluation, and provenance rules are explicit and tested. |
| `catalog.json` | stub | Generated from real repository records; counts, hashes, paths, schema versions, and generated/stale check are reproducible. |
| `data/README.md` | stub | Dataset layout, licensing, formats, versions, exports, and non-ingestion rules match implementation. |
| `data/concepts/README.md` | stub | Concept schema, stable IDs, source/translation rules, and validated record locations are defined. |
| `data/grammar/README.md` | stub | Grammar records and source locations validate under the versioned grammar schema. |
| `data/lexicon/README.md` | stub | Every lexical entry has source ID and precise location plus checked rights; no unsourced entries. |
| `data/sources/README.md` | stub | Source records include verified metadata, source locations, rights, AI permissions, and review state. |
| `data/varieties/README.md` | stub | Language/variety record layout and identifier mapping rules are complete; no unsupported identifiers. |
| `docs/agent-handover.md` | stub | A new agent can continue safely from exact repository state, commands, tests, limitations, and stop conditions. |
| `docs/change-propagation.md` | stub | Dependencies and downstream impacts are represented and propagation is testable. |
| `docs/data-model.md` | stub | ID prefixes include lng-, var-, src-, lex-, grm-, evl-, con- and match actual schemas, constraints, and examples. |
| `docs/decisions/0001-framework-boundary.md` | complete | Framework/app boundary is recorded, rationale is clear, and changes require a superseding decision. |
| `docs/evidence-policy.md` | stub | Evidence labels, source-location requirements, rights, consent, disagreement, and retraction handling are operational. |
| `docs/framework-brief.md` | stub | Required verbatim intent appears; brief accurately describes current capabilities and limits. |
| `docs/language-relationships.md` | stub | Classification/lexifier/contact claims have sources and disputed positions remain explicit. |
| `docs/repository-audit.md` | stub | Audit covers every linked repository's files, security, rights, builds, provenance, and unresolved gaps with evidence. |
| `docs/standards-interoperability.md` | stub | Mappings to external standards are verified, versioned, scoped, and tested. |
| `docs/terminology.md` | stub | Terms distinguish real languages, varieties, classifications, convergence proposals, and fictional canon. |
| `docs/vision-and-scope.md` | stub | Required verbatim intent appears and scope, non-goals, and success criteria are aligned with actual implementation. |
| `evaluation/scoring-policy.md` | stub | Evaluation criteria, thresholds, abstention, held-out cases, rights, and release gates are testable. |
| `evaluation/test-cases/starter-cases.jsonl` | stub | Positive, negative, ambiguity, conflict, rights, and abstention cases are schema-validated and meaningful. |
| `llms.txt` | stub | Required verbatim intent appears; links are absolute, tracking-free, current, and useful to external agents. |
| `registry/projects.yaml` | stub | Each related project has verified canonical URL, role, relationship, audit status, and rights-aware reuse path. |
| `releases/release-process.md` | stub | Reproducible release process checks CI, versions, hashes, tag, release notes, and optional DOI approval. |
| `requirements-dev.txt` | complete | Validator dependencies are declared and CI installs them reproducibly enough for current checks. |
| `schemas/evaluation-case.schema.json` | stub | Has `$id`, schema version, format checking, complete fields, and passing positive/failing negative fixtures. |
| `schemas/grammar-rule.schema.json` | stub | Has `$id`, schema version, precise ID/reference constraints, source locations, and negative tests. |
| `schemas/language.schema.json` | stub | Has `$id`, schema version, kind, sourced substrate/adstrate and lexifier claims, conditional verified-ID requirements, and negative tests. |
| `schemas/lexical-entry.schema.json` | stub | Has `$id`, schema version, strict source ID/location and rights requirements, format validation, and negative tests. |
| `schemas/source-record.schema.json` | stub | Has `$id`, schema version, rights/AI permissions, URL/date format validation, and negative tests. |
| `schemas/variety.schema.json` | stub | Has `$id`, schema version, requested geographic/temporal/orthographic/speaker/parent/contact fields, conditional verified-ID requirements, and negative tests. |
| `scripts/validate_records.py` | stub | Validates every schema and record family, format constraints, negative fixtures, cross-record references, registry, catalog freshness, and demo tests with actionable errors. |
| `registry/resources.yaml` | planned | Contains only opened/verified resource cards with rights/AI-operation boundaries and tracking-free canonical URLs. |
| `data/resources/` | planned | Resource cards or normalized records validate against the resource-card schema; no copied third-party content without permission. |
| `schemas/resource-card.schema.json` | planned | Versioned schema covers resource identity, access, rights, AI operations, use mode, verification and contribution route. |
| `schemas/creative-work.schema.json` | planned | Versioned creative-work schema enforces work type, author/license, AI flags, language/variety, linked records, label and status. |
| `schemas/negative-tests/` | planned | Each schema has at least one intentionally invalid fixture; CI asserts each fixture is rejected. |
| `data/languages/` | planned | Candidate language records use provisional status unless sourced and reviewed; disputed classifications are marked and identifiers verified. |
| `data/varieties/*.jsonl` | planned | Candidate variety records have sourced classification, region, period, orthography, parent and contact claims; no unsupported estimates. |
| `applications/music-poetry/` | planned | README, creative-work schema use, rights, labelling, LLM-feed rules, and clearly owned example work are complete. |
| `applications/scripts/` | planned | README, record type, rights, labelling, LLM-feed rules, and permitted examples are complete. |
| `applications/localization/` | planned | README, record type, rights, labelling, LLM-feed rules, and localization evaluation are complete. |
| `SECURITY.md` | planned | Responsible vulnerability reporting and secret-exposure response are documented. |
| `SUPPORT.md` | planned | Public support routes and realistic maintainer capacity are stated. |
| `CODE_OF_CONDUCT.md` | planned | Enforceable respectful participation and reporting process is present. |
| `.github/ISSUE_TEMPLATE/resource-suggestion.yml` | planned | Structured resource proposal requests URL, coverage, terms, AI permissions and verification evidence. |
| `.github/ISSUE_TEMPLATE/correction.yml` | planned | Correction report captures record ID, source location, proposed fix and confidence. |
| `.github/ISSUE_TEMPLATE/bad-ai-answer.yml` | planned | Report captures query, answer, cited IDs, failure type and reproducible evidence without requiring private data. |
| `.github/PULL_REQUEST_TEMPLATE.md` | planned | Pull requests disclose evidence, rights, validation, impact and human-review requirements. |
| `docs/datasheet-draft.md` | planned | Hugging Face-ready datasheet documents scope, collection, provenance, licensing, consent, limitations and maintenance; not published externally. |
| `docs/sitemap.xml` | planned | Valid sitemap lists only deployed, canonical public pages. |
| `docs/robots.txt` | planned | Robots policy matches actual Pages deployment and does not claim controls it cannot enforce. |
| `docs/dataset-jsonld.html` | planned | Valid schema.org Dataset JSON-LD uses accurate metadata and absolute canonical URLs. |
| `scripts/generate_catalog.py` | planned | Deterministically generates counts and content hashes from validated records and fails CI on stale catalog. |
| `scripts/check_resource_links.py` | planned | Checks registry URLs on a schedule, records status/time, handles rate limits, and never rewrites verified metadata silently. |
| `exports/` JSONL export | planned | Reproducible rights-filtered JSONL exports include schema version, provenance and hashes. |
| `demo/retrieval/` | planned | Offline retrieval cites record/source IDs and abstains when evidence is insufficient; tests validate answers against consumer-answer schema. |
| Read-only MCP server | planned | Only implemented after offline demo passes; read-only, rights-aware, documented, and tested. |
| GitHub Pages deployment | planned | Public site builds from reviewed content with canonical URLs, sitemap and discoverability metadata. |
| Repository topics/description | stub | Description and topics accurately identify Creole languages, linguistic data, interoperability, provenance, and responsible AI. |
| Release tag and GitHub Release | planned | Versioned tag/release exists only after all release gates pass and published artifacts match validated commit. |
| Zenodo DOI | planned | Created only after explicit owner approval; DOI metadata and version match the tagged release. |

## Audit findings

- Latest observed workflow run: [38984185914](https://github.com/Francois-EF-WebOps/BabelGlobalKreole/actions/runs/38984185914), conclusion `success`, commit `f9ca6385cfa7682093672bef6bb774bf43c121b0`.
- Exact validator output from that run: `VALIDATION PASSED: 8 JSON Schemas checked; 6 JSONL records validated.`
- This is a baseline result, not proof that all requested acceptance criteria pass. The current validator does not validate resource cards, language/variety data, negative fixtures, catalog freshness, or cross-record references.
- Current schema files lack `$id` and `schema_version` fields. Language and variety schemas do not yet contain all requested fields or conditional verified-identifier requirements.
- No language or variety data records, external resource registry, creative-work schema, negative fixtures, offline retrieval demo, generated catalog, Pages deployment, or release tag were present in the baseline tree.
- The repository's default branch is `main`; the repository is public. GitHub Pages is not enabled at baseline.
- Security risk identified in sibling repositories remains open: client-side Vite substitutions for `GEMINI_API_KEY`/ `API_KEY` were observed in `Applied-Creole-Linguistics` and `Refuge`. This does not prove a real key was published. The owner should rotate any real key that may have been bundled into public client assets.

## Maintainer batch report — 2026-10-17

### Completed and verified in this batch

- Canonical intent paragraph inserted verbatim into `README.md`, `docs/vision-and-scope.md`, `llms.txt`, and `docs/framework-brief.md`.
- All 24 candidate language records are `record_status: draft`; no language identifiers, lexifier claims, substrate/adstrate claims, or lexical content were added from memory.
- All 24 variety candidates are `record_status: draft` and `retrieval_status: non-retrievable` because each duplicates its language-level label and has no source record. This status is explicit in `schemas/variety.schema.json` version 1.2.0.
- Added user-requested candidate labels for Rodriguan Creole, Agalega Creole, and Chagossian Creole at language and variety level; all remain draft and non-retrievable pending evidence.
- Validator now rejects any JSONL record marked `accepted` when `source_ids` is missing or empty.
- Consumer-agent contract explicitly prohibits citing records with missing or empty `source_ids` as evidence.
- Retried the official ISO 639-3 code-table URL and Gallica homepage. Both returned HTTP 403 in this browser and remain `unverified`; no codes or lexical material were imported.
- Opened the official GIDA CARE Principles page at `https://www.gida-global.org/careprinciples`. The resource card now uses that canonical URL and is marked `verified` for reachability/content only; site-wide reuse and AI permissions remain unknown. The official principles PDF identifies CC BY-NC-ND 4.0, which is not treated as blanket permission for adaptation or AI use.
- Refreshed `catalog.json` counts to 24 language records, 24 variety records, 14 resource cards, and the existing verified evaluation count. Catalog generation is still manual; deterministic generation and stale-catalog CI are not yet implemented.

### Not yet complete

- Language/variety labels have not been promoted to accepted linguistic records. Every classification and external identifier still requires a fetched, cited source record.
- The ISO 639-3 and Gallica URLs remain unverified due to HTTP 403; use only alternate official resources if their authority and contents can be verified.
- History mining has not run: the owner has not supplied `conversations.json`. No private conversation content has been committed.
- No seed lexical records were added under the strict link-first policy.
- No release was created. Final CI for the latest commit must be checked before reporting the batch as green.

