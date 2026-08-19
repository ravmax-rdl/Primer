#!/usr/bin/env python3
"""Deterministic SM-2 scheduler for vault review cards.

The LLM grades recall; THIS script computes every date and interval.
Dependency-free (minimal frontmatter parser) so it runs on any python3.

Usage:
  sm2.py new
      Print initial schedule frontmatter values for a fresh card.

  sm2.py grade <cardfile.md> <grade 0-5>
      Read the card's frontmatter, apply SM-2, write it back, print a summary.

  sm2.py due <root_dir> [--subject NAME]
      List card files whose `due` is today or earlier (the review queue).

  sm2.py peek <cardfile.md>
      Print a card's current schedule fields.

Card frontmatter fields owned by this script:
  due (YYYY-MM-DD), interval (int days), ease (float), reps (int), lapses (int)
"""

import sys
import os
import re
import datetime

TODAY = datetime.date.today()
DATT = "%Y-%m-%d"

# --- minimal frontmatter parse/serialize (flat scalar fields only) ---

def read_frontmatter(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text, None
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    order = []
    for line in fm_raw.split("\n"):
        mm = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if mm:
            key = mm.group(1)
            val = mm.group(2).strip()
            fm[key] = val
            order.append(key)
    return fm, body, order


def write_frontmatter(path, fm, body, order):
    lines = ["---"]
    seen = set()
    for key in order:
        if key in fm and key not in seen:
            lines.append(f"{key}: {fm[key]}")
            seen.add(key)
    for key, val in fm.items():
        if key not in seen:
            lines.append(f"{key}: {val}")
    lines.append("---")
    out = "\n".join(lines) + "\n" + body
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)


def strip_quotes(v):
    return v.strip().strip('"').strip("'")


# --- SM-2 core ---

def sm2(ease, interval, reps, lapses, grade):
    """Return (ease, interval, reps, lapses) after a review with `grade` 0-5."""
    ease = float(ease)
    interval = int(float(interval))
    reps = int(float(reps))
    lapses = int(float(lapses))
    grade = int(grade)
    if grade < 0 or grade > 5:
        raise ValueError("grade must be 0-5")

    if grade >= 3:  # recalled
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 6
        else:
            interval = round(interval * ease)
        reps += 1
    else:  # lapse
        reps = 0
        interval = 1
        lapses += 1

    ease = ease + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
    if ease < 1.3:
        ease = 1.3
    ease = round(ease, 3)
    return ease, interval, reps, lapses


def cmd_new():
    print("due: %s" % TODAY.strftime(DATT))
    print("interval: 0")
    print("ease: 2.5")
    print("reps: 0")
    print("lapses: 0")


def cmd_grade(path, grade):
    fm, body, order = read_frontmatter(path)
    ease = strip_quotes(fm.get("ease", "2.5"))
    interval = strip_quotes(fm.get("interval", "0"))
    reps = strip_quotes(fm.get("reps", "0"))
    lapses = strip_quotes(fm.get("lapses", "0"))
    ease, interval, reps, lapses = sm2(ease, interval, reps, lapses, grade)
    due = TODAY + datetime.timedelta(days=interval)
    fm["ease"] = str(ease)
    fm["interval"] = str(interval)
    fm["reps"] = str(reps)
    fm["lapses"] = str(lapses)
    fm["due"] = due.strftime(DATT)
    if order is None:
        print("ERROR: %s has no YAML frontmatter" % path, file=sys.stderr)
        sys.exit(1)
    for k in ("due", "interval", "ease", "reps", "lapses"):
        if k not in order:
            order.append(k)
    write_frontmatter(path, fm, body, order)
    print("graded %d -> due %s | interval %dd | ease %s | reps %d | lapses %d"
          % (grade, fm["due"], interval, ease, reps, lapses))


def cmd_due(root, subject=None):
    hits = []
    for dirpath, _, files in os.walk(root):
        for name in files:
            if not name.endswith(".md"):
                continue
            p = os.path.join(dirpath, name)
            fm, _, _ = read_frontmatter(p)
            due = strip_quotes(fm.get("due", ""))
            if not due:
                continue
            try:
                d = datetime.datetime.strptime(due, DATT).date()
            except ValueError:
                continue
            if d <= TODAY:
                if subject and subject.lower() not in p.lower():
                    continue
                hits.append((due, p))
    hits.sort()
    for due, p in hits:
        print("%s\t%s" % (due, p))
    print("# %d card(s) due (<= %s)" % (len(hits), TODAY.strftime(DATT)), file=sys.stderr)


def cmd_peek(path):
    fm, _, _ = read_frontmatter(path)
    for k in ("due", "interval", "ease", "reps", "lapses", "source"):
        if k in fm:
            print("%s: %s" % (k, fm[k]))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "new":
        cmd_new()
    elif cmd == "grade" and len(args) == 3:
        cmd_grade(args[1], int(args[2]))
    elif cmd == "due" and len(args) >= 2:
        subject = None
        if "--subject" in args:
            subject = args[args.index("--subject") + 1]
        cmd_due(args[1], subject)
    elif cmd == "peek" and len(args) == 2:
        cmd_peek(args[1])
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
