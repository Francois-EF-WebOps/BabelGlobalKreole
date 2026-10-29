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

## TikTok first adapter (inbox/draft only)

`scripts/tiktok_adapter.py` implements a small, mock-tested client for TikTok's official
Content Posting API inbox-upload initialization and status lookup. It uses
`video.upload` and `PULL_FROM_URL`; it does **not** call Direct Post and does not claim
that an upload is published. The creator must open the TikTok inbox notification and
finish the post in the TikTok app. The media URL must use a domain/prefix verified with
TikTok. The adapter is not wired into the live publisher yet; live publishing remains
fail-closed until account OAuth, UX/consent, verified media hosting, and reconciliation are
reviewed. An ambiguous network failure during initialization is surfaced as an unknown
outcome and is never blindly retried.

Official reference: https://developers.tiktok.com/docs/en/content-posting-api-reference-upload-video

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

## Explicit single-item TikTok inbox command

`scripts/tiktok_inbox_publish.py` is a separate, single-item entry point for an explicitly
authorized draft upload. It requires all of the following environment values:
- `TIKTOK_ACCESS_TOKEN`: token from the creator's authorized TikTok account.
- `PUBLISHING_ENABLED=true`.
- `TIKTOK_INBOX_UPLOAD_ENABLED=true`.
- `TIKTOK_VERIFIED_VIDEO_HOSTS`: comma-separated exact hostnames verified with TikTok.

Example (only after app authorization and hostname verification):

```sh
export TIKTOK_ACCESS_TOKEN='…'
export PUBLISHING_ENABLED=true
export TIKTOK_INBOX_UPLOAD_ENABLED=true
export TIKTOK_VERIFIED_VIDEO_HOSTS='media.example.com'
python scripts/tiktok_inbox_publish.py --video-url 'https://media.example.com/approved-cut.mp4'
```

The example hostname is illustrative and must be replaced with a real verified hostname.
Never commit tokens or put them in command-line arguments. The command handles one URL per
invocation; it does not schedule or bulk-upload the 11 configured channels. A successful
response means only that inbox upload was initialized, not that a video was published.
Check a returned ID with `python scripts/tiktok_inbox_publish.py --status PUBLISH_ID`.
Status checks require the same authorized token. Status output and the upload response should
be retained for reconciliation; no real account or token has been used in CI.

## TikTok Direct Post adapter

`scripts/tiktok_direct_post_adapter.py` implements the official Direct Post initialization flow:
it queries current creator info first, checks the selected privacy level against the returned
options, requires explicit consent from the caller, then initializes a single post from a
public HTTPS video URL. It returns a `publish_id`; that ID must be reconciled through the
status endpoint before recording a post as completed.

The adapter is deliberately not wired to scheduled publishing yet. A successful init is not
proof of a completed post, and an ambiguous network outcome must not be retried blindly.
TikTok requires the app to have the `video.publish` scope approved and authorized. Until the
app has passed TikTok's audit, direct-post content is restricted to private viewing. TikTok's
Direct Post guidance also requires creator information to be displayed and explicit consent
to be collected in the publishing UX; an unattended job alone does not satisfy that UX
requirement. See:
- https://developers.tiktok.com/docs/en/content-posting-api-reference-direct-post
- https://developers.tiktok.com/docs/en/content-posting-api-get-started

CI tests use mocked responses only. No real account, token, video URL, or post is used.
