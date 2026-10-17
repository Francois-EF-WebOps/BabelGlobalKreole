#!/usr/bin/env python3
"""Check registered resource URLs without changing registry verification claims."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "resources" / "resources.jsonl"


def strip_tracking(url):
    parts = urlsplit(url)
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
             if not key.lower().startswith("utm_")]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def request_status(url, method):
    request = Request(url, method=method, headers={"User-Agent": "BabelGlobalKreole-link-check/1.0", **({"Range": "bytes=0-0"} if method == "GET" else {})})
    try:
        with urlopen(request, timeout=15) as response:
            return response.status, response.geturl()
    except HTTPError as exc:
        return exc.code, exc.geturl()
    except (URLError, TimeoutError, OSError):
        return None, url


def check(url):
    status, final_url = request_status(url, "HEAD")
    if status in (403, 405, 501):
        status, final_url = request_status(url, "GET")
    if status is None:
        label = "unreachable"
    elif status in (401, 403, 429):
        label = "blocked_or_rate_limited"
    elif 200 <= status < 400:
        label = "reachable"
    else:
        label = "http_error"
    return label, status, strip_tracking(final_url)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="resource-link-check-report.json")
    args = parser.parse_args()
    rows = []
    for line_no, line in enumerate(REGISTRY.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        card = json.loads(line)
        label, status, final_url = check(card["url"])
        rows.append({
            "id": card["id"],
            "name": card["name"],
            "url": strip_tracking(card["url"]),
            "final_url": final_url,
            "http_status": status,
            "result": label,
            "registry_verification_unchanged": card["verification"],
        })
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "source": "data/resources/resources.jsonl",
        "note": "Reachability checks do not establish license, AI-use permission, linguistic validity, or community consent. This report does not modify registry cards.",
        "results": rows,
    }
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {}
    for row in rows:
        counts[row["result"]] = counts.get(row["result"], 0) + 1
    print(f"RESOURCE LINK REPORT: {len(rows)} URLs checked; " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    for row in rows:
        print(f"{row['id']}: {row['result']} (HTTP {row['http_status']}) {row['url']}")
    print(f"Report written to {args.output}; registry statuses unchanged.")


if __name__ == "__main__":
    main()
