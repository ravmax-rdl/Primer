#!/usr/bin/env python3
"""Resolve a paper code or course name through the distribution crosswalk."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib.vault import find_vault  # noqa: E402

VAULT = find_vault()
DOC = VAULT / "Papers & Reviews" / "Programme" / "crosswalk.json"
CODE_RE = re.compile(r"([A-Za-z]+)[ _-]?(\d+)", re.I)


def norm(code: str) -> str:
    match = CODE_RE.search(code)
    if not match:
        return code.strip()
    return "%s%s" % (match.group(1).upper(), match.group(2))


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: lookup.py <code-or-course-name>")
        raise SystemExit(2)
    query = " ".join(sys.argv[1:]).strip()
    data = json.loads(DOC.read_text(encoding="utf-8"))
    code = norm(query)
    record = data["map"].get(code)
    if record:
        print("code\t%s" % code)
        print("title\t%s" % record.get("title"))
        print("current\t%s" % ",".join(record.get("current") or []))
        print("confidence\t%s" % record.get("confidence"))
        if record.get("notes"):
            print("notes\t%s" % record["notes"])
        if not record.get("current"):
            print("BLOCK\tno current equivalent — exclude from exam selection")
        elif record.get("confidence") == "low":
            print("BLOCK\tlow confidence — confirm before exam selection")
        return
    query_lower = query.lower()
    for current in data["current"]:
        if query_lower in current["course"].lower() or query_lower == current["code"].lower():
            print("code\t%s" % current["code"])
            print("title\t%s" % current["course"])
            print("current\t%s" % current["code"])
            print("confidence\thigh")
            return
    print("unknown\t%s" % query)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
