"""Mock tests for TikTok Direct Post preflight and safety gates."""
import importlib.util, json
from pathlib import Path
from urllib.error import URLError
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("tiktok_direct_post_adapter", ROOT / "scripts" / "tiktok_direct_post_adapter.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class Response:
    def __init__(self, body): self.body = json.dumps(body).encode()
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self): return self.body

def ok(data): return {"data": data, "error": {"code": "ok", "message": ""}}

def test_direct_post_queries_creator_first_and_initializes_once():
    calls = []
    def opener(request, timeout):
        payload = json.loads(request.data.decode())
        calls.append((request.full_url, payload))
        if request.full_url.endswith("/creator_info/query/"):
            return Response(ok({"privacy_level_options": ["SELF_ONLY", "PUBLIC_TO_EVERYONE"]}))
        return Response(ok({"publish_id": "pub-test-123"}))
    result = MODULE.direct_post_from_url("https://verified.example/video.mp4", "First test", "SELF_ONLY",
        explicit_consent=True, access_token="test-token", opener=opener)
    assert result["publish_id"] == "pub-test-123" and result["published"] is False
    assert calls[0][0].endswith("/creator_info/query/") and calls[1][0].endswith("/video/init/")
    assert calls[1][1]["source_info"]["video_url"] == "https://verified.example/video.mp4"
    assert calls[1][1]["post_info"]["privacy_level"] == "SELF_ONLY"

def test_no_explicit_consent_means_no_network_call():
    calls = []
    with pytest.raises(ValueError, match="consent"):
        MODULE.direct_post_from_url("https://verified.example/video.mp4", "Test", "SELF_ONLY",
            explicit_consent=False, access_token="test-token", opener=lambda *a, **k: calls.append(1))
    assert calls == []

def test_privacy_must_be_in_latest_creator_options():
    def opener(request, timeout): return Response(ok({"privacy_level_options": ["SELF_ONLY"]}))
    with pytest.raises(ValueError, match="latest creator_info"):
        MODULE.direct_post_from_url("https://verified.example/video.mp4", "Test", "PUBLIC_TO_EVERYONE",
            explicit_consent=True, access_token="test-token", opener=opener)

def test_non_https_url_rejected_before_network():
    calls = []
    with pytest.raises(ValueError, match="HTTPS"):
        MODULE.direct_post_from_url("http://example.test/video.mp4", "Test", "SELF_ONLY",
            explicit_consent=True, access_token="test-token", opener=lambda *a, **k: calls.append(1))
    assert calls == []

def test_ambiguous_network_failure_is_not_retried():
    calls = []
    def opener(request, timeout):
        calls.append(request.full_url)
        if request.full_url.endswith("/creator_info/query/"):
            return Response(ok({"privacy_level_options": ["SELF_ONLY"]}))
        raise URLError("connection lost")
    with pytest.raises(MODULE.TikTokOutcomeUnknown):
        MODULE.direct_post_from_url("https://verified.example/video.mp4", "Test", "SELF_ONLY",
            explicit_consent=True, access_token="test-token", opener=opener)
    assert len(calls) == 2
