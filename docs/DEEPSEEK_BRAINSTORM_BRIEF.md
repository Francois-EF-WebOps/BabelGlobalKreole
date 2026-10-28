# DeepSeek brainstorming brief: BabelGlobalKreole automation

## Objective
Find the smallest reliable, free, Android-friendly path from existing BabelGlobalKreole source material to reviewed social content, distributable artifacts, publication records, and measured feedback.

## Current verified baseline
- The seven-post queue exists on branch `feat/seven-post-approval-queue`.
- Builder: `scripts/build_post_queue.py`.
- Tests: `scripts/test_post_queue.py`.
- Workflow: `.github/workflows/distribution-check.yml`.
- Documentation: `docs/SEVEN_POST_APPROVAL_QUEUE.md`.
- Current outputs include `approval-queue.md`, `approval-queue.json`, and `receipts.json`.
- Queue items remain `awaiting_human_approval`; receipts must state `not_sent`, `published: false`, and `publication_attempted: false`.
- Current workflow tests and uploads a queue artifact. It does not publish to social platforms or collect analytics.
- Do not assume this branch has been merged to main. Check current repository state before proposing modifications.

## Constraints
- Zero budget; prefer GitHub Actions and standard-library Python.
- Android-only maintainer workflow; review must be possible from a phone.
- Preserve existing files and behaviour. No rewrite, second distribution system, boilerplate scaffolding, placeholders, or unverified claims.
- No social credentials or automatic public posting in the first implementation.
- Keep evidence, provenance, licensing, and human review for linguistic claims.
- Never treat generated drafts, queue builds, or workflow success as proof of publication, reach, accuracy, or revenue.
- Avoid paid APIs, third-party packages, and new external services unless there is a compelling, explicitly costed reason.

## Questions to challenge
1. What is the smallest useful next increment after the existing queue?
2. Which steps should be deterministic scripts versus AI-assisted brainstorming?
3. What checks prevent unsupported claims, missing sources, duplicate posts, invalid state transitions, or accidental publication?
4. How should the queue represent draft, validated, awaiting approval, approved, published, failed, and measured states without falsely implying a platform action?
5. What is the simplest portable record of publication URL/time and manually or officially collected metrics?
6. What can GitHub Actions do reliably for free, and what requires user interaction or platform API approval?
7. What are the likely failure modes, security concerns, and maintenance costs?
8. What is unnecessary and should be explicitly deferred?

## Required answer format
Return a short, critical design review, not code first:
- **Verified facts vs assumptions**
- **Top 3 options**, compared for cost, complexity, reliability, and Android usability
- **Recommended smallest next increment**
- **Concrete file-level changes** mapped to existing paths
- **Acceptance tests**, including negative tests
- **Risks and rollback**
- **Deferred work**
- **Questions that genuinely block implementation**

Do not invent repository files, test results, API capabilities, platform permissions, or metrics. If you propose an API or platform feature, identify what must be verified before use. Challenge the brief where appropriate and explain trade-offs.