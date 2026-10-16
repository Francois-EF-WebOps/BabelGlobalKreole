# Evaluation and release gates

Tests assess declared properties, not whether a language community can be reduced to a score. Report scope, sample size, coverage, failures and uncertainty.

Test families: schema validity and IDs; provenance completeness; rights/privacy gates; orthographic consistency within a declared design; grammar consistency for a declared rule set; semantic distinctions; task-specific translation; pronunciation mapping; regression examples; application compatibility.

Severity:
- `blocker`: rights/privacy violation, destructive history change, fabricated provenance, invalid release package.
- `high`: schema failure, core contradiction, unlabelled invention, broken stable ID.
- `medium`: coverage gap or missing non-critical metadata.
- `low`: style or discoverability issue.

Release is blocked if any blocker remains; required schemas fail; factual claims lack provenance/evidence labels; redistributed content has unknown rights; breaking changes lack migration notes; or release notes overstate tests, adoption, completeness or integrations.

Human/community review is required for high-impact descriptions of community language practice, disputed history, proposed standardization affecting communities, and unresolved rights/privacy implications. Report machine tests separately from human review.
