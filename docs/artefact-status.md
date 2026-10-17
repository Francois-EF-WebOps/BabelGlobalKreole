# Artefact status and acceptance register

**Audit date:** 2026-10-17  
**Inventory:** 113 tracked files on the default branch at this review point.  
**Latest verified validation run before this register refresh:** [CI run 38994680082](https://github.com/Francois-EF-WebOps/BabelGlobalKreole/actions/runs/38994680082), commit `a87e3b0b388ec7524507a7fee65ae77b6e59be94`. It passed 11 schemas, 95 JSONL records, 11 negative fixtures, 21 tests, internal link checks, source-rights resolution, data-integrity checks, and catalog freshness.

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
| `.github/workflows/pages.yml` | partial | Preview build passes; latest checked deployment job was skipped. The live site is not verified. |
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
| `applications/README.md` | complete | Preserves priority order and provides a risk-tiered candidate-domain table; safety-critical domains are explicitly non-operational. |
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
| `data/concepts/concepts.jsonl` | complete | One organizing concept record; concept definitions do not substitute for linguistic evidence. |
| `data/concepts/README.md` | complete | Documents the concept schema and evidence gate; one organizing concept is present. |
| `data/grammar/README.md` | complete | Documents the sourced, scoped grammar-claim policy; three grammar claims are present across two JSONL files. |
| `data/grammar/grammar.jsonl` | complete | Two APiCS-linked Mauritian Creole grammar claims, paraphrased without reproducing examples. |
| `data/grammar/rules.jsonl` | complete | One sourced Mauritian Creole nominal-plurality grammar claim. |
| `data/languages/README.md` | complete | Explains accepted catalogue records, identifier provenance and the coverage register. |
| `data/languages/languages.jsonl` | partial | 19 accepted catalogue records have inspected Glottolog identifiers and source records; unverified candidates remain in `docs/language-coverage.md`. |
| `data/lexicon/README.md` | complete | Documents provenance and rights requirements; one source-backed Mauritian Creole lexical entry is present. |
| `data/lexicon/entries.jsonl` | partial | One APiCS-attributed lexical record for the Mauritian Creole pluralizer; AI training remains unknown. |
| `data/resources/README.md` | complete | Explains resource cards and the difference between reachability and reuse permission. |
| `data/resources/resources.jsonl` | partial | 14 cards; ISO 639-3 and Gallica remain unverified; other statuses are scoped to checked pages/terms. |
| `data/sources/README.md` | complete | Explains source-record provenance and rights fields. |
| `data/sources/sources.jsonl` | partial | 50 source records cover catalogue identifiers and inspected APiCS resources; link-only sources do not imply permission for training or speech generation. |
| `data/varieties/README.md` | complete | Explains variety records and retrieval status. |
| `data/varieties/varieties.jsonl` | partial | One accepted, sourced Martinican Creole variety record; no unsourced 24-record duplicate set remains. |
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
| `docs/language-coverage.md` | partial | Records unresolved candidates and scope extensions outside machine-readable accepted data. |
| `docs/repository-audit.md` | partial | Records sibling-repository findings and open security PRs; full build/runtime audit remains open. |
| `docs/site-deployment.md` | partial | Records the latest skipped deployment, the proposed URL verification failure mode, and the exact post-deploy URL checks; the site is not verified live. |
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
| `schemas/grammar-rule.schema.json` | complete | Defines sourced grammar claims with explicit AI-use permissions. |
| `schemas/language.schema.json` | complete | Defines language records, evidence-linked lexifier claims and conditional identifier verification. |
| `schemas/lexical-entry.schema.json` | complete | Defines lexical entries with provenance, rights and AI-use fields; register is optional source-backed free text, not an enum. |
| `schemas/resource-card.schema.json` | complete | Defines resource metadata and omits unknown license URLs instead of requiring null. |
| `schemas/source-record.schema.json` | complete | Defines source metadata, rights, review and AI-use fields. |
| `schemas/variety.schema.json` | complete | Defines scoped varieties and conditional verified identifiers; unknown optional values can be omitted. |
| `scripts/build_site.py` | complete | Generates a static landing page, Dataset JSON-LD, absolute sitemap, robots.txt, catalog and llms.txt from real repository metadata. |
| `scripts/check_internal_links.py` | complete | Checks local Markdown link targets and fails if none are detected. |
| `scripts/check_resource_links.py` | complete | Checks resource URLs and writes a report without changing rights or verification status. |
| `scripts/generate_catalog.py` | complete | Deterministically generates record counts and SHA-256 hashes, including concept records, from JSONL data; CI detects stale output. |
| `scripts/no_placeholders_check.py` | complete | Rejects zero-byte tracked files, drafting markers, URL tracking parameters, null/empty data values and empty arrays except draft source_ids. |
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
| `tests/retrieval/test_site_build.py` | complete | Tests generated Dataset JSON-LD, absolute sitemap, robots rules and current catalog values. |

## Verified data snapshot

- Language records: 19 accepted catalogue entries with Glottolog identifiers and source IDs. Candidate names not supported as distinct records remain in `docs/language-coverage.md`.
- Variety records: 1 accepted Martinican Creole record supported by a Glottolog dialect page and APiCS dataset. The former set of 24 unsupported variety entries is not present.
- Source records: 50. Source records include Glottolog catalogue pages and inspected APiCS resources; AI training, speech generation and synthetic-data permissions remain unknown unless individually verified.
- Lexical entries: 1 (`ban`, a Mauritian Creole pluralizer, attributed to APiCS). No dictionary or corpus was copied.
- Grammar claims: 3 across `data/grammar/grammar.jsonl` and `data/grammar/rules.jsonl`, including nominal plurality, preverbal tense/aspect/mood marking and the position of standard negation.
- Concept records: 1 organizing concept for nominal plurality.
- Resource cards: 14; unresolved reachability and rights limits remain recorded per resource.
- The current catalog generator should record 95 JSONL records across data and evaluation files after the latest six APiCS source records; CI must verify catalog counts and hashes on the final commit.
- Creative work from owner history: none imported. No `conversations.json` was supplied for private mining or batch approval.

## Remaining work, in dependency order

1. **Language evidence coverage:** the current 19 accepted catalogue records are sourced, but coverage is not complete. Dominican Kwéyòl, Rodrigues, Agalega and Chagossian claims remain in the non-data coverage register pending direct evidence. Keep Papiamento's lexifier attribution disputed; Michif and Nubi remain scope extensions, not core European-lexifier records.
2. **APiCS coverage:** source pages have been inspected for selected languages. Fetch and record the canonical APiCS page, date and precise location for every candidate where an APiCS entry exists before claiming APiCS coverage is complete.
3. **Data quality:** keep the one lexical entry and three grammar claims link-first and narrowly scoped. Do not add copied dictionary entries or third-party lyrics/scripts without source-specific rights review. AI training, speech and synthetic-data flags remain unknown where not explicitly verified.
4. **Discoverability and Pages:** the static site preview builds, but the latest checked workflow's deploy job was skipped. The site URL and generated `sitemap.xml`, `robots.txt`, `llms.txt`, `CITATION.cff` and Dataset JSON-LD have not been verified against a live deployment. The owner must ensure Pages source is GitHub Actions and repository variable `PAGES_ENABLED=true`, then rerun the workflow. Do not add a live URL to README until deployment succeeds and URL checks pass.
5. **Automation:** schema/record validation, negative fixtures, internal Markdown links, record integrity, offline retrieval, catalog freshness and the report-only resource link checker are implemented. The read-only stdio MCP adapter is local, not deployed as a network service.
6. **Sibling-repository security:** [Applied-Creole-Linguistics PR #2](https://github.com/Francois-EF-WebOps/Applied-Creole-Linguistics/pull/2) and [Refuge PR #2](https://github.com/Francois-EF-WebOps/Refuge/pull/2) remain owner-review items. No key rotation is confirmed. If a real key was ever built into a public bundle, rotate it directly in the provider console.
7. **Private-history review:** no `conversations.json` was supplied. A private history import must remain local/git-ignored and every extracted candidate must be independently sourced and owner-approved.
8. **Release:** project remains `0.1.0-draft`; no release tag, GitHub Release or DOI is confirmed. Release only after current CI is green and the owner approves the release metadata.

## Hard acceptance gates

- Every schema has a stable HTTPS `$id`, `schema_version`, and a negative fixture that CI proves invalid.
- Every accepted record has at least one source ID resolving to a source record with a canonical URL, access date and precise source location; duplicate record IDs fail validation.
- Every non-draft data record with a `source_ids` field has a non-empty list; unknown optional values are omitted rather than padded.
- Consumer agents never cite records with empty/missing/unresolved source IDs as evidence and abstain when evidence is missing.
- Resource reachability, source rights, AI-use permissions and community consent remain separate statuses.
- Catalog counts and hashes are generated from real JSONL files and are checked for freshness in CI.
- The final release gate is a green CI run on the exact release commit; earlier passing runs do not certify later changes.
