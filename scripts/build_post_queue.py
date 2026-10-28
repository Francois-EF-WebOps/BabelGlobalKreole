#!/usr/bin/env python3
"""Build a phone-readable seven-post approval queue and non-delivery receipts."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "distribution" / "post-queue.json"
EXPECTED_POSTS = 7
REQUIRED_STATUS = "awaiting_human_approval"


def validate_batch(batch: dict) -> dict:
    required = ("batch_id", "title", "language", "status", "approval_policy", "posts")
    missing = [key for key in required if key not in batch]
    if missing:
        raise ValueError("missing required fields: " + ", ".join(missing))
    if batch["status"] != REQUIRED_STATUS:
        raise ValueError("batch must remain awaiting_human_approval")
    if not isinstance(batch["posts"], list) or len(batch["posts"]) != EXPECTED_POSTS:
        raise ValueError(f"batch must contain exactly {EXPECTED_POSTS} posts")
    ids = set()
    for index, post in enumerate(batch["posts"], start=1):
        for key in ("id", "title", "hook", "body", "cta", "source_urls", "status"):
            if key not in post:
                raise ValueError(f"post {index} missing required field: {key}")
        for key in ("id", "title", "hook", "body", "cta"):
            if not isinstance(post[key], str) or not post[key].strip():
                raise ValueError(f"post {index} field {key} must be non-empty")
        if post["id"] in ids:
            raise ValueError(f"duplicate post id: {post['id']}")
        ids.add(post["id"])
        if post["status"] != REQUIRED_STATUS:
            raise ValueError(f"{post['id']} must remain awaiting_human_approval")
        if not isinstance(post["source_urls"], list) or not post["source_urls"]:
            raise ValueError(f"{post['id']} requires at least one source URL")
        for url in post["source_urls"]:
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError(f"{post['id']} has a non-HTTPS or invalid source URL")
        if post["cta"].strip() == "":
            raise ValueError(f"{post['id']} requires a reviewable CTA")
    return batch


def load_batch(path: Path) -> dict:
    return validate_batch(json.loads(path.read_text(encoding="utf-8")))


def render_markdown(batch: dict) -> str:
    lines = [
        f"# {batch['title']}",
        "",
        f"**Batch:** `{batch['batch_id']}`  ",
        f"**Status:** Awaiting human approval — nothing has been posted.  ",
        f"**Language:** {batch['language']}",
        "",
        "> Phone review: read each post, open its sources, then approve, edit, or reject it in the GitHub pull request. Approval of this queue does not itself publish to a social account.",
        "",
    ]
    for index, post in enumerate(batch["posts"], start=1):
        lines.extend([
            f"## {index}. {post['title']}",
            "",
            f"**Hook:** {post['hook']}",
            "",
            post["body"],
            "",
            f"**Suggested CTA:** {post['cta']}",
            "",
            "**Sources:**",
        ])
        lines.extend(f"- [{url}]({url})" for url in post["source_urls"])
        lines.extend(["", f"**Review status:** `{post['status']}`", ""])
    return "\n".join(lines).rstrip() + "\n"


def build(batch: dict, output_dir: Path) -> dict:
    validate_batch(batch)
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    queue_copy = dict(batch)
    queue_copy["generated_at_utc"] = generated_at
    (output_dir / "approval-queue.json").write_text(
        json.dumps(queue_copy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "approval-queue.md").write_text(render_markdown(batch), encoding="utf-8")
    receipt = {
        "batch_id": batch["batch_id"],
        "generated_at_utc": generated_at,
        "source_path": "distribution/post-queue.json",
        "post_count": len(batch["posts"]),
        "human_approval_required": True,
        "publication_attempted": False,
        "delivery_status": "not_sent",
        "posts": [
            {
                "post_id": post["id"],
                "status": "queued_for_human_review",
                "delivery_status": "not_sent",
                "published": False,
                "source_count": len(post["source_urls"]),
            }
            for post in batch["posts"]
        ],
    }
    (output_dir / "receipts.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        receipt = build(load_batch(args.source), args.output_dir)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"POST QUEUE BUILD FAILED: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "status": "queued_for_human_review",
        "batch_id": receipt["batch_id"],
        "post_count": receipt["post_count"],
        "delivery_status": receipt["delivery_status"],
        "outputs": ["approval-queue.md", "approval-queue.json", "receipts.json"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
