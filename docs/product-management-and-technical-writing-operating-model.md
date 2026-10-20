# Product Management and Technical Writing Operating Model

**Status:** Proposed operating standard  
**Applies across:** BabelGlobalKreole, Applied Creole Linguistics, and Mascarene Knowledge Commons  
**Principle:** Product management and technical writing are continuous project capabilities, not occasional tasks or job titles.

## Purpose

Every project should be able to explain who it serves, what problem it addresses, what is currently true, what will be delivered next, how quality will be judged, and how another person can understand or continue the work.

This operating model adapts the useful responsibilities commonly found in product-management and technical-writing roles. It does not imply employment, institutional endorsement, or that any project is already production-ready.

## Shared responsibilities

### Product management
- Maintain a clear problem statement, intended audiences, user needs, and explicit non-goals.
- Prioritize work by user value, evidence, feasibility, risk, cost, and available capacity.
- Keep a roadmap with small, verifiable milestones and named acceptance criteria.
- Record decisions, dependencies, risks, assumptions, and changes in scope.
- Define the smallest useful release and collect feedback before expanding.
- Report honestly on status: planned, in progress, blocked, tested, released, or retired.

### Technical writing and knowledge stewardship
- Keep the README as the reliable entry point: purpose, current status, how to use or inspect the project, limitations, and next steps.
- Write for the intended reader, not only for the project author.
- Maintain a consistent vocabulary and explain specialist terms.
- Separate sourced facts, interpretations, proposals, hypotheses, and validated results.
- Link claims to traceable sources where applicable; record provenance, rights, consent, and uncertainty.
- Provide examples and step-by-step instructions that can be followed on a phone where practical.
- Keep documentation synchronized with actual repository state; never describe unbuilt or untested features as complete.

## Shared minimum artefacts

Each repository should maintain or explicitly mark as not yet needed:

1. **Project brief:** audience, problem, value, scope, non-goals.
2. **Roadmap:** next milestones, priority rationale, dependencies, and status.
3. **Decision log:** decision, date, rationale, alternatives, consequences.
4. **Risk and assumptions register:** uncertainty, impact, mitigation, review trigger.
5. **Acceptance tests:** observable conditions for considering a milestone complete.
6. **Evidence/source ledger:** source, claim supported, provenance, rights/status, limits.
7. **Release notes/changelog:** what changed, what did not, known issues, validation performed.
8. **Contribution guide:** how to propose corrections, contribute safely, and report problems.
9. **Cross-project interface note:** which project owns each artefact and where canonical information lives.

Do not create empty files simply to satisfy this list. Add an artefact when it serves a real need; otherwise document the decision and review date.

## Status vocabulary

Use consistent status labels across projects:

- **Proposed** — an idea, not yet committed.
- **Planned** — selected for future work.
- **In progress** — work has started.
- **Blocked** — a dependency or constraint prevents progress.
- **Implemented** — the artefact or feature exists.
- **Tested** — a stated test was performed; record the result.
- **Released** — intentionally made available to its intended audience.
- **Validated with participants** — a defined user/community test was conducted and its scope and limits are documented.
- **Retired** — no longer maintained or recommended.

“Implemented” does not mean “tested”; “tested” does not mean “validated by the community.”

## Cross-project division of responsibility

### BabelGlobalKreole — framework and shared architecture
Owns the global language/variety framework, comparison concepts, bridge and convergence terminology, governance principles, and cross-language proposal status. It must not imply that all Creoles are interchangeable or that a shared form has community acceptance without evidence.

### Applied Creole Linguistics — research and validation
Owns research questions, methods, evidence standards, evaluation design, consent/privacy practice, speaker-testing records, and interpretation of results. Hypotheses must remain distinguishable from findings.

### Mascarene Knowledge Commons — discovery and public context
Owns the public-facing discovery journey, accessible explanations, contextual pages, source-backed knowledge, and reader feedback routes. It is a coordination/discovery layer, not the canonical linguistic standard.

### Shared boundary
A project may link to another project's canonical artefact; it should not silently duplicate or redefine it. Changes that affect another project's interface must be recorded and linked.

## Lightweight operating cadence

- **At each work session:** identify one user-facing outcome and one verifiable finish condition.
- **At each milestone:** update status, acceptance evidence, known limitations, and next action.
- **At each release:** review README, changelog, links, rights/privacy, and what was actually tested.
- **Monthly or at a major change:** review priorities, assumptions, dependencies, and whether documentation still matches reality.

Given phone-first and resource-constrained work, prefer short Markdown records, simple tables/CSV when useful, and small changes that can be reviewed in GitHub mobile. Avoid introducing paid tools or heavy systems unless a demonstrated need justifies them.

## Acceptance checklist

A milestone is not considered complete until the relevant items are checked:

- [ ] A specific audience and need are named.
- [ ] The deliverable and non-goals are clear.
- [ ] Acceptance criteria are observable.
- [ ] Sources, permissions, and privacy are handled where applicable.
- [ ] Documentation matches the artefact that exists.
- [ ] Validation claims match tests actually performed.
- [ ] Dependencies and cross-project links are current.
- [ ] The next action is small and explicit.

## Portfolio evidence and employment integrity

These projects can demonstrate product thinking, technical writing, research coordination, and documentation practice. They must be described as independent portfolio work. Do not claim paid client delivery, team size, usage metrics, production reliability, external adoption, or speaker validation unless independently evidenced.

For job applications, tailor the portfolio to the employer's actual requirements and clearly distinguish professional employment history from independent project work.
