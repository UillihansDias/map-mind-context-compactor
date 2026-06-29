#!/usr/bin/env python3
"""Extract likely local file references from a context packet."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


ABS_PATH = r"/(?:[\w.@+~-][\w .@+~-]*/)+[\w.@+~-][\w .@+~-]*"
REL_FILE = r"(?:\.{1,2}/)?[\w@+\-][\w@+\-./ ]+\.(?:py|js|ts|tsx|jsx|md|json|yaml|yml|toml|txt|sh|css|html|go|rs|java|rb|php|swift|kt|sql)"
PATH_RE = re.compile(rf"(?P<path>{ABS_PATH}|{REL_FILE})(?::(?P<line>\d+))?")


def extract(text: str) -> list[tuple[str, str, bool]]:
    refs: dict[str, tuple[str, bool]] = {}
    for match in PATH_RE.finditer(text):
        raw = match.group("path").strip("`'\"),.;")
        if len(raw) < 3 or "://" in raw:
            continue
        expanded = os.path.expanduser(raw)
        exists = Path(expanded).exists()
        refs[raw] = (match.group("line") or "", exists)
    return [(path, line, exists) for path, (line, exists) in sorted(refs.items())]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", help="Markdown context packet to inspect")
    args = parser.parse_args()

    text = Path(args.packet).read_text(encoding="utf-8")
    refs = extract(text)
    if not refs:
        print("No local file references found.")
        return 0

    for path, line, exists in refs:
        status = "exists" if exists else "missing"
        suffix = f":{line}" if line else ""
        print(f"{status}\t{path}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
