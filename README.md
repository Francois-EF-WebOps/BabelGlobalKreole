# Babel / Global (K)Creole

**Status:** Framework bootstrap — proposal, not a completed language standard  
**Version:** 0.1.0-draft

BabelGlobalKreole is a public, permanently maintained, evidence-grounded knowledge and interoperability layer for Creole languages. It starts from Mauritian Creole (Kreol Morisien), expands to French-lexifier Creoles of the Caribbean and Indian Ocean, then to Creoles with other European lexifiers, recording non-European contributions where documented. It links to existing scholarly and community resources instead of duplicating them. Creative applications (first music, lyrics, poetry; then scripts; then programming/localization) consume the framework and never define it. Creative output is always labelled separately from attested evidence.

Babel / Global (K)Creole is an evidence-led, machine-readable framework for documenting, comparing, designing, evaluating and responsibly applying Creole-related language knowledge. It is not a claim that all Creoles are one language, a replacement for existing Creoles, or a finished universal language.

## Start here

### People and community contributors
- [Vision and scope](docs/vision-and-scope.md): what the framework is and is not.
- [Terminology](docs/terminology.md): how this repository distinguishes languages, varieties, evidence and creative proposals.
- [Contributing guide](CONTRIBUTING.md): propose a correction or resource with evidence and rights information.
- [Governance](GOVERNANCE.md): current maintainer model and review safeguards.

### Researchers
- [Evidence policy](docs/evidence-policy.md): provenance, uncertainty, source locations, consent and rights.
- [Language relationships](docs/language-relationships.md): comparison boundaries and classification cautions.
- [Standards interoperability](docs/standards-interoperability.md): mappings and format strategy.
- [Data model](docs/data-model.md): record families, identifiers and invariants.
- [Machine-readable catalog](catalog.json): current record counts, paths and file hashes.
- [Cross-project registry](registry/projects.yaml): related projects and their roles.

### AI agents and LLM consumers
- [LLM discovery entry point](llms.txt): canonical links and consumer rules.
- [Root agent instructions](AGENTS.md): safe repository-editing rules.
- [Consumer-agent contract](agents/consumer-agent-contract.md): evidence citation, rights and abstention behaviour.
- [Consumer answer schema](agents/consumer-answer.schema.json): machine-readable answer contract.
- [Offline retrieval demo](demo/retrieval/README.md): local metadata retrieval and tested abstention behaviour.

### Developers and application builders
- [Framework brief](docs/framework-brief.md): concise architecture and limitations.
- [Schemas](schemas/): versioned record constraints and negative fixtures.
- [Adapter contract](adapters/README.md): interchange direction and current implementation limits.
- [Application tracks](applications/README.md): music/poetry, scripts, localization and other consumers.
- [Data licensing and AI-use policy](DATA-LICENSE.md): source-specific reuse boundaries.
- [Evaluation policy](evaluation/scoring-policy.md): regression and release gates.

### Citation and maintenance
- [Citation metadata](CITATION.cff): cite the repository and exact revision used.
- [Changelog](CHANGELOG.md): recorded changes and limitations.
- [Repository audit and artefact status](docs/artefact-status.md): verified state and remaining acceptance gates.

## Operating loop
`DISCOVER → RETRIEVE → CLASSIFY → PROPOSE → VALIDATE → REVIEW → RELEASE → PROPAGATE → MEASURE → MAINTAIN`

A model-generated answer is not itself evidence. Applications consume versioned framework data; they do not silently redefine the framework.

## Layers
- **Framework:** principles, terminology, governance, schemas, provenance, evaluation and change management.
- **Research:** sourced descriptions of real languages, varieties, contact histories and linguistic claims.
- **Design:** explicit proposals for convergence or constructed languages, separated from attested evidence.
- **Interoperability:** portable records and adapters for agents, LLMs, translation, speech, education, games, publishing and more.
- **Applications:** music, games, education, research, speech and translation. Applications are first-class but do not define the framework's boundary.

## Current limits
This is an initial specification, not a complete comparative corpus, validated global language, finished grammar or exhaustive lexicon. External APIs, agent loops and music-generation integrations are not claimed to be operational. Listing a source does not grant permission to reuse its content.

## Principles
Preserve source repositories and their histories; distinguish evidence from inference and invention; respect language communities and rights; keep real-language description separate from fictional canon; make uncertainty machine-readable; prefer portable formats; let automation propose and test; track downstream dependencies rather than silently rewriting outputs.

## Project operations
- [Security policy](SECURITY.md): report vulnerabilities without publishing secrets.
- [Support](SUPPORT.md): best-effort help and contribution routes.
- [Code of conduct](CODE_OF_CONDUCT.md): participation, privacy and community-consent expectations.
- [Dataset datasheet draft](docs/huggingface-datasheet.md): current coverage, provenance and limits; not a published dataset.
- [Documentation site deployment](docs/site-deployment.md): site output and the one-time Pages setting.
- [Read-only MCP adapter](mcp_server/README.md): optional local stdio tools for agent discovery.

## Contribute
Open an issue with scope and acceptance criteria, add provenance and rights information, use the relevant schema, add regression cases, run `python scripts/validate_records.py`, `python scripts/check_internal_links.py`, and `python scripts/no_placeholders_check.py`, and request review. See [CONTRIBUTING.md](CONTRIBUTING.md).
