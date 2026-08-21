---
description: Review canvas for a past-paper PDF (page crops + worked solutions)
argument-hint: "<pdf>"
---
Load `past-papers`, `canvas-gen`, `pdf-search`, and `vault-syntax`. Build a review canvas for **$1**.

- Embed questions with pdf++ links. Use `rect=` only if copied from pdf++; otherwise `#page=N`.
- Worked solutions in adjacent text nodes, graded from lecture notes, labelled unofficial for Programme
- Model writes a `graph.json`; `layout.py` assigns coordinates. Merge if a canvas already exists. Write a `.canvas` next to the paper or under `Papers & Reviews/Programme/`.
- Do not use `obsidian_create_canvas` (it dumps on the vault root and strips hex colours).
