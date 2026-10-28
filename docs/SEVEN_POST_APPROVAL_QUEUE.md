# Seven-post approval queue

## Purpose

Generate one batch of seven evidence-led, English-language social drafts from existing BabelGlobalKreole scope and policy documents. This extends the existing distribution lane; it does not create another repository or replace `distribution/source.json`.

## Phone review

1. Open the pull request containing `distribution/post-queue.json`.
2. Read the generated `approval-queue.md` artifact from the Distribution Queue Checks workflow, or inspect the source JSON directly.
3. Open the cited source links for each post.
4. Approve, edit, or reject each item in the PR discussion. Do not treat merge as permission to post to an external account.
5. External publishing remains a separate manual action until a platform and account permissions are explicitly configured.

## Hard gates

- Exactly seven unique post IDs per batch.
- Every post has a hook, body, call to action, and one or more HTTPS source URLs.
- Every post remains `awaiting_human_approval` until reviewed.
- The builder creates Markdown and JSON review queues plus `receipts.json`.
- Receipts must say `not_sent`, `published: false`, and `publication_attempted: false`; queue generation is not delivery.
- No third-party package, paid API, social credential, or email provider is required.
- Queue drafts are not added to the public Pages output by this workflow.

## Commands

```sh
python scripts/test_post_queue.py
python scripts/build_post_queue.py --output-dir /tmp/babel-post-queue
```

## Acceptance

A successful build produces `approval-queue.md`, `approval-queue.json`, and `receipts.json` for exactly seven posts. Tests reject wrong batch sizes, duplicate IDs, missing/invalid source URLs, and any attempt to mark the queue or a post as approved for publication without human review.

## Current limits

The batch is a draft queue, not evidence that a post has been published, seen, or generated revenue. This version does not connect to social accounts, schedule posts, or collect engagement analytics.
