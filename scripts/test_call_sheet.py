"""Acceptance and negative tests for the manual call-sheet builder."""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_call_sheet", ROOT / "scripts" / "build_call_sheet.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def base_data():
    channels = json.loads((ROOT / "data/channels.json").read_text(encoding="utf-8"))
    affiliates = json.loads((ROOT / "data/affiliates.json").read_text(encoding="utf-8"))
    return channels, affiliates


def sample_bundle(count=1, channel_ids=None):
    channels_doc, affiliates_doc = base_data()
    channels = channels_doc["channels"]
    channel_ids = channel_ids or [channels[0]["channel_id"]]
    seasons = []
    cuts = []
    affiliate_map = {channel["channel_id"]: channel["affiliate_program_id"] for channel in channels}
    language_map = {channel["channel_id"]: channel["primary_language"] for channel in channels}
    for index, channel_id in enumerate(channel_ids):
        season_id = f"SEASON-{index+1}"
        seasons.append({"season_id": season_id, "channel_id": channel_id, "master_id": None, "runtime_seconds": 540})
        for cut_index in range(count):
            cuts.append({
                "cut_id": f"CUT-{index+1}-{cut_index+1}",
                "parent_season_id": season_id,
                "cut_hash": f"hash-{index+1}-{cut_index+1}",
                "runtime_seconds": 20,
                "language": language_map[channel_id],
                "hook_visual": f"Hook {index+1}-{cut_index+1}",
                "product_id": affiliate_map[channel_id],
                "channel_id": channel_id,
                "status": "approved",
                "attention_source_range": {"start_seconds": cut_index * 30, "end_seconds": cut_index * 30 + 20}
            })
    return channels_doc, affiliates_doc, {"seasons": seasons}, {"cuts": cuts}


def test_valid_call_sheet_builds_markdown():
    bundle = sample_bundle(count=2)
    result = MODULE.validate_and_build(*bundle, day="2026-10-29")
    assert "# Manual posting call sheet — 2026-10-29" in result
    assert "| CUT-1-1 |" in result
    assert "no content was published" in result.lower() or "does not publish" in result.lower()


def test_daily_load_exceeded():
    ids = [channel["channel_id"] for channel in base_data()[0]["channels"][:5]]
    bundle = sample_bundle(count=3, channel_ids=ids)
    # 15 approved cuts exceed the global cap even though the per-channel cap is respected.
    with pytest.raises(ValueError, match="daily operator load exceeded"):
        MODULE.validate_and_build(*bundle, day="2026-10-29")


def test_wrong_language():
    bundle = sample_bundle(count=1)
    bundle[3]["cuts"][0]["language"] = "fr" if bundle[3]["cuts"][0]["language"] == "en" else "en"
    with pytest.raises(ValueError, match="wrong language"):
        MODULE.validate_and_build(*bundle, day="2026-10-29")


def test_wrong_affiliate():
    bundle = sample_bundle(count=1)
    bundle[3]["cuts"][0]["product_id"] = "not-the-assigned-program"
    with pytest.raises(ValueError, match="wrong affiliate/product"):
        MODULE.validate_and_build(*bundle, day="2026-10-29")


def test_high_extraction_ratio():
    bundle = sample_bundle(count=12)
    for cut in bundle[3]["cuts"]:
        cut["runtime_seconds"] = 25
    with pytest.raises(ValueError, match="extraction ratio"):
        MODULE.validate_and_build(*bundle, day="2026-10-29")


def test_duplicate_cut_within_saga():
    bundle = sample_bundle(count=1)
    first = bundle[3]["cuts"][0]
    duplicate = copy.deepcopy(first)
    duplicate["cut_id"] = "CUT-DUPLICATE"
    duplicate["parent_season_id"] = "SEASON-OTHER"
    duplicate["cut_hash"] = first["cut_hash"]
    bundle[2]["seasons"].append({"season_id":"SEASON-OTHER","channel_id":first["channel_id"],"master_id":None,"runtime_seconds":540})
    bundle[3]["cuts"].append(duplicate)
    with pytest.raises(ValueError, match="cut_hash reused across seasons"):
        MODULE.validate_and_build(*bundle, day="2026-10-29")


def test_overlapping_attention_ranges_in_same_season_are_rejected():
    bundle = sample_bundle(count=2)
    bundle[3]["cuts"][1]["attention_source_range"] = {"start_seconds": 10, "end_seconds": 40}
    with pytest.raises(ValueError, match="overlaps"):
        MODULE.validate_and_build(*bundle, day="2026-10-29")


def test_unapproved_cuts_are_not_scheduled():
    bundle = sample_bundle(count=1)
    bundle[3]["cuts"][0]["status"] = "draft"
    result = MODULE.validate_and_build(*bundle, day="2026-10-29")
    assert "Approved cuts:** 0" in result
