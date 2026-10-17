# Applications

Applications consume BabelGlobalKreole; they do not define its scope. Each application must pin the framework version, schema version and record IDs used. Application contracts are not operational integrations.

## Priority order

1. [Music, lyrics and poetry](music-poetry/README.md)
2. [Film and series scripts](scripts/README.md)
3. [Programming and software localization](localization/README.md)
4. Other candidate domains below, only as evidence and capacity allow.

Third-party lyrics, scripts, dictionaries and corpora are excluded unless the specific source license permits the exact use. Creative output must be labelled `creative_coinage` or `application_canon` and must never be presented as attested linguistic evidence.

## Candidate domains and risk tiers

| Priority | Candidate domain | Risk tier | Current status and required gate |
|---|---|---|---|
| 1 | Music, lyrics, poetry and performance | Low to moderate; rights-sensitive | First application priority. Use owner-authored work or explicitly licensed sources; record attribution and separate creative coinage from attested forms. |
| 2 | Film/series scripts and dialogue | Moderate; rights- and representation-sensitive | Second priority. Use approved material only; register descriptions are optional free text and must be sourced when they make linguistic claims. |
| 3 | Programming, UI strings and software localization | Moderate; errors may affect access or transactions | Third priority. Require source-backed terminology, locale review and human testing before release. |
| 4 | Games, education, research and general publishing | Low to moderate depending on use | Later candidate applications; not operational integrations. Avoid claiming community endorsement or representing one register as universal. |
| 5 | Speech, transcription and translation | Moderate to high; privacy and consent-sensitive | Research only until rights, speaker consent, data minimization and evaluation are documented. |
| 6 | Finance, banking and remittances | High impact | Candidate domain only; not operational. Any consequential financial or regulatory translation requires qualified human review and testing. |
| 7 | Medical, clinical intake and public health | Safety-critical | Research only; not operational. Any clinical use requires qualified medical and language experts to validate every consequential translation. Never use this framework alone for diagnosis, triage or treatment. |
| 8 | Engineering, construction, maritime and industrial safety | Safety-critical | Research only; not operational. Human engineering/safety expert validation is mandatory; do not use generated translations as operating instructions. |
| 9 | Space, satellite telemetry and emergency alerts | Safety-critical | Research only; not operational. Human domain-expert validation, end-to-end testing and fail-safe design are mandatory before any real alerting or control use. |

Safety-critical means no production deployment, no autonomous decision-making, and no claim of operational readiness. A schema or example record does not constitute a validated technical vocabulary.

## Existing track documents

- [Music, lyrics and poetry](music-poetry/README.md)
- [Film and series scripts](scripts/README.md)
- [Programming and localization](localization/README.md)
- [Education](education.md)
- [Games](games.md)
- [Research](research.md)
- [Speech and translation](speech-and-translation.md)
