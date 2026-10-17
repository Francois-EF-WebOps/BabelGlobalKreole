# Language coverage and scope register

This document is the non-data register for candidates that are not yet suitable as language or variety records. The machine-readable core data contains only catalogue entries whose identifiers and source metadata were inspected. A name in this table is not an accepted classification.

## Core records excluded from data pending better source resolution

| Candidate | Current disposition | Evidence checked / next gate |
|---|---|---|
| Dominican Kwéyòl | Coverage candidate; not a separate language record in this snapshot | Glottolog's bibliographic records describe Dominican Creole in relation to Saint Lucian Creole French; no distinct language-level Glottolog record was verified in this pass. Compare community and scholarly sources before deciding whether to model it as a variety. |
| Rodriguan Creole | Coverage candidate only | APiCS's Mauritian survey discusses Rodrigues as a dependency, and Glottolog bibliography includes work titled *Pour une étude du créole rodriguais*. That does not by itself establish a distinct language record or justify a code. |
| Agalega Creole | Coverage candidate only | APiCS's Mauritian survey names Agalega as a dependency; no distinct language-level record was verified. Do not infer a separate variety solely from geography. |
| Chagossian Creole | Coverage candidate only | No dedicated Glottolog language page was verified in this pass. Require a source describing the language/variety before creating a record. |
| Papiamentu / Papiamento | Sourced extension candidate; lexifier analysis disputed | Glottolog and APiCS pages were inspected. APiCS describes multiple major lexifiers (Afro-Portuguese, Spanish and Dutch); Babel does not select one as the single lexifier. Keep it outside the current core inventory until scope and modelling are reviewed. |

## Scope extensions beyond the current European-lexifier focus

| Candidate | Disposition | Evidence / boundary |
|---|---|---|
| Michif | Extension of scope: mixed language with Cree and French components | Glottolog page inspected; its identifier and ISO code are in a source record, not asserted as a core language record. Do not force it into a European-lexifier-only classification. |
| Nubi | Extension of scope: Arabic-lexifier contact language | Glottolog page inspected; its identifier and ISO code are in a source record, not asserted as a core language record. It is outside the current core scope. |
| Other mixed or non-European-lexifier cases | Individually reviewed extensions | Add only after a fetched catalogue page and relevant scholarly/community evidence support the exact classification. Do not generalize from geography or a contact language. |

## Source records for verification

- Glottolog pages: [Papiamento](https://glottolog.org/resource/languoid/id/papi1253), [Michif](https://glottolog.org/resource/languoid/id/mich1243), [Nubi](https://glottolog.org/resource/languoid/id/nubi1253).
- APiCS: [Papiamentu dataset 47](https://apics-online.info/contributions/47), [Mauritian Creole survey](https://apics-online.info/surveys/55).
- The identifiers in this document are not a substitute for machine-readable language records. The roadmap must not display ISO or Glottocode values unless those values are verified in `data/languages/` or `data/varieties/`.


## APiCS regional datasets that must not be flattened

| Catalogue label | APiCS datasets inspected | Modelling note |
|---|---|---|
| Kabuverdianu / Cape Verdean Creole | [Santiago (30)](https://apics-online.info/contributions/30), [Brava (31)](https://apics-online.info/contributions/31), [São Vicente (32)](https://apics-online.info/contributions/32) | The core language record links all three sources; the island datasets remain distinct and do not imply one uniform orthography or grammar. |
| Chabacano / Chavacano | [Cavite (45)](https://apics-online.info/contributions/45), [Ternate (44)](https://apics-online.info/contributions/44), [Zamboanga (46)](https://apics-online.info/contributions/46) | The core record links these regional datasets, but no single dataset is treated as exhaustive of every Chabacano variety. Separate variety records require an explicit parent/identity mapping decision. |
| Palenquero | [Palenquero (48)](https://apics-online.info/contributions/48) | The APiCS dataset is linked to the catalogue record; claims about substrate influence remain limited to the source's stated evidence. |

The core data contains only identifiers confirmed on inspected Glottolog pages. This coverage register intentionally omits ISO and Glottocode columns for candidates without core language/variety records.
