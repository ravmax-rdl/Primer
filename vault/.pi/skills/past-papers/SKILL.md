---
name: past-papers
description: >
  Map source course codes, classify real questions, grade with explicit evidence,
  and support exam postmortems. Used internally by /exam.
---

# Past papers

1. Read `Papers & Reviews/Programme/Crosswalk.md` and `crosswalk.json` before
   using a source-paper code. Low confidence or no current mapping blocks it.
2. Require an `indexed` PDF state before quoting a question. Report other states
   accurately and never reconstruct an unreadable stem.
3. Cite official marking schemes when available. Otherwise grade from a named
   source, state confidence, and do not call the result official.
4. Write at most one approved classified topic note per turn.

Internal references `crosswalk.md`, `classify.md`, `paper.md`, `mock.md`,
`predict.md`, `paper-review.md`, and `postmortem.md` run through `/exam`; they are
not slash commands.

```bash
python .pi/skills/past-papers/lookup.py "LEGACY102"
python .pi/skills/past-papers/lookup.py "Foundations of Logic"
```
