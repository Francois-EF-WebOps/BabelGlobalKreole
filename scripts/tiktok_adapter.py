"""Minimal TikTok Content Posting API adapter for inbox/draft uploads.

This adapter only uploads a draft to the creator's TikTok inbox. It never performs
Direct Post. A creator must finish and publish the draft in the TikTok app.
The caller must ensure the video URL's domain/prefix is verified with TikTok.

Important: inbox initialization is non-idempotent. If the request outcome is ambiguous,
do not retry it blindly; reconcile using a known publish_id if one was returned.
"""
from __future__ import annotations

import json
import os
from typing import Callable
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

API_BASE = "https://open.tiktokapis.com/v2"
INBOX_INIT_PATH = "/post/publish/inbox/video/init/"
STATUS_PATH = "/post/publish/status/fetch/"


class TikTokAPIError(RuntimeError):
    """TikTok returned a non-ok API error."""


class TikTokOutcomeUnknown(RuntimeError):
    """The network failed after an inbox-init request may have reached TikTok."""


def _json_request(url: str, token: str, payload: dict, *, opener: Callable = urlopen) -> dict:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        method="POST",
    )
    try:
        with opener(request, timeout=30) as response:
            body = response.read()
    except URLError as exc:
        raise TikTokOutcomeUnknown(
            "TikTok request outcome is unknown; do not repeat inbox initialization blindly."
        ) from exc
    try:
        result = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TikTokAPIError("TikTok returned invalid JSON") from exc
    error = result.get("error", {})
    if error.get("code") not in (None, "", "ok"):
        raise TikTokAPIError(
            f"TikTok API error {error.get('code')}: {error.get('message', '')}"
        )
    if not isinstance(result.get("data"), dict):
        raise TikTokAPIError("TikTok response is missing data")
    return result["data"]


def upload_inbox_draft(
    video_url: str,
    *,
    access_token: str | None = None,
    opener: Callable = urlopen,
) -> dict:
    """Initialize an official TikTok inbox upload using a verified HTTPS media URL."""
    token = access_token or os.environ.get("TIKTOK_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing TIKTOK_ACCESS_TOKEN")
    parsed = urlparse(video_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("video_url must be an HTTPS URL on a TikTok-verified domain/prefix")
    data = _json_request(
        API_BASE + INBOX_INIT_PATH,
        token,
        {"source_info": {"source": "PULL_FROM_URL", "video_url": video_url}},
        opener=opener,
    )
    publish_id = data.get("publish_id")
    if not isinstance(publish_id, str) or not publish_id:
        raise TikTokAPIError("TikTok inbox-init response is missing publish_id")
    return {"publish_id": publish_id, "status": "upload_initialized_not_published"}


def fetch_post_status(
    publish_id: str,
    *,
    access_token: str | None = None,
    opener: Callable = urlopen,
) -> dict:
    """Fetch status for a previously returned publish_id; does not initialize a post."""
    token = access_token or os.environ.get("TIKTOK_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing TIKTOK_ACCESS_TOKEN")
    if not isinstance(publish_id, str) or not publish_id.strip():
        raise ValueError("publish_id is required")
    return _json_request(
        API_BASE + STATUS_PATH,
        token,
        {"publish_id": publish_id},
        opener=opener,
    )
