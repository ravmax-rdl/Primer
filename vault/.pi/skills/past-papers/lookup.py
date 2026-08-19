#!/usr/bin/env python3
"""Resolve a paper code or course name through crosswalk.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib.vault import find_vault  # noqa: E402

VAULT = find_vault()
DOC = VAULT / "Papers & Reviews" / "BSc" / "crosswalk.json"
CODE_RE = re.compile(r"(SCS|ENH?|EN|IS)[ _-]?(\d{4})", re.I)


def norm(code: str) -> str:
    m = CODE_RE.search(code)
    if not m:
        return code.strip()
    prefix = m.group(1).upper()
    if prefix == "ENH":
        prefix = "ENH"
    elif prefix == "EN":
        prefix = "EN"
    return "%s %s" % (prefix, m.group(2))


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: lookup.py <code-or-course-name>")
        sys.exit(2)
    q = " ".join(sys.argv[1:]).strip()
    data = json.loads(DOC.read_text(encoding="utf-8"))
    code = norm(q)
    rec = data["map"].get(code)
    if rec:
        print("code\t%s" % code)
        print("title\t%s" % rec.get("title"))
        print("current\t%s" % ",".join(rec.get("current") or []))
        print("confidence\t%s" % rec.get("confidence"))
        if rec.get("notes"):
            print("notes\t%s" % rec["notes"])
        if not rec.get("current"):
            print("BLOCK\tno current Y1 S1 equivalent — exclude from /mock")
        elif rec.get("confidence") == "low":
            print("BLOCK\tlow confidence — confirm before /mock")
        return
    qlow = q.lower()
    for cur in data["current"]:
        if qlow in cur["course"].lower() or qlow == cur["code"].lower():
            print("code\t%s" % cur["code"])
            print("title\t%s" % cur["course"])
            print("current\t%s" % cur["code"])
            print("confidence\thigh")
            return
    print("unknown\t%s" % q)
    sys.exit(1)


if __name__ == "__main__":
    main()
