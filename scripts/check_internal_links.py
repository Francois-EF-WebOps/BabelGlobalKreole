#!/usr/bin/env python3
"""Check that local Markdown links point to tracked repository paths."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\\[[^\\]]*\\]\\(([^)]+)\\)")
errors = []
checked = 0

for document in sorted(ROOT.rglob("*.md")):
    if ".git" in document.parts:
        continue
    content = document.read_text(encoding="utf-8")
    for match in LINK.finditer(content):
        target = match.group(1).strip()
        if target.startswith("<") and ">" in target:
            target = target[1:target.index(">")]
        else:
            target = target.split()[0] if target else ""
        if not target or target.startswith("#"):
            continue
        parts = urlsplit(target)
        if parts.scheme or parts.netloc:
            continue
        path = unquote(parts.path)
        if not path:
            continue
        resolved = (document.parent / path).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{document.relative_to(ROOT)}: link escapes repository: {target}")
            continue
        checked += 1
        if not resolved.exists():
            line = content.count("\n", 0, match.start()) + 1
            errors.append(f"{document.relative_to(ROOT)}:{line}: missing local target {target}")

if errors:
    print("INTERNAL LINK CHECK FAILED")
    print("\n".join(errors))
    sys.exit(1)
print(f"INTERNAL LINK CHECK PASSED: {checked} local Markdown links resolve to repository paths.")
