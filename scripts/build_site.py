#!/usr/bin/env python3
"""Build a small metadata landing site with absolute sitemap and JSON-LD URLs."""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import urljoin
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_URL = "https://github.com/Francois-EF-WebOps/BabelGlobalKreole"


def build(base_url, output_dir):
    base_url = base_url.rstrip("/")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    counts = catalog["record_counts"]
    description = (
        "A public, evidence-grounded knowledge and interoperability layer for Creole languages. "
        "It links to existing resources, separates sourced evidence from creative output, "
        "and does not claim to be a complete corpus or a single universal Creole."
    )
    dataset = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "Babel / Global (K)Creole",
        "description": description,
        "url": base_url + "/",
        "identifier": REPOSITORY_URL,
        "creator": {
            "@type": "Organization",
            "name": "Francois-EF-WebOps",
            "url": "https://github.com/Francois-EF-WebOps",
        },
        "keywords": [
            "Creole languages",
            "language documentation",
            "language data interoperability",
            "provenance",
            "responsible AI use",
        ],
        "distribution": [{
            "@type": "DataDownload",
            "name": "Machine-readable record catalog",
            "encodingFormat": "application/json",
            "contentUrl": "https://raw.githubusercontent.com/Francois-EF-WebOps/BabelGlobalKreole/main/catalog.json",
        }],
        "additionalProperty": [
            {"@type": "PropertyValue", "name": name, "value": value}
            for name, value in counts.items()
        ],
    }
    jsonld = json.dumps(dataset, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    links = [
        ("Repository and source history", REPOSITORY_URL),
        ("Machine-readable catalog", REPOSITORY_URL + "/blob/main/catalog.json"),
        ("LLM discovery file", REPOSITORY_URL + "/blob/main/llms.txt"),
        ("Evidence policy", REPOSITORY_URL + "/blob/main/docs/evidence-policy.md"),
        ("Data model and IDs", REPOSITORY_URL + "/blob/main/docs/data-model.md"),
        ("External resource cards", REPOSITORY_URL + "/blob/main/data/resources/resources.jsonl"),
        ("Consumer-agent contract", REPOSITORY_URL + "/blob/main/agents/consumer-agent-contract.md"),
        ("Offline retrieval demo", REPOSITORY_URL + "/blob/main/demo/retrieval/README.md"),
        ("Contributing guide", REPOSITORY_URL + "/blob/main/CONTRIBUTING.md"),
    ]
    link_html = "\n".join(
        f'<li><a href="{html.escape(url, quote=True)}">{html.escape(label)}</a></li>'
        for label, url in links
    )
    count_html = "\n".join(
        f"<li><strong>{html.escape(name.replace('_', ' ').capitalize())}:</strong> {value}</li>"
        for name, value in counts.items()
    )
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Babel / Global (K)Creole — evidence and interoperability</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<link rel="canonical" href="{html.escape(base_url + '/', quote=True)}">
<meta property="og:title" content="Babel / Global (K)Creole">
<meta property="og:description" content="{html.escape(description, quote=True)}">
<meta property="og:type" content="website">
<script type="application/ld+json">{jsonld}</script>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.6;max-width:900px;margin:0 auto;padding:1.5rem;color:#202124}}
h1,h2{{line-height:1.2}} a{{overflow-wrap:anywhere}} .notice{{border-left:4px solid #666;padding:.75rem 1rem;background:#f5f5f5}}
</style>
</head>
<body>
<header><h1>Babel / Global (K)Creole</h1>
<p>{html.escape(description)}</p></header>
<section class="notice"><strong>Current status: bootstrap draft.</strong>
This is a metadata and interoperability framework, not a complete language corpus, not a universal Creole language, and not a claim of community endorsement. Draft records are not evidence.</section>
<h2>Current repository counts</h2><ul>{count_html}</ul>
<p>Counts describe records in this repository snapshot, not the global number of languages, varieties, or resources. Rights and AI-use permissions are assessed per source and operation; a link is not permission to copy or train.</p>
<h2>Start here</h2><ul>{link_html}</ul>
<footer><p>Generated from the versioned repository catalog. Verify claims against cited sources and the exact commit or release used.</p></footer>
</body></html>
"""
    (output / "index.html").write_text(page, encoding="utf-8")
    (output / "llms.txt").write_text((ROOT / "llms.txt").read_text(encoding="utf-8"), encoding="utf-8")
    (output / "catalog.json").write_text((ROOT / "catalog.json").read_text(encoding="utf-8"), encoding="utf-8")
    (output / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: " + base_url + "/sitemap.xml\n",
        encoding="utf-8",
    )
    sitemap_urls = [base_url + "/", base_url + "/llms.txt", base_url + "/catalog.json"]
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"  <url><loc>{xml_escape(url)}</loc></url>" for url in sitemap_urls)
        + "\n</urlset>\n"
    )
    (output / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"SITE BUILT: {output.resolve()} (3 sitemap URLs; Dataset JSON-LD included; no source corpus copied).")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="Exact deployed Pages base URL, including repository path if any")
    parser.add_argument("--output-dir", default="site", help="Output directory")
    args = parser.parse_args()
    if not args.base_url.startswith("https://"):
        parser.error("--base-url must be an HTTPS URL")
    build(args.base_url, args.output_dir)


if __name__ == "__main__":
    main()
