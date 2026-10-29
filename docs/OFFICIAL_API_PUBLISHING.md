# Official-API publishing: implementation gates

## Current state

This branch adds a validated dry-run planner and a receipt-ledger primitive. It does **not**
publish to any platform. Live publishing deliberately fails closed until each platform adapter
is implemented and reviewed. The existing manual call sheet and seven-post approval queue
remain intact and are still the fallback.

## Why this is not yet a cron-based live publisher

The registered channel inventory currently lists 11 TikTok channels. It does not contain
YouTube or Meta accounts, OAuth account IDs, platform-specific metadata, or verified video
hosting URLs. Production `data/seasons.json` and `data/cuts.json` are empty.

TikTok's official Content Posting API requires an approved app and `video.publish` scope,
user authorization, a verified domain/prefix for URL pull, a creator-info query, and the
post initialization/status lifecycle. TikTok documents that unaudited clients are restricted
to private viewing. A scheduled job must not pretend these consent and audit requirements
have been satisfied. See the official documentation:
- https://developers.tiktok.com/docs/en/content-posting-api-get-started
- https://developers.tiktok.com/docs/en/content-posting-api-reference-direct-post
- https://developers.tiktok.com/docs/en/content-posting-api-reference-get-video-status

YouTube uploads use a different OAuth scope and resumable upload protocol; they cannot be
implemented by sending the TikTok request shape. Meta/Instagram publishing has separate
account eligibility, permissions, container creation, and publish/status steps.

## Current behavior

- `python scripts/publish.py --dry-run`: runs existing call-sheet validation, requires every
  approved cut to have a public HTTPS `video_url`, and prints a JSON plan. No network calls,
  posts, or receipt mutations occur.
- `python scripts/publish.py --publish --confirm-live`: refuses unless
  `PUBLISHING_ENABLED=true`; even then it refuses because no platform adapter is enabled.
- `data/receipts.json`: reserved for durable per-cut/channel receipts. Confirmed post URLs
  cannot be erased by a later non-published receipt.
- The retry helper supports HTTP 429 and 5xx responses for safe requests, honoring
  `Retry-After`. It explicitly does not blindly retry publish-init after ambiguous network
  failures. The adapter must reconcile provider status first to avoid duplicate posts.
- The workflow runs tests and dry-run only. It does not expose secrets, publish content, or
  commit generated receipts.

## Required before a live adapter can be enabled

1. Confirm the intended platform and actual account for every channel; do not infer from brand handles.
2. Create/review the official developer app and obtain the exact required scopes.
3. Complete per-account OAuth and store credentials as GitHub Actions secrets, never JSON.
4. Verify video hosting/domain ownership and test media accessibility.
5. Implement provider-specific status reconciliation and duplicate protection.
6. Add provider-specific tests using mocked HTTP responses; test the API's real errors and quotas.
7. Verify that the planned UX meets the platform's terms, including any user consent requirements.
8. Start with one authorized test account and a private/unlisted test post before widening access.

The repository's current policy remains stricter than a platform maximum: at most three
approved cuts per channel and twelve total approved cuts per operator day.
