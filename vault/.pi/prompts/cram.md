---
description: Backward-plan from an exam date across the SM-2 queue
argument-hint: "<exam-date> [course]"
---
Load `spaced-repetition`, `past-papers`, and `canvas-gen`. Cram plan for ${2:-the current semester}, exam **$1**.

1. Cards due between today and $1 (`sm2.py due Review`).
2. Classified-bank high-frequency topics (if present).
3. `/gap` topics still unwritten.

Write **one** plan note under `Time Tables/` (not a bulk of new cards). Structure it with `> [!todo]` for must-do strands and optional `<progress>` bars for coverage — those are not the SM-2 queue (`Due.base` is). A canvas is optional and must go through `layout.py`. Do not invent due dates — the SM-2 script owns those.
