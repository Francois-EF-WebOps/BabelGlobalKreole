# Standards and interoperability roadmap

This document records compatibility targets, not a claim of current conformance.

## Language and variety identifiers
- **ISO 639-3:** use only verified identifiers and cite the registry record or authoritative source. Some varieties may have no individual code; do not invent one.
- **BCP 47:** use language tags for language/content identification where a valid tag exists. A tag is not a substitute for a community-appropriate variety identifier.
- **Glottolog:** optionally record a verified Glottocode with lookup date and source. A Glottocode is a catalog identifier, not proof of ancestry or endorsement.
- Keep the framework's stable internal IDs even when external identifiers are absent or contested. External mappings are assertions with provenance, not keys to overwrite identity.

## Data exchange
- **CLDF:** assess a CLDF-compatible export for comparative lexical and structural tables once the first real dataset and its relationships are stable. Do not claim CLDF conformance until the relevant module, metadata, and validation are tested.
- **W3C PROV:** map provenance concepts to PROV-O where this improves interchange; the internal provenance fields remain explicit until a tested mapping exists.
- **OntoLex-Lemon:** consider for lexical resources that need RDF/linked-data interoperability, rather than forcing all project records into RDF prematurely.
- **APiCS and other curated datasets:** cite and link to their records where appropriate; do not copy their data without checking licenses and terms.

## AI/ML packaging
JSONL is the initial portable retrieval format. Each released item should be self-contained enough to preserve its ID, language/variety scope, evidence label, rights state, source references, and schema/release version. Croissant/Hugging Face packaging and embeddings are future adapters, not current capabilities.

## Release gate
A compatibility badge or claim requires a reproducible test, recorded tool/version, and published result. A field named after a standard is not itself conformance.
