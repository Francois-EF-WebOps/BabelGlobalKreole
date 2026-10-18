#!/usr/bin/env python3
"""Build a zero-dependency, multi-channel package from one approved source record."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "distribution" / "source.json"
PUBLIC_STATUS = "approved_for_publication"


def validate_source(data: dict) -> dict:
    required = (
        "id", "slug", "title", "summary", "audience", "language", "jurisdiction",
        "created_at", "status", "rights_status", "canonical_source", "body_markdown",
        "sources", "review_trigger", "distribution",
    )
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError("missing required fields: " + ", ".join(missing))
    for key in ("id", "slug", "title", "summary", "audience", "language", "jurisdiction",
                "rights_status", "canonical_source", "body_markdown", "review_trigger"):
        if not isinstance(data[key], str) or not data[key].strip():
            raise ValueError(f"{key} must be a non-empty string")
    if data["status"] != PUBLIC_STATUS:
        raise ValueError(f"publication blocked: status must equal {PUBLIC_STATUS!r}")
    if data["rights_status"] != "owner_authored_summary_of_this_repository":
        raise ValueError("publication blocked: rights_status is not an explicitly allowed value")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", data["slug"]):
        raise ValueError("slug must contain lowercase letters, digits, and hyphens only")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data["created_at"]):
        raise ValueError("created_at must use YYYY-MM-DD")
    try:
        datetime.strptime(data["created_at"], "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("created_at is not a valid date") from exc
    parsed = urlparse(data["canonical_source"])
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("canonical_source must be an absolute HTTPS URL")
    if not isinstance(data["sources"], list) or not data["sources"]:
        raise ValueError("at least one source is required")
    for item in data["sources"]:
        if not isinstance(item, dict) or not item.get("label") or not item.get("url"):
            raise ValueError("each source needs a label and URL")
        parsed = urlparse(item["url"])
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("source URLs must be absolute HTTPS URLs")
    if not isinstance(data["distribution"], dict) or not all(
        data["distribution"].get(k) is True for k in ("website", "rss", "json")
    ):
        raise ValueError("website, RSS, and JSON channels must be explicitly enabled")
    if not re.search(r"(?im)^##?\s+Sources and status\s*$", data["body_markdown"]):
        raise ValueError("body must contain a 'Sources and status' section")
    return data


def load_source(path: Path) -> dict:
    return validate_source(json.loads(path.read_text(encoding="utf-8")))


def markdown_to_html(markdown: str) -> str:
    """Small safe subset renderer: headings, paragraphs, unordered lists, and links."""
    output = []
    in_list = False
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            if in_list:
                output.append("</ul>")
                in_list = False
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            if in_list:
                output.append("</ul>")
                in_list = False
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline_markup(heading.group(2))}</h{level}>")
        elif line.startswith("- "):
            if not in_list:
                output.append("<ul>")
                in_list = True
            output.append(f"<li>{inline_markup(line[2:])}</li>")
        else:
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<p>{inline_markup(line)}</p>")
    if in_list:
        output.append("</ul>")
    return "\n".join(output)


def inline_markup(text: str) -> str:
    escaped = html.escape(text, quote=True)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    def link_replacement(match):
        label, target = match.group(1), match.group(2)
        parsed = urlparse(html.unescape(target))
        if parsed.scheme != "https" or not parsed.netloc:
            return label
        return f'<a href="{html.escape(target, quote=True)}" rel="noopener noreferrer">{label}</a>'
    escaped = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link_replacement, escaped)
    return escaped


def xml_text(parent: ET.Element, tag: str, value: str) -> None:
    child = ET.SubElement(parent, tag)
    child.text = value


def build(source: dict, output_dir: Path, base_url: str) -> dict:
    validate_source(source)
    base = base_url.rstrip("/")
    article_url = f"{base}/distribution/"
    output_dir.mkdir(parents=True, exist_ok=True)
    article_dir = output_dir / "distribution"
    article_dir.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0)
    source_links = "\n".join(
        f'<li><a href="{html.escape(s["url"], quote=True)}" rel="noopener noreferrer">{html.escape(s["label"])}</a></li>'
        for s in source["sources"]
    )
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(source["title"])}</title>
<meta name="description" content="{html.escape(source["summary"], quote=True)}">
<link rel="canonical" href="{html.escape(article_url, quote=True)}">
<link rel="alternate" type="application/rss+xml" title="BabelGlobalKreole RSS" href="{html.escape(base + "/feed.xml", quote=True)}">
<meta property="og:title" content="{html.escape(source["title"], quote=True)}">
<meta property="og:description" content="{html.escape(source["summary"], quote=True)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{html.escape(article_url, quote=True)}">
<style>
body{{font:18px/1.65 system-ui,sans-serif;max-width:780px;margin:0 auto;padding:1.25rem;color:#17202a}}
header,footer{{border-bottom:1px solid #ddd;padding-bottom:1rem;margin-bottom:1.5rem}}
footer{{border-top:1px solid #ddd;border-bottom:0;padding-top:1rem;font-size:.9rem}}
a{{overflow-wrap:anywhere}}li{{margin:.35rem 0}}.meta{{color:#555;font-size:.92rem}}
</style>
</head>
<body>
<header><p><a href="{html.escape(base + "/", quote=True)}">BabelGlobalKreole</a> / Public distribution</p>
<h1>{html.escape(source["title"])}</h1>
<p>{html.escape(source["summary"])}</p>
<p class="meta">Audience: {html.escape(source["audience"])} · Language: {html.escape(source["language"])} · Updated from source: {html.escape(source["created_at"])}</p></header>
<main>{markdown_to_html(source["body_markdown"])}
<h2>References</h2><ul>{source_links}</ul>
<p class="meta">Review trigger: {html.escape(source["review_trigger"])}</p>
<p class="meta">Canonical source: <a href="{html.escape(source["canonical_source"], quote=True)}">{html.escape(source["canonical_source"])}</a></p>
</main>
<footer><p>Generated from source record {html.escape(source["id"])}. This summary does not replace the cited sources.</p><p><a href="{html.escape(base + "/feed.xml", quote=True)}">RSS feed</a> · <a href="{html.escape(base + "/distribution/source.json", quote=True)}">Machine-readable source record</a></p></footer>
</body></html>
"""
    (article_dir / "index.html").write_text(page, encoding="utf-8")
    (article_dir / "source.json").write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    xml_text(channel, "title", "BabelGlobalKreole — public knowledge")
    xml_text(channel, "link", base + "/")
    xml_text(channel, "description", "Source-linked public updates from BabelGlobalKreole.")
    xml_text(channel, "lastBuildDate", format_datetime(generated_at))
    item = ET.SubElement(channel, "item")
    xml_text(item, "title", source["title"])
    xml_text(item, "link", article_url)
    xml_text(item, "guid", article_url)
    xml_text(item, "description", source["summary"])
    xml_text(item, "pubDate", format_datetime(datetime.strptime(source["created_at"], "%Y-%m-%d").replace(tzinfo=timezone.utc)))
    ET.indent(rss, space="  ")
    (output_dir / "feed.xml").write_bytes(ET.tostring(rss, encoding="utf-8", xml_declaration=True))

    social = (
        f'{source["title"]}\n\n{source["summary"]}\n\nRead the source-linked overview: {article_url}\n'
        f'Project source: {source["canonical_source"]}\n'
    )
    newsletter = (
        f'Subject: {source["title"]}\n\n'
        f'{source["summary"]}\n\n'
        f'Read the full overview: {article_url}\n\n'
        f'Why it matters: the page separates the project’s intended scope from claims it does not make, and links readers to the underlying project policies.\n'
    )
    (article_dir / "social-post.txt").write_text(social, encoding="utf-8")
    (article_dir / "newsletter.txt").write_text(newsletter, encoding="utf-8")

    manifest = {
        "source_id": source["id"],
        "source_path": "distribution/source.json",
        "generated_at_utc": generated_at.isoformat(),
        "base_url": base,
        "outputs": {
            "website": article_url,
            "rss": base + "/feed.xml",
            "json": base + "/distribution/source.json",
            "social_copy": base + "/distribution/social-post.txt",
            "newsletter_copy": base + "/distribution/newsletter.txt"
        },
        "delivery_status": {
            "website": "built; public availability depends on successful Pages deployment",
            "rss": "built; public availability depends on successful Pages deployment",
            "json": "built; public availability depends on successful Pages deployment",
            "social_post": "copy generated; no social API credentials or account posting configured",
            "newsletter": "copy generated; no email delivery provider configured"
        },
        "metrics": {
            "source_records": 1,
            "channel_assets_generated": 5,
            "page_views": None,
            "rss_subscribers": None,
            "social_reach": None,
            "revenue": None
        }
    }
    (article_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    landing = output_dir / "index.html"
    if landing.exists():
        existing = landing.read_text(encoding="utf-8")
        feed_link = f'<link rel="alternate" type="application/rss+xml" title="BabelGlobalKreole RSS" href="{html.escape(base + "/feed.xml", quote=True)}">'
        if "BabelGlobalKreole RSS" not in existing and "</head>" in existing:
            existing = existing.replace("</head>", feed_link + "\n</head>", 1)
        nav_link = f'<p><a href="{html.escape(article_url, quote=True)}">Latest distributed knowledge brief: {html.escape(source["title"])}</a></p>'
        if "Latest distributed knowledge brief:" not in existing and "</body>" in existing:
            existing = existing.replace("</body>", nav_link + "\n</body>", 1)
        landing.write_text(existing, encoding="utf-8")

    sitemap = output_dir / "sitemap.xml"
    if sitemap.exists():
        tree = ET.parse(sitemap)
        root = tree.getroot()
        ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        existing_locs = {el.text for el in root.findall(f"{namespace}url/{namespace}loc")}
        for url in (article_url, base + "/feed.xml"):
            if url not in existing_locs:
                node = ET.SubElement(root, namespace + "url")
                loc = ET.SubElement(node, namespace + "loc")
                loc.text = url
        ET.indent(tree, space="  ")
        tree.write(sitemap, encoding="utf-8", xml_declaration=True)

    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    try:
        source = load_source(args.source)
        manifest = build(source, args.output_dir, args.base_url)
    except (OSError, json.JSONDecodeError, ValueError, ET.ParseError) as exc:
        print(f"DISTRIBUTION BUILD FAILED: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "built", "source_id": source["id"], "outputs": manifest["outputs"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
