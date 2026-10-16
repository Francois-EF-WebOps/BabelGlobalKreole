# Change propagation

A canonical record change does not automatically rewrite every consumer. It triggers impact review.

Each change records ID/date; old/new versions; reason and evidence; compatibility class; affected records and consumer projects; tests to rerun; required review; migration/rollback/deprecation plan; release version.

## Loop
1. Change a canonical record in a reviewed branch.
2. Identify consumers and tests.
3. Run schema/regression checks.
4. Report pass/fail/untested consumers.
5. Decide which downstream updates are needed.
6. Applications pin a released version or snapshot.
7. Review and release consumer changes separately.
8. Feed issues/failures back without silent overwrites.

## Adoption maturity
M0 documented; M1 validated by schemas/local tests; M2 consumed by an independent application; M3 maintained with consumer regression tests; M4 externally reused with verifiable citation/issue/fork/report; M5 community-reviewed with documented input. Never claim a higher level without evidence.
