# KIT.md — Evidence-to-Validation Contributor Kit

**Purpose:** turn one small, sourced language-data contribution into a reproducible, reviewable result. This is a contributor kit, not a claim that the framework is a finished language standard.

## Read first
1. `README.md`
2. `CONTRIBUTING.md`
3. `GOVERNANCE.md`
4. `docs/evidence-policy.md`
5. `docs/data-model.md` and the schema/validation instructions linked from the README.

## Minimum requirements
- One clearly scoped record or correction.
- Source URL plus precise source location; record access date where required.
- Evidence status and uncertainty; do not turn a hypothesis or creative proposal into an attested fact.
- Rights, consent and redistribution status recorded before copying source material.
- Stable identifier and every schema-required field.

## Low-cost tools and procurement
- Start with a phone and the GitHub web interface; no paid service is required by this kit.
- If validation requires a computer/runtime, use the repository's documented free CI workflow or a trusted local Node/Python environment only after identifying the actual project requirements.
- Do not purchase a data service, API plan, or hosting before proving the need. Do not put credentials in commits.

## Procedure
1. Read the existing schema and an accepted example; do not invent fields.
2. Select one small source-backed change.
3. Record the source and rights evidence before drafting the record.
4. Add the record in the existing canonical location; preserve existing records and histories.
5. Run the repository's documented validator/CI. If the command is unknown, inspect workflow files and package/config files first; do not guess.
6. Run at least one negative check (missing required field, invalid identifier, or invalid provenance) using a disposable fixture, not production data.
7. Review the diff for unrelated changes, secrets, copied copyrighted text and unsupported claims.
8. Record exact commands, result, commit/PR link, and unresolved failures.

## Acceptance checklist
- [ ] Schema-valid positive example.
- [ ] Negative fixture is rejected for the expected reason.
- [ ] Every factual record has traceable source provenance and rights status.
- [ ] Existing records and project boundaries remain intact.
- [ ] A second contributor can repeat the steps from this file.
- [ ] Results distinguish verified checks from checks not run.

## Evidence to attach
A short case study: problem → source → data change → validation command/result → limitation → handover. Do not claim the live Pages deployment works unless the deployed URL, sitemap/robots and other relevant endpoints have actually been checked.