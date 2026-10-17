# Babel / Global (K)Creole

**Status:** Framework bootstrap — proposal, not a completed language standard  
**Version:** 0.1.0-draft

BabelGlobalKreole is a public, permanently maintained, evidence-grounded knowledge and interoperability layer for Creole languages. It starts from Mauritian Creole (Kreol Morisien), expands to French-lexifier Creoles of the Caribbean and Indian Ocean, then to Creoles with other European lexifiers, recording non-European contributions where documented. It links to existing scholarly and community resources instead of duplicating them. Creative applications (first music, lyrics, poetry; then scripts; then programming/localization) consume the framework and never define it. Creative output is always labelled separately from attested evidence.

Babel / Global (K)Creole is an evidence-led, machine-readable framework for documenting, comparing, designing, evaluating and responsibly applying Creole-related language knowledge. It is not a claim that all Creoles are one language, a replacement for existing Creoles, or a finished universal language.

## Start here
- [AI/LLM discovery](llms.txt) and [agent entry point](AGENTS.md)
- [Framework brief](docs/framework-brief.md)
- [Consumer-agent contract](agents/consumer-agent-contract.md) and [answer schema](agents/consumer-answer.schema.json)
- [Standards interoperability roadmap](docs/standards-interoperability.md)
- [Data licensing and AI-use policy](DATA-LICENSE.md)
- [Machine-readable catalog](catalog.json)
- [Citation metadata](CITATION.cff)
- [Vision and scope](docs/vision-and-scope.md)
- [Terminology](docs/terminology.md)
- [Language relationships](docs/language-relationships.md)
- [Evidence, provenance and rights](docs/evidence-policy.md)
- [Governance](GOVERNANCE.md)
- [Agent operating contract](agents/instructions.md)
- [Data model](docs/data-model.md)
- [Evaluation gates](evaluation/scoring-policy.md)
- [Integration contract](adapters/README.md)
- [Cross-project registry](registry/projects.yaml)
- [Repository audit](docs/repository-audit.md)

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

## Contribute
Open an issue with scope and acceptance criteria, add provenance and rights information, use the relevant schema, add regression cases, run `python scripts/validate_records.py`, and request review. See [CONTRIBUTING.md](CONTRIBUTING.md).
