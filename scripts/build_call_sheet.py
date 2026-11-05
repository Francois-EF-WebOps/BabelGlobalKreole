#!/usr/bin/env python3
"""Build today's manual posting call sheet. This script never publishes content."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

from dedup import validate_no_overlaps

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_and_build(channels_doc: dict, affiliates_doc: dict, seasons_doc: dict, cuts_doc: dict, day: str | None = None) -> str:
    policy = channels_doc.get("policy", {})
    channels = channels_doc.get("channels")
    affiliates = affiliates_doc.get("affiliates")
    seasons = seasons_doc.get("seasons")
    cuts = cuts_doc.get("cuts")
    if not all(isinstance(value, list) for value in (channels, affiliates, seasons, cuts)):
        raise ValueError("channels, affiliates, seasons, and cuts must each be arrays")
    for name, rows, key in (
        ("channel", channels, "channel_id"),
        ("affiliate", affiliates, "program_id"),
        ("season", seasons, "season_id"),
        ("cut", cuts, "cut_id"),
    ):
        values = [row.get(key) for row in rows]
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError(f"every {name} needs a non-empty {key}")
        if len(values) != len(set(values)):
            raise ValueError(f"duplicate {name} {key}")
    channel_map = {row["channel_id"]: row for row in channels}
    affiliate_ids = {row["program_id"] for row in affiliates}
    season_map = {row["season_id"]: row for row in seasons}
    if len(channel_map) != 11:
        raise ValueError("expected exactly 11 registered channels")
    global_cap = int(policy.get("daily_operator_load_cap", 12))
    default_channel_cap = int(policy.get("per_channel_cap", 3))
    max_cuts_per_season = int(policy.get("max_cuts_per_season", 12))
    max_ratio = float(policy.get("max_extraction_ratio", 0.45))

    approved = [cut for cut in cuts if cut.get("status") == "approved"]
    # Validate all cuts for accidental reuse/overlap, including drafts, before scheduling.
    validate_no_overlaps(cuts)
    if len(approved) > global_cap:
        raise ValueError(f"daily operator load exceeded: {len(approved)} approved cuts > {global_cap}")

    counts: dict[str, int] = {}
    season_cuts: dict[str, list[dict]] = {}
    for cut in approved:
        cut_id = cut.get("cut_id", "<unknown>")
        channel_id = cut.get("channel_id")
        if channel_id not in channel_map:
            raise ValueError(f"{cut_id}: unknown channel_id {channel_id!r}")
        channel = channel_map[channel_id]
        counts[channel_id] = counts.get(channel_id, 0) + 1
        cap = min(int(channel.get("daily_cap", default_channel_cap)), default_channel_cap)
        if counts[channel_id] > cap:
            raise ValueError(f"{channel_id}: per-channel cap exceeded ({counts[channel_id]} > {cap})")
        if cut.get("language") != channel.get("primary_language"):
            raise ValueError(f"{cut_id}: wrong language for {channel_id}")
        if cut.get("product_id") != channel.get("affiliate_program_id"):
            raise ValueError(f"{cut_id}: wrong affiliate/product for {channel_id}")
        if channel.get("affiliate_program_id") not in affiliate_ids:
            raise ValueError(f"{channel_id}: affiliate program is not registered")
        season_id = cut.get("parent_season_id")
        if season_id not in season_map:
            raise ValueError(f"{cut_id}: unknown parent season {season_id!r}")
        season = season_map[season_id]
        if season.get("channel_id") != channel_id:
            raise ValueError(f"{cut_id}: season belongs to a different channel")
        runtime = cut.get("runtime_seconds")
        if not isinstance(runtime, int) or runtime <= 0:
            raise ValueError(f"{cut_id}: runtime_seconds must be a positive integer")
        if not isinstance(cut.get("hook_visual"), str) or not cut["hook_visual"].strip():
            raise ValueError(f"{cut_id}: hook_visual is required")
        if cut.get("status") != "approved":
            raise ValueError(f"{cut_id}: only approved cuts can be scheduled")
        season_cuts.setdefault(season_id, []).append(cut)

    for season_id, season_rows in season_cuts.items():
        season = season_map[season_id]
        season_runtime = season.get("runtime_seconds")
        if not isinstance(season_runtime, int) or season_runtime <= 0:
            raise ValueError(f"{season_id}: runtime_seconds must be a positive integer")
        if len(season_rows) > max_cuts_per_season:
            raise ValueError(f"{season_id}: exceeds maximum {max_cuts_per_season} cuts")
        total_cut_runtime = sum(cut["runtime_seconds"] for cut in season_rows)
        ratio = total_cut_runtime / season_runtime
        if ratio > max_ratio:
            raise ValueError(
                f"{season_id}: extraction ratio {ratio:.3f} exceeds {max_ratio:.0%}"
            )

    timezone_name = str(policy.get("operator_timezone", "UTC"))
    try:
        today = day or datetime.now(ZoneInfo(timezone_name)).date().isoformat()
    except Exception as exc:
        raise ValueError(f"invalid operator_timezone: {timezone_name}") from exc
    try:
        date.fromisoformat(today)
    except ValueError as exc:
        raise ValueError("day must be an ISO date YYYY-MM-DD") from exc
    start = datetime.strptime(str(policy.get("default_first_post_time", "09:00")), "%H:%M")
    gap = int(policy.get("minutes_between_posts", 60))
    lines = [
        f"# Manual posting call sheet — {today}",
        "",
        f"**Approved cuts:** {len(approved)} / {global_cap} daily operator limit",
        "**Publishing:** manual only; this file does not publish or confirm a post.",
        "",
        "| Done | Time (operator local time) | Handle | Cut ID | Hook | Product / affiliate | Link to post |",
        "|---|---|---|---|---|---|---|",
    ]
    ordered = sorted(approved, key=lambda cut: (cut.get("channel_id", ""), cut.get("cut_id", "")))
    for index, cut in enumerate(ordered):
        channel = channel_map[cut["channel_id"]]
        scheduled = start + timedelta(minutes=gap * index)
        hook = cut["hook_visual"].replace("|", "\\|").replace("\n", " ")
        product = str(cut["product_id"]).replace("|", "\\|")
        lines.append(
            f"| [ ] | {scheduled.strftime('%H:%M')} | @{channel['channel_id']} "
            f"| {cut['cut_id']} | {hook} | {product} | Add actual post URL after manual publication |"
        )
    if not approved:
        lines.extend(["", "No approved cuts are scheduled. Add and validate real content before posting."])
    lines.extend(["", "After posting, record the actual URL and time. Never mark a cut published merely because it appears on this call sheet.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", help="Call-sheet date, YYYY-MM-DD (defaults to today)")
    parser.add_argument("--output", type=Path, default=ROOT / "today.md")
    parser.add_argument("--channels", type=Path, default=ROOT / "data" / "channels.json")
    parser.add_argument("--affiliates", type=Path, default=ROOT / "data" / "affiliates.json")
    parser.add_argument("--seasons", type=Path, default=ROOT / "data" / "seasons.json")
    parser.add_argument("--cuts", type=Path, default=ROOT / "data" / "cuts.json")
    args = parser.parse_args()
    try:
        markdown = validate_and_build(
            read_json(args.channels), read_json(args.affiliates),
            read_json(args.seasons), read_json(args.cuts), args.day
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"CALL SHEET BUILD FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"Call sheet written to {args.output}; no content was published.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
