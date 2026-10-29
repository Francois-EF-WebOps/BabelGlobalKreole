# Channel call-sheet backend

## Purpose

Build a daily Markdown call sheet for human-operated social accounts. This lane validates candidate cuts and never publishes to a platform.

## Files

- `data/channels.json`: 11 channel registry, policy caps, assigned language and affiliate-program key.
- `data/affiliates.json`: known program keys; payout minimum and approval mode remain unknown until verified.
- `data/seasons.json`: source seasons and their actual runtime.
- `data/cuts.json`: real cut records. Starts empty; synthetic test records live under `tests/fixtures/`.
- `scripts/dedup.py`: within-season attention-range overlap checks and channel-saga hash reuse checks.
- `scripts/build_call_sheet.py`: validates approved cuts and writes `today.md`.
- `scripts/test_call_sheet.py`: acceptance and negative tests.
- `.github/workflows/call-sheet-check.yml`: test workflow for the feature branch.

## Important data interpretation

The source brief uses `product_id` for the value that must match `channel.affiliate_program_id`. This first version follows that exact contract, so `product_id` currently stores the affiliate program key, not a separately catalogued physical product. A future product catalogue should separate `product_id` from `affiliate_program_id` before tracking individual products.

The current channel list and proposed brand/affiliate table conflict on several affiliate assignments. The registry uses the earlier explicitly enumerated 11-channel mapping as the initial source of truth. Verify those assignments before any affiliate links or product claims are published. Proposed brand handles are stored separately and do not rename the underlying account IDs.

No master assets or season assets were supplied, so channel `master_id` and season registry start as null/empty rather than inventing asset identifiers. Real approved cuts cannot be scheduled until their season records are populated.

## Validation rules

- Only cuts with `status: approved` appear on the call sheet.
- The whole set of cuts is checked for overlapping source ranges within a channel/season and duplicate hashes within a channel saga.
- Approved cuts must reference a registered channel, affiliate program and season belonging to that channel.
- Cut language must match the channel primary language.
- The cut `product_id` must match the channel affiliate program key.
- Per-channel daily cap is 3; global operator cap is 12.
- A season can yield at most 12 approved cuts, and their combined runtime cannot exceed 45% of the season runtime.
- The generated hourly times are operator placeholders for sequencing only, starting at the configured time. They are not audience-optimised recommendations and no content is published.
- The call sheet's post URL column is completed only after the operator manually posts.

## Run

```sh
python scripts/build_call_sheet.py --day 2026-10-29 --output /tmp/today.md
pytest -q scripts/test_call_sheet.py
```

The production `data/cuts.json` is intentionally empty until actual content is approved. `tests/fixtures/mock_cuts.json` is synthetic and must never be posted.
