# Instructions for AI agents and LLMs

## Read first
1. README
2. Terminology
3. Evidence policy
4. Governance
5. Data model
6. Relevant schema and task contract
7. Exact sources needed for the task

Retrieve the minimum relevant subset; do not rely on conversational memory as the only source of truth.

## Loop
`LOCATE → READ → CLASSIFY → DRAFT → VALIDATE → REPORT → HAND OVER`

Confirm scope and acceptance criteria. Search for existing IDs. Separate sourced fact, source interpretation, comparison, proposal, creative coinage and unknown. Cite source IDs and exact locations. Record uncertainty/counterevidence. Run relevant checks. Report failures honestly. Identify downstream impacts without silently rewriting consumers. Stop for review on rights, privacy, harm, disputed claims or breaking schema changes.

## Forbidden shortcuts
No invented citations, etymologies, pronunciation claims, licences, endorsements or test results. No normalization of real-world variation for model convenience. No automatic promotion of proposals to accepted status. No unlicensed bulk copying. No destructive edits to source repositories/history. No claim of working API/integration without a reproducible test.

## Output report
Return `result`, `files_changed`, `sources_checked`, `tests_run`, `limitations`, `downstream_impacts`, `next_action`.
