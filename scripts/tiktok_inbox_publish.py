#!/usr/bin/env python3
"""Explicitly gated, single-item TikTok inbox-draft uploader.

This command never performs Direct Post. The creator must complete publication in TikTok.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.parse import urlparse

from tiktok_adapter import fetch_post_status, upload_inbox_draft


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--video-url", help="HTTPS video URL hosted on a TikTok-verified domain")
    mode.add_argument("--status", metavar="PUBLISH_ID", help="check a previously returned publish_id")
    args = parser.parse_args()

    if not os.environ.get("TIKTOK_ACCESS_TOKEN"):
        print("BLOCKED: set TIKTOK_ACCESS_TOKEN in the environment; never pass it on the command line.", file=sys.stderr)
        return 2

    try:
        if args.status:
            result = fetch_post_status(args.status)
            print(json.dumps({"mode": "status_check", "data": result}, indent=2, ensure_ascii=False))
            return 0

        if os.environ.get("PUBLISHING_ENABLED") != "true":
            raise RuntimeError("PUBLISHING_ENABLED must be explicitly set to true")
        if os.environ.get("TIKTOK_INBOX_UPLOAD_ENABLED") != "true":
            raise RuntimeError("TIKTOK_INBOX_UPLOAD_ENABLED must be explicitly set to true")
        parsed = urlparse(args.video_url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("video URL must be HTTPS")
        verified_hosts = {
            host.strip().lower()
            for host in os.environ.get("TIKTOK_VERIFIED_VIDEO_HOSTS", "").split(",")
            if host.strip()
        }
        if not verified_hosts:
            raise RuntimeError("TIKTOK_VERIFIED_VIDEO_HOSTS must list the exact verified hostname(s)")
        if parsed.hostname.lower() not in verified_hosts:
            raise ValueError("video URL hostname is not in TIKTOK_VERIFIED_VIDEO_HOSTS")

        result = upload_inbox_draft(args.video_url)
        print(json.dumps({
            "mode": "tiktok_inbox_draft",
            "status": result["status"],
            "publish_id": result["publish_id"],
            "published": False,
            "next_step": "Open TikTok, review the inbox notification, and finish publishing manually."
        }, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
