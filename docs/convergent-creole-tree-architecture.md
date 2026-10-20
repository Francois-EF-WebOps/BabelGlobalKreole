# Convergent Creole Tree Architecture

**Status:** Proposed architecture; not a validated language standard  
**Version:** 0.1.0-draft  
**Purpose:** Define how BabelGlobalKreole supports both a practical cross-Creole bridge and the possible emergence of a shared convergent language without erasing existing languages.

## 1. Vision

The tree metaphor describes a system in which distinct Creole languages and varieties remain living branches while shared knowledge, interoperability and community-tested conventions grow between them. A shared trunk is an outcome of documented comparison, deliberate design where needed, testing and sustained use—not a claim that all Creoles descend from one language or are interchangeable.

The target has two horizons:

1. **Bridge first:** help speakers understand, compare, learn from and communicate across varieties using evidence-backed mappings, explanations and tools.
2. **Potential shared language:** support a proposed common language only through transparent design, speaker evaluation, revision and voluntary adoption.

The bridge can be useful even if no single common language is ultimately adopted.

## 2. Non-negotiable distinctions

Every record and application must distinguish:

- **Attested usage:** a form documented in a specific language/variety, source, place, time, meaning and context.
- **Scholarly analysis:** an interpretation attributed to a source or researcher.
- **Comparative observation:** a documented similarity or difference; not by itself evidence of ancestry.
- **Bridge mapping:** an explanation or mapping that helps users understand across varieties.
- **Proposed convergence:** a designed candidate for common use, not proof of existing usage.
- **Community-tested proposal:** a proposal with documented evaluation; this label does not imply universal acceptance.
- **Adopted convention:** a convention supported by documented, sustained use in a stated scope.
- **Creative coinage/application canon:** invented forms for a creative or application context, kept separate from linguistic evidence.

Do not call all Creoles one language for convenience. Do not infer a genealogical relationship from a shared label, a similar word, or a resemblance alone. Include varieties beyond French-lexifier Creoles where relevant and properly sourced; record their histories and relationships accurately rather than forcing them into one family tree.

## 3. Conceptual layers

1. **Language and variety registry** — identifiers, names, locations where relevant, self-designations, orthographies, variation and relationship claims.
2. **Evidence and provenance** — sources, exact locations, dates, rights, consent, uncertainty and review status.
3. **Linguistic records** — lexical forms, senses, grammar, pronunciation, register, pragmatics and contextual examples.
4. **Comparison graph** — typed relationships such as shared feature, lexical borrowing, contact influence, structural comparison, mutual-intelligibility claim, design inspiration or disputed relationship.
5. **Bridge layer** — cross-variety glosses, concept mappings, explanations, paraphrases and learning paths.
6. **Convergence design layer** — candidate vocabulary, grammar, spelling, pronunciation and usage conventions, each with rationale and alternatives.
7. **Evaluation layer** — comprehension, production, learnability, ambiguity, register, accessibility and speaker feedback.
8. **Distribution and application layer** — versioned snapshots for learning, search, speech, translation, publishing, games, music and other tools.
9. **Governance and change propagation** — decisions, dissent, versioning, rights gates, corrections and downstream impact.

## 4. Convergence workflow

Use the following loop:

`DISCOVER → DOCUMENT → COMPARE → PROPOSE → TEST → REVISE → REVIEW → RELEASE → OBSERVE → MAINTAIN`

### Step 1 — Document

Collect permitted, traceable evidence of real usage. Preserve original spellings and variants. Record language/variety, source location, meaning, context, date, register where supported, rights and consent.

### Step 2 — Compare

State exactly what is similar and different. Separate semantic similarity, formal similarity, structural comparison, contact influence and genealogical hypotheses. Include counterexamples and conflicting evidence.

### Step 3 — Build the bridge

Prefer an explanation or mapping that preserves each language's own form and meaning. A bridge can use paraphrase, glosses, audio, examples or context—not just word substitution.

### Step 4 — Propose only where needed

A candidate common form or rule must include:
- stable proposal ID and version;
- target concept/function and intended scope;
- source records and comparative rationale;
- alternatives considered;
- predicted benefits and possible harms;
- known ambiguity, false friends and register concerns;
- pronunciation, spelling or grammar choices where applicable;
- evaluation plan and explicit unresolved questions.

### Step 5 — Test with speakers

Use tasks rather than preference polling alone: interpret a new sentence, follow an instruction, explain a meaning, produce a response, distinguish a false friend, and learn a form after a short exposure. Include speakers from different participating varieties and relevant usage backgrounds. Obtain informed consent and minimise personal data.

### Step 6 — Revise and release

Publish results, including negative results, uncertainty, disagreements and sample limitations. Do not promote a proposal to attested usage. Do not claim community endorsement from a small or unrepresentative test.

### Step 7 — Observe use

Track voluntary use, comprehension, corrections, learnability and continued use over time. Revisit proposals when evidence changes. A proposal may be revised, forked, deprecated or rejected.

## 5. Decision rules for candidate forms

Use a documented decision matrix rather than a single prestige or speaker-count ranking. Consider:

