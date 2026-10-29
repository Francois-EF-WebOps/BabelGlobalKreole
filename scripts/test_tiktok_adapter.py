"""Mock-only tests for the TikTok official inbox adapter; no network calls."""
import importlib.util
import json
from pathlib import Path
from urllib.error import URLError

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("tiktok_adapter", ROOT / "scripts" / "tiktok_adapter.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Response:
    def __init__(self, body):
        self.body = json.dumps(body).encode()
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self):
        return self.body


def test_inbox_upload_uses_official_endpoint_and_never_claims_published():
    seen = {}
    def opener(request, timeout):
        seen["url"] = request.full_url
        seen["method"] = request.method
        seen["payload"] = json.loads(request.data.decode())
        seen["auth"] = request.get_header("Authorization")
        return Response({"data": {"publish_id": "draft-123"}, "error": {"code": "ok"}})
    result = MODULE.upload_inbox_draft(
        "https://verified.example.test/cut.mp4", access_token="test-token", opener=opener
    )
    assert seen["url"].endswith("/post/publish/inbox/video/init/")
    assert seen["method"] == "POST"
    assert seen["payload"]["source_info"]["source"] == "PULL_FROM_URL"
    assert seen["payload"]["source_info"]["video_url"] == "https://verified.example.test/cut.mp4"
    assert seen["auth"] == "Bearer test-token"
    assert result == {"publish_id": "draft-123", "status": "upload_initialized_not_published"}


@pytest.mark.parametrize("url", ["http://example.test/video.mp4", "file:///tmp/video.mp4", "not-a-url"])
def test_inbox_upload_rejects_non_https_urls_before_network(url):
    def forbidden(*args, **kwargs):
        raise AssertionError("network must not be called")
    with pytest.raises(ValueError, match="HTTPS"):
        MODULE.upload_inbox_draft(url, access_token="test-token", opener=forbidden)


def test_missing_token_is_rejected():
    with pytest.raises(ValueError, match="TIKTOK_ACCESS_TOKEN"):
        MODULE.upload_inbox_draft("https://verified.example.test/cut.mp4", access_token="")


def test_ambiguous_network_failure_is_not_retried():
    calls = {"count": 0}
    def opener(request, timeout):
        calls["count"] += 1
        raise URLError("connection reset")
    with pytest.raises(MODULE.TikTokOutcomeUnknown, match="do not repeat"):
        MODULE.upload_inbox_draft(
            "https://verified.example.test/cut.mp4", access_token="test-token", opener=opener
        )
    assert calls["count"] == 1


def test_status_fetch_uses_existing_publish_id():
    seen = {}
    def opener(request, timeout):
        seen["url"] = request.full_url
        seen["payload"] = json.loads(request.data.decode())
        return Response({"data": {"status": "PROCESSING_UPLOAD"}, "error": {"code": "ok"}})
    result = MODULE.fetch_post_status("draft-123", access_token="test-token", opener=opener)
    assert seen["url"].endswith("/post/publish/status/fetch/")
    assert seen["payload"] == {"publish_id": "draft-123"}
    assert result["status"] == "PROCESSING_UPLOAD"


def test_api_error_is_reported():
    def opener(request, timeout):
        return Response({"data": {}, "error": {"code": "scope_not_authorized", "message": "missing scope"}})
    with pytest.raises(MODULE.TikTokAPIError, match="scope_not_authorized"):
        MODULE.upload_inbox_draft(
            "https://verified.example.test/cut.mp4", access_token="test-token", opener=opener
        )
