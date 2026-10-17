# Artefact status and acceptance register

**Audit date:** 2026-10-17  
**Inventory:** 108 tracked files on the default branch at this review point.  
**Latest verified validation run before this register update:** [CI run 38990985804](https://github.com/Francois-EF-WebOps/BabelGlobalKreole/actions/runs/38990985804), commit `d330722b70be1c22187c3966eac35e87e3f21c79`. That run passed 11 schemas, 70 JSONL records, 11 negative fixtures, 44 local Markdown links, 20 tests, data-integrity checks, and catalog freshness.

## State meanings

- **complete** means the file meets its stated, bounded purpose; it does not mean the whole framework is complete.
- **partial** means the file contains real usable content but depends on evidence, deployment, review or implementation that is not yet available.
- **planned** means no file is being kept merely to represent future work; the work is recorded below.
- No record is promoted to accepted solely to make the catalog look complete.

## File-by-file status

| Path | State | Done criteria / current truth |
|---|---|---|
| `.github/ISSUE_TEMPLATE/bad-ai-answer.yml` | complete | Collects the question, problematic answer, cited IDs, failure type and evidence without requesting private material. |
| `.github/ISSUE_TEMPLATE/correction.yml` | complete | Collects a record/path, proposed correction, source URL, precise location and rights acknowledgement. |
| `.github/ISSUE_TEMPLATE/resource-suggestion.yml` | complete | Collects canonical resource URL, coverage, license/AI-use evidence and intended use. |
| `.github/workflows/mcp.yml` | complete | Installs the optional MCP SDK and tests evidence/rights gates plus the stdio tool handshake. |
| `.github/workflows/pages.yml` | partial | Builds a site preview on push; deployment is gated until the owner enables Pages and sets `PAGES_ENABLED=true`. |
| `.github/workflows/resource-links.yml` | complete | Runs a weekly/manual report-only link check and uploads its report; it does not rewrite registry verification. |
| `.github/workflows/validate.yml` | complete | Runs schema/record validation, negative fixtures, data-integrity checks, retrieval tests and catalog freshness on push and pull request. |
| `.gitignore` | complete | Excludes secrets and private history-mining inputs/outputs from version control. |
| `AGENTS.md` | complete | Provides the agent entry point and links to detailed evidence, rights and review contracts. |
| `CHANGELOG.md` | partial | Records changes for draft 0.1.0; update before any release. |
| `CITATION.cff` | partial | Provides citation metadata; align version/date with an approved release before formal release. |
| `CODE_OF_CONDUCT.md` | complete | Sets respectful participation, privacy, consent and dispute expectations without claiming community mandate. |
| `CONTRIBUTING.md` | complete | Explains evidence, rights, validation, review and contribution workflow. |
| `DATA-LICENSE.md` | complete | Separates repository code licensing from data/source rights and AI-use permissions. |
| `GOVERNANCE.md` | partial | States maintainer-led status and safeguards; community review and succession are not established. |
| `LICENSE` | complete | Provides repository code/documentation license; does not override source-specific rights. |
| `README.md` | partial | Contains verbatim intent and entry points; deployment and broader coverage remain incomplete. |
| `SECURITY.md` | complete | Defines private vulnerability reporting guidance and credential handling; no secret is included. |
| `SUPPORT.md` | complete | Defines best-effort support and issue-form routes without a response-time promise. |
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
| `docs/huggingface-datasheet.md` | partial | Describes current snapshot and limits for review; not a published dataset card. |
| `docs/framework-brief.md` | partial | Contains verbatim intent and framework boundaries; full interoperability and coverage remain incomplete. |
| `docs/language-relationships.md` | partial | Defines cautious relationship modelling; actual relationships require sourced claims. |
| `docs/repository-audit.md` | partial | Records sibling-repository findings and open security PRs; full build/runtime audit remains open. |
| `docs/site-deployment.md` | complete | Documents the exact one-time Pages settings needed; the site is not yet public. |
| `docs/standards-interoperability.md` | partial | Maps standards and possible adapters; implemented exports and conformance tests remain incomplete. |
| `docs/terminology.md` | complete | Defines project terms and separates real-language evidence from creative canon. |
| `docs/vision-and-scope.md` | complete | Contains verbatim intent and boundaries. |
| `evaluation/scoring-policy.md` | complete | Defines evaluation dimensions and scoring cautions. |
| `evaluation/test-cases/starter-cases.jsonl` | partial | Six starter evaluation cases; coverage and held-out regression tests remain limited. |
| `llms.txt` | partial | Contains verbatim intent and absolute canonical links; no deployed Pages endpoint yet. |
| `registry/projects.yaml` | partial | Links known projects; several project locations remain explicitly unverified and are omitted rather than represented by null URLs. |
| `registry/resources.yaml` | complete | Indexes all 14 canonical resource cards in the JSONL registry. |
| `releases/release-process.md` | complete | Defines release steps; no tagged GitHub release or DOI has been created. |
| `mcp_server/README.md` | complete | Documents local stdio setup, read-only tools, evidence gates and current limitations. |
| `mcp_server/registry.py` | complete | Implements local search/get/catalog, source resolution, abstention and retrieval-rights filtering. |
| `mcp_server/server.py` | complete | Exposes three read-only MCP tools; no write or network-fetch tools. |
| `requirements-dev.txt` | complete | Pins the JSON Schema validator dependency range used by CI. |
| `requirements-mcp.txt` | complete | Keeps the official MCP SDK optional for users who want the stdio adapter. |
| `schemas/concept.schema.json` | complete | Adds the missing concept-record schema with stable IDs and version metadata. |
| `schemas/creative-work.schema.json` | complete | Defines labelled creative works and generation provenance; unknown optional fields can be omitted. |
| `schemas/evaluation-case.schema.json` | complete | Defines evaluation cases with a versioned schema. |
| `schemas/grammar-rule.schema.json` | complete | Defines sourced grammar rules with explicit AI-use permissions; no grammar data published. |
| `schemas/language.schema.json` | complete | Defines language records, evidence-linked lexifier claims and conditional identifier verification. |
| `schemas/lexical-entry.schema.json` | complete | Defines lexical entries with provenance, rights and AI-use fields. |
| `schemas/resource-card.schema.json` | complete | Defines resource metadata and omits unknown license URLs instead of requiring null. |
| `schemas/source-record.schema.json` | complete | Defines source metadata, rights, review and AI-use fields. |
| `schemas/variety.schema.json` | complete | Defines scoped varieties and conditional verified identifiers; unknown optional values can be omitted. |
| `scripts/build_site.py` | complete | Generates a static landing page, Dataset JSON-LD, absolute sitemap, robots.txt, catalog and llms.txt from real repository metadata. |
| `scripts/check_internal_links.py` | complete | Checks local Markdown link targets and fails if none are detected. |
| `scripts/check_resource_links.py` | complete | Checks resource URLs and writes a report without changing rights or verification status. |
| `scripts/generate_catalog.py` | complete | Deterministically generates record counts and SHA-256 hashes from JSONL data; CI detects stale output. |
| `scripts/no_placeholders_check.py` | complete | Rejects zero-byte tracked files, drafting markers, empty strings/nulls in data records and empty arrays except draft source_ids. |
| `scripts/record_integrity.py` | complete | Provides tested canonical-ID extraction and duplicate-ID detection, prioritizing each record's own ID over parent references. |
| `scripts/validate_records.py` | complete | Checks all schemas, JSONL records, format constraints, negative fixtures, duplicate IDs and accepted-record source resolution. |
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
| `tests/retrieval/test_demo.py` | complete | Tests supported citation, abstention for draft/unsourced data, unknown queries and variety-ID resolution. |
| `tests/retrieval/test_resource_links.py` | complete | Tests that URL tracking parameters are removed and stable URL parts are preserved. |
| `tests/retrieval/test_mcp_registry.py` | complete | Tests MCP abstention, source resolution, retrieval permission filtering and evidence ranking. |
| `tests/retrieval/test_record_integrity.py` | complete | Tests canonical ID selection and duplicate-ID detection. |
| `tests/mcp/test_mcp_server.py` | complete | Launches the MCP server over stdio and verifies only the three read-only tools are exposed. |
| `tests/retrieval/test_site_build.py` | complete | Tests generated Dataset JSON-LD, absolute sitemap, robots rules and catalog values. Tests that URL tracking parameters are removed and stable URL parts are preserved. | Tests supported citation, abstention for draft/unsourced records and missing source locations, unknown queries, variety-ID resolution, and lexical-entry ID lookup. |

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
2. **Resource verification:** ISO 639-3 returned HTTP 200 from the automated runner but HTTP 403 in browser retrieval; its content and terms remain unverified, so the card stays unverified. Gallica returned HTTP 403 in both checks and remains unverified. CARE's official page returned HTTP 200 and was inspected; its link does not grant reuse or AI permission.
3. **Data usefulness:** add small sourced lexical/grammar records only after source locations, exact reuse permissions and relevant consent are established. Strict link-first remains the default.
4. **Private-history review:** after the owner supplies `conversations.json`, mine it only into git-ignored candidates; show batches for approval. Assistant-authored claims stay quarantined until independently sourced.
5. **Discoverability:** a static landing-page builder now generates `robots.txt`, `sitemap.xml`, and Schema.org Dataset JSON-LD. The preview workflow passes. GitHub Pages is not live because the available GitHub connection cannot change repository settings or supply the non-default token required to enable Pages. The owner must select **Settings → Pages → GitHub Actions** and set repository variable `PAGES_ENABLED=true`. Repository topics also remain unset because the connection exposes no topic-edit operation.
6. **Automation:** the offline retrieval demo, catalog freshness check, local Markdown link checker, no-empty-data check, and report-only scheduled link checker are implemented. [Resource-link run 38990223532](https://github.com/Francois-EF-WebOps/BabelGlobalKreole/actions/runs/38990223532) checked all 14 URLs: 12 returned HTTP 200 from the runner; Gallica and HathiTrust returned HTTP 403 to the automated request. HathiTrust was reachable through browser retrieval, so this is not treated as proof that the resource is offline. The link report does not change rights or verification claims. A read-only local stdio MCP adapter is implemented and smoke-tested; it is not deployed as a network service.
7. **Sibling-repository security:** [Applied-Creole-Linguistics PR #2](https://github.com/Francois-EF-WebOps/Applied-Creole-Linguistics/pull/2) removes unused key injection; [Refuge PR #2](https://github.com/Francois-EF-WebOps/Refuge/pull/2) disables browser-side Gemini calls until a proxy exists. Both remain open and unmerged; neither repo has CI. No key was rotated. If a real key was ever built into a public bundle, the owner should rotate it directly in the provider console.
8. **Release:** the project remains `0.1.0-draft`. No release tag, GitHub Release or DOI exists. Create a release only after the current commit's CI is green and the release contents/metadata are reviewed.

## Hard acceptance gates

- Every schema has a stable HTTPS `$id`, `schema_version`, and a negative fixture that CI proves invalid.
- Every accepted record has at least one source ID resolving to a source record with a canonical URL, access date and precise source location; duplicate record IDs fail validation.
- Every non-draft data record with a `source_ids` field has a non-empty list; unknown optional values are omitted rather than padded.
- Consumer agents never cite records with empty/missing/unresolved source IDs as evidence and abstain when evidence is missing.
- Resource reachability, source rights, AI-use permissions and community consent remain separate statuses.
- Catalog counts and hashes are generated from real JSONL files and are checked for freshness in CI.
- The final release gate is a green CI run on the exact release commit; earlier passing runs do not certify later changes.
