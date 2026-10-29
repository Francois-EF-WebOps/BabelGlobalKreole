#!/usr/bin/env python3
"""Validate and plan official-API publishing; live publishing is deliberately fail-closed.

This module never uses browser automation, unofficial endpoints, or token values in JSON.
A platform adapter must be implemented and reviewed against that platform's current API,
OAuth scopes, user-consent UX, and post-status reconciliation before live mode can be enabled.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS_PATH = ROOT / "data" / "receipts.json"
MAX_RETRIES = 5
MAX_PLATFORM_POSTS_PER_CHANNEL_PER_DAY = 15


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_inputs(channels_doc: dict, affiliates_doc: dict, seasons_doc: dict, cuts_doc: dict) -> list[dict]:
    """Run the existing call-sheet validator before any network operation."""
    from build_call_sheet import validate_and_build

    # Reuse the repository's complete validation rules; do not duplicate or weaken them.
    validate_and_build(channels_doc, affiliates_doc, seasons_doc, cuts_doc)
    channels = {row["channel_id"]: row for row in channels_doc["channels"]}
    approved = [cut for cut in cuts_doc["cuts"] if cut.get("status") == "approved"]
    for cut in approved:
        cut_id = cut["cut_id"]
        video_url = cut.get("video_url")
        if not isinstance(video_url, str) or not video_url.strip():
            raise ValueError(f"{cut_id}: approved cut requires video_url")
        parsed = urlparse(video_url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"{cut_id}: video_url must be a public HTTPS URL")
        platform = channels[cut["channel_id"]].get("platform")
        if not isinstance(platform, str) or not platform.strip():
            raise ValueError(f"{cut_id}: channel has no platform")
        if not isinstance(cut.get("caption", cut.get("hook_visual")), str):
            raise ValueError(f"{cut_id}: caption/hook_visual must be text")
    return sorted(approved, key=lambda row: (row["channel_id"], row["cut_id"]))


def build_plan(channels_doc: dict, cuts: list[dict]) -> list[dict]:
    channels = {row["channel_id"]: row for row in channels_doc["channels"]}
    counts: dict[str, int] = {}
    plan = []
    for cut in cuts:
        channel_id = cut["channel_id"]
        counts[channel_id] = counts.get(channel_id, 0) + 1
        configured_cap = min(
            int(channels[channel_id].get("daily_cap", 3)),
            int(channels_doc.get("policy", {}).get("per_channel_cap", 3)),
        )
        if counts[channel_id] > configured_cap:
            raise ValueError(f"{channel_id}: daily cap exceeded ({counts[channel_id]} > {configured_cap})")
        if counts[channel_id] > MAX_PLATFORM_POSTS_PER_CHANNEL_PER_DAY:
            raise ValueError(f"{channel_id}: conservative platform safety ceiling exceeded")
        plan.append({
            "cut_id": cut["cut_id"],
            "channel_id": channel_id,
            "platform": channels[channel_id]["platform"],
            "video_url": cut["video_url"],
            "caption": cut.get("caption", cut.get("hook_visual", "")),
            "status": "planned_not_sent",
        })
    return plan


def request_with_backoff(request: Request, *, opener: Callable = urlopen,
                         sleep: Callable = time.sleep, retries: int = MAX_RETRIES):
    """HTTP helper for future official adapters; retries 429/5xx only when safe to retry.

    Callers must not use this to blindly repeat a non-idempotent publish-init request.
    For a publish request, reconcile provider status before retrying after an ambiguous result.
    """
    attempt = 0
    while True:
        try:
            return opener(request, timeout=30)
        except HTTPError as exc:
            retryable = exc.code == 429 or 500 <= exc.code <= 599
            if not retryable or attempt >= retries:
                raise
            retry_after = exc.headers.get("Retry-After") if exc.headers else None
            try:
                delay = max(0.0, float(retry_after)) if retry_after else min(2 ** attempt, 60)
            except (TypeError, ValueError):
                delay = min(2 ** attempt, 60)
            sleep(delay)
            attempt += 1
        except URLError:
            # A connection failure may occur after the provider accepted a post.
            # Never retry publish-init blindly; caller must reconcile status first.
            raise


def write_receipt(receipts_path: Path, receipt: dict) -> None:
    """Append/replace by stable cut_id + channel_id; never overwrite a confirmed URL."""
    doc = read_json(receipts_path) if receipts_path.exists() else {"receipts": []}
    rows = doc.get("receipts")
    if not isinstance(rows, list):
        raise ValueError("receipts.json must contain a receipts array")
    key = (receipt["cut_id"], receipt["channel_id"])
    for index, old in enumerate(rows):
        if (old.get("cut_id"), old.get("channel_id")) == key:
            if old.get("platform_post_url") and not receipt.get("platform_post_url"):
                raise ValueError(f"{key}: refusing to overwrite a confirmed post URL")
            rows[index] = {**old, **receipt}
            break
    else:
        rows.append(receipt)
    doc["receipts"] = rows
    receipts_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def publish_one(item: dict, *, environment: dict[str, str] | None = None) -> dict:
    """No live adapter is enabled until its API and consent flow pass review.

    This explicit refusal prevents a workflow from appearing successful while silently
    skipping a provider, or accidentally posting through an unapproved integration.
    """
    env = environment if environment is not None else os.environ
    platform = item["platform"].lower()
    token_name = f"{platform.upper()}_ACCESS_TOKEN_{''.join(c if c.isalnum() else '_' for c in item['channel_id'].upper())}"
    if not env.get(token_name):
        raise RuntimeError(f"{item['channel_id']}: missing GitHub secret/environment variable {token_name}")
    raise RuntimeError(
        f"{item['channel_id']}: live adapter for {platform!r} is not enabled. "
        "Complete official API app review, account OAuth, platform-specific consent, "
        "and status reconciliation before live publishing."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channels", type=Path, default=ROOT / "data" / "channels.json")
    parser.add_argument("--affiliates", type=Path, default=ROOT / "data" / "affiliates.json")
    parser.add_argument("--seasons", type=Path, default=ROOT / "data" / "seasons.json")
    parser.add_argument("--cuts", type=Path, default=ROOT / "data" / "cuts.json")
    parser.add_argument("--receipts", type=Path, default=RECEIPTS_PATH)
    parser.add_argument("--dry-run", action="store_true", help="validate and print a plan; never call platform APIs")
    parser.add_argument("--publish", action="store_true", help="request live publishing; fails closed until an adapter is approved")
    parser.add_argument("--confirm-live", action="store_true", help="additional acknowledgement required with --publish")
    args = parser.parse_args()
    if args.publish and not args.confirm_live:
        print("LIVE PUBLISH BLOCKED: pass --confirm-live as a separate explicit acknowledgement.", file=sys.stderr)
        return 2
    if not args.dry_run and not args.publish:
        print("Choose --dry-run or --publish --confirm-live.", file=sys.stderr)
        return 2
    try:
        channels_doc = read_json(args.channels)
        cuts = validate_inputs(channels_doc, read_json(args.affiliates), read_json(args.seasons), read_json(args.cuts))
        plan = build_plan(channels_doc, cuts)
        if args.dry_run:
            print(json.dumps({
                "mode": "dry-run",
                "created_at_utc": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
                "approved_cut_count": len(plan),
                "network_calls": 0,
                "posts_sent": 0,
                "plan": plan,
            }, indent=2, ensure_ascii=False))
            return 0
        if os.environ.get("PUBLISHING_ENABLED") != "true":
            raise RuntimeError("live publishing is disabled; PUBLISHING_ENABLED must be explicitly set to true")
        # Intentionally no fallback or unofficial posting path.
        for item in plan:
            publish_one(item)
        return 0
    except (OSError, json.JSONDecodeError, ValueError, RuntimeError) as exc:
        print(f"PUBLISHER BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
