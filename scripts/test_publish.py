"""Tests for validation, dry-run behavior, receipts, and safe retry primitives."""
import importlib.util
import json
from pathlib import Path
from urllib.error import HTTPError
from email.message import Message

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("publish", ROOT / "scripts" / "publish.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def bundle():
    channels = json.loads((ROOT / "data/channels.json").read_text(encoding="utf-8"))
    affiliates = json.loads((ROOT / "data/affiliates.json").read_text(encoding="utf-8"))
    seasons = {"seasons": [{
        "season_id": "S-1", "channel_id": channels["channels"][0]["channel_id"],
        "master_id": None, "runtime_seconds": 540
    }]}
    channel = channels["channels"][0]
    cuts = {"cuts": [{
        "cut_id": "CUT-1", "parent_season_id": "S-1", "cut_hash": "hash-1",
        "runtime_seconds": 20, "language": channel["primary_language"],
        "hook_visual": "A real test hook", "product_id": channel["affiliate_program_id"],
        "channel_id": channel["channel_id"], "status": "approved",
        "attention_source_range": {"start_seconds": 0, "end_seconds": 20},
        "video_url": "https://media.example.test/cut-1.mp4"
    }]}
    return channels, affiliates, seasons, cuts


def test_valid_approved_cut_produces_plan_without_network_calls():
    channels, affiliates, seasons, cuts_doc = bundle()
    approved = MODULE.validate_inputs(channels, affiliates, seasons, cuts_doc)
    plan = MODULE.build_plan(channels, approved)
    assert len(plan) == 1
    assert plan[0]["status"] == "planned_not_sent"
    assert plan[0]["video_url"].startswith("https://")
    assert plan[0]["platform"] == "tiktok"


def test_missing_video_url_is_rejected_before_network():
    channels, affiliates, seasons, cuts_doc = bundle()
    del cuts_doc["cuts"][0]["video_url"]
    with pytest.raises(ValueError, match="requires video_url"):
        MODULE.validate_inputs(channels, affiliates, seasons, cuts_doc)


def test_non_https_video_url_is_rejected():
    channels, affiliates, seasons, cuts_doc = bundle()
    cuts_doc["cuts"][0]["video_url"] = "http://media.example.test/video.mp4"
    with pytest.raises(ValueError, match="public HTTPS"):
        MODULE.validate_inputs(channels, affiliates, seasons, cuts_doc)


def test_live_adapter_fails_closed_even_with_token():
    item = {"channel_id": "f.i.n.l.e.y.1", "platform": "tiktok"}
    with pytest.raises(RuntimeError, match="adapter.*not enabled"):
        MODULE.publish_one(item, environment={"TIKTOK_ACCESS_TOKEN_F_I_N_L_E_Y_1": "not-a-real-token"})


def test_receipt_does_not_erase_confirmed_url(tmp_path):
    path = tmp_path / "receipts.json"
    path.write_text(json.dumps({"receipts": [{
        "cut_id": "CUT-1", "channel_id": "channel-1",
        "status": "published", "platform_post_url": "https://platform.test/post/1"
    }]}), encoding="utf-8")
    with pytest.raises(ValueError, match="refusing to overwrite"):
        MODULE.write_receipt(path, {
            "cut_id": "CUT-1", "channel_id": "channel-1",
            "status": "not_sent", "platform_post_url": None
        })


def test_429_retry_uses_retry_after_and_retries():
    headers = Message()
    headers["Retry-After"] = "3"
    calls = {"count": 0}
    sleeps = []
    class Response:
        status = 200
    def opener(request, timeout):
        calls["count"] += 1
        if calls["count"] == 1:
            raise HTTPError(request.full_url, 429, "rate limit", headers, None)
        return Response()
    from urllib.request import Request\n    result = MODULE.request_with_backoff(Request("https://example.test/"), opener=opener, sleep=sleeps.append, retries=2)
    assert result.status == 200
    assert calls["count"] == 2
    assert sleeps == [3.0]


def test_empty_production_inventory_is_safe():
    channels = json.loads((ROOT / "data/channels.json").read_text(encoding="utf-8"))
    affiliates = json.loads((ROOT / "data/affiliates.json").read_text(encoding="utf-8"))
    seasons = json.loads((ROOT / "data/seasons.json").read_text(encoding="utf-8"))
    cuts = json.loads((ROOT / "data/cuts.json").read_text(encoding="utf-8"))
    assert MODULE.validate_inputs(channels, affiliates, seasons, cuts) == []
    assert MODULE.build_plan(channels, []) == []
