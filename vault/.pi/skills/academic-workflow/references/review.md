---
description: Drill due SM-2 cards; self-grade; the script reschedules
argument-hint: "[subject] [n]"
---
Load the `spaced-repetition` skill. Pull cards due today via `sm2.py due Review`${1:+, filtered to subject $1}${2:+, up to $2 cards}.

Quiz me one card at a time via the `ask_user` tool: show the prompt side, I answer, then reveal the back. I self-grade 0–5. Feed each grade to `sm2.py grade <cardfile> <0-5>` to reschedule — never edit `due`/`interval`/`ease` by hand. Judge my recall on concept match, not exact wording.

At the end, summarise what locked and what lapsed, and offer to make fresh cards (`cards.md`) for anything that keeps lapsing.
