# Artefact status and acceptance register

**Audit date:** 2026-10-17  
**Inventory:** 84 tracked files on the default branch at this review point.  
**Latest verified review point before these documentation-only edits:** [CI run 38989618664](https://github.com/Francois-EF-WebOps/BabelGlobalKreole/actions/runs/38989618664), commit `5c6c91eb9e1a968fac7a6c128f81533c505fbb09`. That run passed 11 schemas, 70 JSONL records, 11 negative fixtures, six retrieval tests, data-integrity checks, and catalog freshness. Documentation changes made after that commit require their own CI run before being called verified.

## State meanings

- **complete** means the file meets its stated, bounded purpose; it does not mean the whole framework is complete.
- **partial** means the file contains real usable content but depends on evidence, deployment, review or implementation that is not yet available.
- **planned** means no file is being kept merely to represent future work; the work is recorded below.
- No record is promoted to accepted solely to make the catalog look complete.

## File-by-file status

| Path | State | Done criteria / current truth |
|---|---|---|
| `.github/workflows/validate.yml` | complete | Runs schema/record validation, negative fixtures, drafting-marker checks, retrieval tests and catalog freshness on push and pull request. |
| `.gitignore` | complete | Excludes secrets and private history-mining inputs/outputs from version control. |
| `AGENTS.md` | complete | Provides the agent entry point and links to detailed evidence, rights and review contracts. |
| `CHANGELOG.md` | partial | Records changes for draft 0.1.0; update before any release. |
| `CITATION.cff` | partial | Provides citation metadata; align version/date with an approved release before formal release. |
| `CONTRIBUTING.md` | complete | Explains evidence, rights, validation, review and contribution workflow. |
| `DATA-LICENSE.md` | complete | Separates repository code licensing from data/source rights and AI-use permissions. |
| `GOVERNANCE.md` | partial | States maintainer-led status and safeguards; community review and succession are not established. |
| `LICENSE` | complete | Provides repository code/documentation license; does not override source-specific rights. |
| `README.md` | partial | Contains verbatim intent and entry points; deployment and broader coverage remain incomplete. |
| `VERSION` | partial | Identifies the public draft version; not a tagged release. |
| `adapters/README.md` | partial | Documents adapter direction; no executable interchange adapters are implemented. |
| `agents/consumer-agent-contract.md` | complete | Defines citation, abstention, evidence-scope and rights behaviour for consuming agents. |
| `agents/consumer-answer.schema.json` | complete | Versioned machine-readable answer contract; covered by negative fixture and demo validation. |
| `agents/instructions.md` | complete | Defines repository editing and evidence safety constraints. |
| `agents/review-checklist.md` | complete | Provides human review checks for evidence, rights and schema changes. |
| `agents/task-contract.schema.json` | complete | Defines machine-readable agent task contract; negative fixture is checked. |
| `applications/README.md` | complete | Indexes application tracks and states that contracts are not operational integrations. |
| `applications/education.md` | partial | Describes a possible education consumer; no deployed integration. |
| `applications/games.md` | partial | Describes a possible game consumer; no deployed integration. |
| `applications/localization/README.md` | complete | Defines localization track, record types, rights, labelling and LLM limits. |
| `applications/music-poetry/README.md` | complete | Defines music/lyrics/poetry track, rights, labelling and LLM limits; no owner work published. |
| `applications/music.md` | complete | Compatibility entry point to the music application track. |
| `applications/research.md` | partial | Describes a research consumer; no deployed integration. |
| `applications/scripts/README.md` | complete | Defines script track, rights, labelling and LLM limits; no third-party script text included. |
| `applications/speech-and-translation.md` | partial | Defines a possible speech/translation consumer; no speech corpus or live service. |
| `catalog.json` | complete | Generated from JSONL files with counts and SHA-256 hashes; CI checks freshness. |
| `data/README.md` | complete | Explains data layout and provenance principles. |
| `data/concepts/README.md` | partial | Documents concept schema and evidence gate; no concept records yet. |
| `data/grammar/README.md` | partial | Documents grammar record requirements; no grammar records yet. |
| `data/languages/README.md` | complete | Explains language records, draft status and sourced identifiers. |
| `data/languages/languages.jsonl` | partial | 24 candidates are drafts; only Mauritian Creole currently has sourced metadata and a verified Glottocode. |
| `data/lexicon/README.md` | partial | Documents lexical record requirements; no lexical entries yet. |
| `data/resources/README.md` | complete | Explains resource cards and the difference between reachability and reuse permission. |
| `data/resources/resources.jsonl` | partial | 14 cards; ISO 639-3 and Gallica remain unverified; other statuses are scoped to checked pages/terms. |
| `data/sources/README.md` | complete | Explains source-record provenance and rights fields. |
| `data/sources/sources.jsonl` | partial | Two inspected source records for Mauritian Creole; no broad language coverage yet. |
| `data/varieties/README.md` | complete | Explains variety records and retrieval status. |
| `data/varieties/varieties.jsonl` | partial | 24 draft, non-retrievable records are explicit candidates duplicating language-level labels until a source describes a distinct variety. |
| `demo/retrieval/README.md` | complete | Documents local usage and limitations of the offline read-only demo. |
| `demo/retrieval/demo.py` | complete | Searches local JSONL metadata, requires resolvable dated source locations for evidence, validates answers and abstains on unsupported matches. |
| `docs/agent-handover.md` | complete | Explains safe handover and evidence boundaries. |
| `docs/artefact-status.md` | partial | This register tracks every current file and remaining dependencies; refresh after material changes. |
| `docs/change-propagation.md` | complete | Describes downstream impact and change propagation. |
| `docs/data-model.md` | complete | Defines stable IDs and now lists language, variety, source, lexical, grammar, evaluation, concept, resource and creative-work prefixes. |
| `docs/decisions/0001-framework-boundary.md` | complete | Records the framework/application boundary decision. |
| `docs/evidence-policy.md` | complete | Defines evidence labels, provenance and claim limits. |
| `docs/framework-brief.md` | partial | Contains verbatim intent and framework boundaries; full interoperability and coverage remain incomplete. |
| `docs/language-relationships.md` | partial | Defines cautious relationship modelling; actual relationships require sourced claims. |
| `docs/repository-audit.md` | partial | Records initial sibling-repository security findings; remediation PRs and full runtime audit remain open. |
| `docs/standards-interoperability.md` | partial | Maps standards and possible adapters; implemented exports and conformance tests remain incomplete. |
| `docs/terminology.md` | complete | Defines project terms and separates real-language evidence from creative canon. |
| `docs/vision-and-scope.md` | complete | Contains verbatim intent and boundaries. |
| `evaluation/scoring-policy.md` | complete | Defines evaluation dimensions and scoring cautions. |
| `evaluation/test-cases/starter-cases.jsonl` | partial | Six starter evaluation cases; coverage and held-out regression tests remain limited. |
| `llms.txt` | partial | Contains verbatim intent and absolute canonical links; no deployed Pages endpoint yet. |
| `registry/projects.yaml` | partial | Links known projects; several project locations remain explicitly unverified and are omitted rather than represented by null URLs. |
| `registry/resources.yaml` | complete | Indexes all 14 canonical resource cards in the JSONL registry. |
| `releases/release-process.md` | complete | Defines release steps; no tagged GitHub release or DOI has been created. |
| `requirements-dev.txt` | complete | Pins the JSON Schema validator dependency range used by CI. |
| `schemas/concept.schema.json` | complete | Adds the missing concept-record schema with stable IDs and version metadata. |
| `schemas/creative-work.schema.json` | complete | Defines labelled creative works and generation provenance; unknown optional fields can be omitted. |
| `schemas/evaluation-case.schema.json` | complete | Defines evaluation cases with a versioned schema. |
| `schemas/grammar-rule.schema.json` | complete | Defines sourced grammar rules; no grammar data published. |
| `schemas/language.schema.json` | complete | Defines language records, evidence-linked lexifier claims and conditional identifier verification. |
| `schemas/lexical-entry.schema.json` | complete | Defines lexical entries with provenance, rights and AI-use fields. |
| `schemas/resource-card.schema.json` | complete | Defines resource metadata and omits unknown license URLs instead of requiring null. |
| `schemas/source-record.schema.json` | complete | Defines source metadata, rights, review and AI-use fields. |
| `schemas/variety.schema.json` | complete | Defines scoped varieties and conditional verified identifiers; unknown optional values can be omitted. |
| `scripts/generate_catalog.py` | complete | Deterministically generates record counts and SHA-256 hashes from JSONL data; CI detects stale output. |
| `scripts/no_placeholders_check.py` | complete | Rejects zero-byte tracked files, drafting markers, empty strings/nulls in data records and empty arrays except draft source_ids. |
| `scripts/validate_records.py` | complete | Checks all schemas, JSONL records, format constraints, negative fixtures and accepted-record source resolution. |
| `tests/negative/concept.schema.json.invalid.json` | complete | Intentionally invalid concept instance must be rejected. |
| `tests/negative/consumer-answer.schema.json.invalid.json` | complete | Intentionally invalid consumer answer must be rejected. |
| `tests/negative/creative-work.schema.json.invalid.json` | complete | Intentionally invalid creative-work instance must be rejected. |
| `tests/negative/evaluation-case.schema.json.invalid.json` | complete | Intentionally invalid evaluation case must be rejected. |
| `tests/negative/grammar-rule.schema.json.invalid.json` | complete | Intentionally invalid grammar-rule instance must be rejected. |
| `tests/negative/language.schema.json.invalid.json` | complete | Intentionally invalid language instance must be rejected. |
| `tests/negative/lexical-entry.schema.json.invalid.json` | complete | Intentionally invalid lexical-entry instance must be rejected. |
| `tests/negative/resource-card.schema.json.invalid.json` | complete | Intentionally invalid resource-card instance must be rejected. |
| `tests/negative/source-record.schema.json.invalid.json` | complete | Intentionally invalid source-record instance must be rejected. |
| `tests/negative/task-contract.schema.json.invalid.json` | complete | Intentionally invalid task-contract instance must be rejected. |
| `tests/negative/variety.schema.json.invalid.json` | complete | Intentionally invalid variety instance must be rejected. |
| `tests/retrieval/test_demo.py` | complete | Tests supported citation, abstention for draft/unsourced records and missing source locations, unknown queries, variety-ID resolution, and lexical-entry ID lookup. |

## Verified data snapshot

- Language candidates: 24, all `draft`.
- Variety candidates: 24, all `draft` and `non-retrievable` because they duplicate language-level labels until sources establish distinct varieties.
- Source records: 2, for Glottolog's Morisyen entry and APiCS's Mauritian Creole dataset.
- Verified external identifiers: Glottocode `mori1278` for the Mauritian Creole candidate. No ISO 639-3 identifier is recorded as verified in Babel yet.
- Resource cards: 14. ISO 639-3 and Gallica remain `unverified` after HTTP 403 responses. CARE's official page was reachable, but reachability does not grant reuse or AI permissions.
- Lexical entries: 0. Grammar rules: 0. Concept records: 0. No third-party lyrics, scripts or dictionary contents were copied.
- Creative work from owner history: none imported. No `conversations.json` was supplied for private mining or batch approval.

## Remaining work, in dependency order

1. **Evidence coverage:** source and verify the remaining language candidates; only create a variety when a fetched source describes a distinct variety. Include Rodriguan, Agalega and Chagossian claims only when supported by sources.
2. **Resource verification:** retry official ISO 639-3 and Gallica routes through accessible official pages or authoritative downloadable tables; preserve their unverified status until confirmed. Maintain a repeatable link-check report.
3. **Data usefulness:** add small sourced lexical/grammar records only after source locations, exact reuse permissions and relevant consent are established. Strict link-first remains the default.
4. **Private-history review:** after the owner supplies `conversations.json`, mine it only into git-ignored candidates; show batches for approval. Assistant-authored claims stay quarantined until independently sourced.
5. **Discoverability:** GitHub Pages is not enabled. Missing deployment artefacts include `robots.txt`, `sitemap.xml`, a Dataset JSON-LD landing page, issue templates, `SECURITY.md`, `SUPPORT.md`, and `CODE_OF_CONDUCT.md`. Add and test these before enabling public Pages.
6. **Automation:** the offline retrieval demo is tested; a scheduled link checker and read-only MCP server are not deployed. Build the MCP server only after the demo's evidence/rights behaviour remains stable.
7. **Sibling-repository security:** client-side Vite key substitution was observed in Applied-Creole-Linguistics and Refuge. This is a configuration exposure risk, not proof that a live key was published. Security remediation must go through PRs; do not rotate keys or publish secrets without owner direction.
8. **Release:** the project remains `0.1.0-draft`. No release tag, GitHub Release or DOI exists. Create a release only after the current commit's CI is green and the release contents/metadata are reviewed.

## Hard acceptance gates

- Every schema has a stable HTTPS `$id`, `schema_version`, and a negative fixture that CI proves invalid.
- Every accepted record has at least one source ID resolving to a source record with a canonical URL, access date and precise source location.
- Every non-draft data record with a `source_ids` field has a non-empty list; unknown optional values are omitted rather than padded.
- Consumer agents never cite records with empty/missing/unresolved source IDs as evidence and abstain when evidence is missing.
- Resource reachability, source rights, AI-use permissions and community consent remain separate statuses.
- Catalog counts and hashes are generated from real JSONL files and are checked for freshness in CI.
- The final release gate is a green CI run on the exact release commit; earlier passing runs do not certify later changes.
