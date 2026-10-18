# Autonomous idea-to-consumer lane (first implementation)

**Canonical repository:** BabelGlobalKreole  
**Coordination reference:** Mascarene Knowledge Commons, docs/KNOWLEDGE_TO_DISTRIBUTION_SYSTEM.md  
**Status:** First bounded lane; automated build and delivery require CI/deployment verification.

## Decision

Reuse BabelGlobalKreole's existing public source, validation conventions, Pages workflow, and static-site builder. Do not create a new umbrella repository. MKC remains the coordination and governance layer; it does not copy canonical language content.

The first lane takes one owner-authored, release-approved source record and generates:
1. A mobile-readable public HTML page.
2. An RSS 2.0 feed entry.
3. A machine-readable JSON source record.
4. Social-post copy.
5. Newsletter copy.
6. A manifest recording outputs and which delivery steps have actually occurred.

The source record is distribution/source.json. It summarises the repository's own scope; it is not a claim of independent linguistic validation.

## Lifecycle

SOURCE RECORD → RELEASE GATE → BUILD → TEST → PAGES DEPLOYMENT → RSS / JSON CONSUMPTION → METRICS → REVIEW

GitHub Actions runs the deterministic build. The existing Pages deployment remains guarded by the repository's PAGES_ENABLED == 'true' variable. A successful build or uploaded artifact does not prove that the site is public; the deployment job and live URLs must be checked.

## Channel boundaries

| Channel | Automated in this version | Consumer-facing status |
|---|---|---|
| Website page | Build and include in Pages artifact | Live only after a successful Pages deployment |
| RSS | Generate feed.xml and advertise it from the site | Live only after a successful Pages deployment |
| JSON | Generate a public machine-readable record | Live only after a successful Pages deployment |
| Social | Generate copy and URL | Not auto-posted; no social account/API credentials configured |
| Newsletter | Generate copy | Not emailed; no email delivery provider configured |

The first version does not claim social posting, email delivery, revenue, readership, or SEO indexing. Do not add paid services. If free social APIs are later configured, use repository secrets, deduplication/idempotency, bounded retries, and failure notification before enabling automatic posting.

## Quality and safety gates

- Source record is valid JSON and contains required metadata.
- Status must be exactly approved_for_publication.
- Rights status must be the explicitly allowed owner-authored-summary value.
- Source and canonical URLs must be HTTPS and include labels.
- Slug and date formats are validated.
- Source list is non-empty; the body contains a sources/status section.
- Website, RSS and JSON outputs must exist and be non-empty.
- Canonical URL, RSS URL, source record ID, and feed item URL must be consistent.
- Do not place secrets, personal records, private conversations, unreviewed claims, or uncleared third-party material in the public source record.
- Do not auto-publish arbitrary ideas: the source record's explicit release status is a hard gate.

## Delivery receipts and retries

GitHub Actions run URL and deployment URL are the primary delivery receipts. The generated manifest lists each channel and avoids representing generated copy as a delivered post or email. Failed validation stops the build. Failed deployment fails the deploy job and can be rerun through GitHub Actions; do not create an automatic infinite retry loop. The workflow's native failure notifications are the exception channel; the repository owner's GitHub notification preferences determine how those are delivered.

## Measurement

Record only observed values. In the initial lane:
- Source records: 1.
- Channel assets generated: 5.
- Public website/RSS/JSON availability: pending a successful Pages deployment and live URL checks.
- Social reach, RSS subscribers, page views, conversions, and revenue: unknown until real telemetry exists.

After deployment, verify the exact Pages URL, article page, feed, JSON, sitemap, and robots directives. If privacy-respecting analytics are added later, prefer aggregate metrics and do not introduce unnecessary personal-data collection.

## Acceptance tests

Run:

    python scripts/test_distribution.py
    python scripts/build_distribution.py --base-url https://example.test/project --output-dir /tmp/babel-distribution-test

Expected:
- Approved source builds all five channel assets.
- Draft/unapproved source is rejected.
- Missing sources are rejected.
- Feed and sitemap include the article URL.
- Root page advertises the RSS feed and article.
- Manifest records generated outputs separately from actual delivery.
- No third-party service or paid API is required to build the package.

## Current limitation

This is a bounded, reproducible distribution lane, not yet a fully autonomous social/email publisher. Public delivery depends on the existing Pages setting and a successful deployment. Live reach and revenue cannot be claimed without measurement.
