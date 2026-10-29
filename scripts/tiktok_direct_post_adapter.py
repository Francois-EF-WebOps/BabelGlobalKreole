"""TikTok Content Posting API Direct Post adapter.

This module initializes a direct video post only after creator-info preflight and explicit
caller consent. Public visibility still depends on TikTok app audit and account permissions.
"""
from __future__ import annotations

import json
import os
from typing import Callable
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

API_BASE = "https://open.tiktokapis.com/v2"
CREATOR_INFO_PATH = "/post/publish/creator_info/query/"
DIRECT_INIT_PATH = "/post/publish/video/init/"
STATUS_PATH = "/post/publish/status/fetch/"
VALID_PRIVACY = {
    "PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "FOLLOWER_OF_CREATOR", "SELF_ONLY"
}


class TikTokAPIError(RuntimeError):
    """TikTok returned an API error or an incomplete response."""


class TikTokOutcomeUnknown(RuntimeError):
    """The request may have reached TikTok; reconcile before retrying."""


def _request(path: str, payload: dict, *, access_token: str | None = None,
             opener: Callable = urlopen) -> dict:
    token = access_token or os.environ.get("TIKTOK_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing TIKTOK_ACCESS_TOKEN")
    req = Request(
        API_BASE + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        method="POST",
    )
    try:
        with opener(req, timeout=30) as response:
            raw = response.read()
    except URLError as exc:
        raise TikTokOutcomeUnknown(
            "TikTok request outcome is unknown; do not retry post initialization blindly."
        ) from exc
    try:
        result = json.loads(raw.decode("utf-8"))
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


def query_creator_info(*, access_token: str | None = None,
                       opener: Callable = urlopen) -> dict:
    """Fetch current creator settings; required before a Direct Post attempt."""
    data = _request(CREATOR_INFO_PATH, {}, access_token=access_token, opener=opener)
    if not isinstance(data.get("privacy_level_options"), list):
        raise TikTokAPIError("Creator info is missing privacy_level_options")
    return data


def direct_post_from_url(video_url: str, caption: str, privacy_level: str, *,
                         explicit_consent: bool,
                         disable_comment: bool = False,
                         disable_duet: bool = False,
                         disable_stitch: bool = False,
                         is_aigc: bool = False,
                         access_token: str | None = None,
                         opener: Callable = urlopen) -> dict:
    """Initialize one Direct Post using a verified HTTPS media URL.

    This does not claim publication completion; callers must poll the returned publish_id.
    The caller must show the creator information and capture the user's consent in a compliant
    interface before calling this function.
    """
    if explicit_consent is not True:
        raise ValueError("Explicit creator consent is required for every post")
    if not isinstance(caption, str) or len(caption.encode("utf-16-le")) // 2 > 2200:
        raise ValueError("caption must be text of at most 2200 UTF-16 code units")
    parsed = urlparse(video_url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("video_url must be HTTPS on a TikTok-verified domain/prefix")
    if privacy_level not in VALID_PRIVACY:
        raise ValueError("Unsupported privacy_level")
    creator = query_creator_info(access_token=access_token, opener=opener)
    if privacy_level not in creator["privacy_level_options"]:
        raise ValueError("privacy_level must be one of the latest creator_info options")
    payload = {
        "post_info": {
            "title": caption,
            "privacy_level": privacy_level,
            "disable_comment": bool(disable_comment),
            "disable_duet": bool(disable_duet),
            "disable_stitch": bool(disable_stitch),
            "is_aigc": bool(is_aigc),
        },
        "source_info": {"source": "PULL_FROM_URL", "video_url": video_url},
    }
    data = _request(DIRECT_INIT_PATH, payload, access_token=access_token, opener=opener)
    publish_id = data.get("publish_id")
    if not isinstance(publish_id, str) or not publish_id:
        raise TikTokAPIError("TikTok direct-post response is missing publish_id")
    return {
        "publish_id": publish_id,
        "status": "post_initialized_pending_processing",
        "privacy_level": privacy_level,
        "published": False,
    }


def fetch_post_status(publish_id: str, *, access_token: str | None = None,
                      opener: Callable = urlopen) -> dict:
    if not isinstance(publish_id, str) or not publish_id.strip():
        raise ValueError("publish_id is required")
    return _request(STATUS_PATH, {"publish_id": publish_id},
                    access_token=access_token, opener=opener)