- comprehension across the intended varieties;
- semantic precision and risk of false friends;
- naturalness and compatibility with each language's grammar;
- ease of learning and pronunciation;
- accessibility in speech, writing and low-bandwidth tools;
- cultural meaning, register and social implications;
- source quality and confidence;
- community feedback and adoption evidence;
- reversibility and cost of changing a convention.

Possible actions are **reuse**, **adapt**, **combine**, **create**, **retain alternatives**, or **defer**. No candidate must be selected if evidence is insufficient.

## 6. Record model and status fields

Build on existing stable IDs and schemas; do not introduce a parallel data system. Proposed records should link to existing language, variety, source, lexical, grammar, concept and evaluation records.

Every convergence proposal should record at least:
- `proposal_id`, `proposal_version`, `target_scope`;
- `target_concept_or_function`;
- `candidate_form_or_rule`;
- `source_ids` and relevant source locations;
- `evidence_status`, `rights_status`, `review_status`;
- `alternatives`, `rationale`, `counterevidence`, `known_risks`;
- `evaluation_protocol`, `results`, `sample_limitations`;
- `community_feedback_summary` with consent and privacy safeguards;
- `decision_status`, `decision_record`, `version` and downstream consumers.

Keep evidence status, rights status, review status and proposal/adoption status as separate dimensions. Unknown remains unknown. Do not add a new required field without updating schemas, fixtures, validators and compatibility notes together.

## 7. Evaluation gates

A proposal may advance only when the gate's evidence is recorded.

- **Gate A — traceability:** sources and rights/consent status are adequate for the intended use.
- **Gate B — linguistic clarity:** scope, meaning, variation and alternatives are documented.
- **Gate C — test readiness:** tasks, participant inclusion, scoring and privacy plan are defined.
- **Gate D — observed results:** results and limitations are published; unsupported claims are removed.
- **Gate E — release readiness:** schema validation, regression tests, versioning and consumer impact checks pass.
- **Gate F — adoption claim:** sustained use is demonstrated with evidence appropriate to the claim. Downloads or generated examples alone are insufficient.

Rights or privacy uncertainty blocks redistribution of affected content. A proposal may still be discussed at metadata level where lawful and appropriate.

## 8. Community governance

BabelGlobalKreole is currently a maintainer-led framework, not a constituted global standards body. This document does not claim endorsement by any language community.

- Technical mechanics can be maintained centrally with documented review.
- Claims about real-language usage require traceable evidence and appropriate specialist input.
- Community-specific meanings, sensitive material and identity decisions require relevant community involvement.
- Convergence proposals must preserve alternatives, dissent and the right not to participate.
- No community's language is merely raw material for another community's product.
- Contributors retain recognition according to licence, consent and attribution terms.
- Commercial reuse and AI use follow source-specific rights and consent; public accessibility does not grant permission.

## 9. Project responsibilities

- **BabelGlobalKreole:** canonical schemas, terminology, provenance, relationship types, convergence proposals, evaluation contracts, versioning and interoperability.
- **Applied Creole Linguistics:** research protocols, comparative analyses, prototype exercises, speaker testing, evaluation results and teaching implications.
- **Mascarene Knowledge Commons:** source-aware discovery, accessible explanations, context, uncertainty, links and practical next steps.
- **Applications:** consume versioned records; they do not silently redefine linguistic evidence or the framework.

Each project remains independently maintained. Link to canonical records instead of copying entire source datasets.

## 10. First pilot

Start with a small, sourced comparison involving Haitian Kreyòl and Mauritian Kreol, only where comparable evidence can be found and permitted. Do not assume the languages are interchangeable or that a specific pair of forms is equivalent before research.

1. Select a small number of everyday concepts or communicative tasks.
2. Link each entry to inspected sources and exact locations.
3. Document meanings, contexts, variants and unresolved differences.
4. Create a bridge explanation.
5. If justified, propose one clearly labelled convergent candidate.
6. Prepare comprehension and production tasks for speaker review.
7. Publish the protocol and limitations before claiming a result.

This pilot is a research plan, not evidence that speaker testing or convergence has already occurred.

## 11. Definition of done for the architecture milestone

- [ ] The bridge and potential shared-language horizons are explicit.
- [ ] Attested usage, comparison, bridge mappings, proposals and adoption are distinct.
- [ ] Existing schemas and IDs are reused where appropriate.
- [ ] The evaluation and governance gates are documented.
- [ ] Cross-project responsibilities are linked without merging repositories.
- [ ] A first pilot is scoped without fabricated data or claims of validation.
- [ ] Links, schemas, tests and status statements are checked before release.

## 12. References and adjacent resources to audit

These are candidate resources to inspect and cite for specific uses; their existence does not grant permission to copy their data:
- CreoleVal: https://github.com/hclent/creoleval
- APiCS Online: https://apics-online.info/
- CLDF APiCS dataset: https://github.com/cldf-datasets/apics
- Creole NLP: https://github.com/creole-nlp/creole-nlp

Before importing records, verify current scope, licence, provenance, version, and any third-party dataset terms.