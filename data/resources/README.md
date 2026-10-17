# External resource cards

Canonical resource-card records are stored as one JSON object per line in `resources.jsonl` and validated against `schemas/resource-card.schema.json`.

- A card records access and verification separately from reuse permissions.
- `verified` means the resource landing page or official terms were reachable and inspected during the stated check; it does not imply every claim, item, or license is fully verified.
- `unverified` means the page or rights details could not be verified during this check.
- A link does not grant permission to copy, redistribute, train on, or synthesize source material.
- Unknown permissions remain `unknown`; do not convert them to allowed by inference.
- Cards are discovery metadata, not copies of the linked resources.
