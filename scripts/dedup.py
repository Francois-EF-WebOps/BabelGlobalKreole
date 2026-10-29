#!/usr/bin/env python3
"""Validate cut overlap within a channel saga; no publishing is performed."""
from __future__ import annotations


def validate_no_overlaps(cuts: list[dict]) -> None:
    """Raise ValueError for overlapping source ranges or reused hashes in a channel saga."""
    by_season: dict[tuple[str, str], list[tuple[float, float, str]]] = {}
    hashes: dict[tuple[str, str], tuple[str, str]] = {}
    for cut in cuts:
        channel = cut.get("channel_id")
        season = cut.get("parent_season_id")
        cut_id = cut.get("cut_id", "<unknown>")
        cut_hash = cut.get("cut_hash")
        if not isinstance(channel, str) or not channel or not isinstance(season, str) or not season:
            raise ValueError(f"{cut_id}: channel_id and parent_season_id are required")
        if not isinstance(cut_hash, str) or not cut_hash.strip():
            raise ValueError(f"{cut_id}: cut_hash is required")
        hash_key = (channel, cut_hash)
        previous = hashes.get(hash_key)
        if previous is not None:
            previous_season, previous_id = previous
            if previous_season != season:
                raise ValueError(
                    f"{cut_id}: cut_hash reused across seasons in channel saga "
                    f"({previous_id} in {previous_season}, {cut_id} in {season})"
                )
            raise ValueError(f"{cut_id}: duplicate cut_hash within channel saga ({previous_id})")
        hashes[hash_key] = (season, cut_id)

        source_range = cut.get("attention_source_range")
        if not isinstance(source_range, dict) or "start_seconds" not in source_range or "end_seconds" not in source_range:
            raise ValueError(f"{cut_id}: attention_source_range needs start_seconds and end_seconds")
        start, end = source_range["start_seconds"], source_range["end_seconds"]
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or start < 0 or end <= start:
            raise ValueError(f"{cut_id}: invalid attention_source_range")
        key = (channel, season)
        ranges = by_season.setdefault(key, [])
        for other_start, other_end, other_id in ranges:
            if start < other_end and other_start < end:
                raise ValueError(
                    f"{cut_id}: source range overlaps {other_id} in channel {channel}, season {season}"
                )
        ranges.append((start, end, cut_id))
