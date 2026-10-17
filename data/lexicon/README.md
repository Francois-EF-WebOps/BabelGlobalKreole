# Lexical records

Store one validated JSON record per file or use a documented JSONL export. Do not add bulk dictionary/corpus content until rights and provenance are verified. Use `schemas/lexical-entry.schema.json`.

## Online lexical resources

Online dictionaries and phrase lists are catalogued separately in `data/resources/online-lexical-resources.jsonl`. A resource card is a discovery link, not a claim that its content may be copied or redistributed.

Before importing a word, definition, example, pronunciation, or bulk export:

1. Identify the exact entry and underlying source; do not treat an aggregator as a single authoritative source.
2. Record the canonical URL, access date, and precise entry/page/section locator in a source record.
3. Check the applicable license and attribution requirements, including any third-party content or item-level exceptions.
4. Record rights and each relevant AI-use permission separately. If uncertain, keep the item linked externally and do not copy it.
5. Distinguish source-attested forms from proposed forms, editorial corrections, and creative coinages.
6. Validate the lexical record against `schemas/lexical-entry.schema.json` and run the repository validation workflow.

The initial online-resource register includes Wiktionary's Mauritian Creole lemma category, Glosbe's English–Morisyen interface, Lexilogos's Mauritian dictionary directory, and Omniglot's Mauritian phrase list. Their availability does not mean that every item is independently verified or cleared for reuse. No lexical entries have been imported by adding these resource cards.


## Global coverage and scope

The online-resource register is not Mauritius-only. `data/resources/global-lexical-resources.jsonl` adds cross-Creole discovery resources and language-specific links for Haitian Creole, Jamaican Creole, Seychellois Creole, and Papiamentu, alongside the Mauritian-focused links in `data/resources/online-lexical-resources.jsonl`. The existing general resource catalogue also links to global references such as Glottolog and APiCS.

These records are a starting index, not a claim of complete global coverage. Continue coverage in the project's agreed order—Mauritian Creole, French-lexifier Creoles, English-lexifier Creoles, Portuguese-lexifier Creoles, Spanish-lexifier Creoles, then Dutch-lexifier Creoles—while also tracking Arabic-lexifier and other contact-language traditions already in scope. Do not force every contact language into a Creole classification, and do not infer lexical equivalence from a shared lexifier.

Use APiCS for comparative structural descriptions and its cited bibliographies; do not treat it as a bulk lexicon. Use WOLD for loanword/etymological investigation only for the languages and datasets it actually contains. Creole NLP is a discovery index whose linked datasets have independent rights and access conditions. The ASJP Haitian wordlist is currently link-only because its dataset reuse terms were not verified in this review.
