---
description: Run the Alvar teach protocol on a subject, writing into the day's note
argument-hint: "<course> [target-note]"
---
Load the `vault-syntax` skill and the `teach` skill, then tutor me on **$1** using the probe → plan → teach → lock-in-quiz protocol.

Target note: ${2:-today's `Study Notes/Programme/Y01_S01/W##/D##/$1.md`}. If the week/day is ambiguous, ask me which before writing.

Rules:
- Read `.pi/LEARNER.md` first.
- Probe with 1–3 MCQs via the `ask_user` tool (never paste A/B/C/D in chat; always include "I don't know"). Write an `## Understanding map` using the checkbox markers in `vault-syntax`: `- [x]` known, `- [/]` edge, `- [?]` unknown, `- [!]` blocked — each with a one-line evidence clause.
- Show a fenced ` ```mermaid ` flowchart **before** teaching. One reasoning step per turn, then quiz that step via `ask_user`. Advance only on lock-in; on failure, stay or insert a prerequisite.
- Write taught content with live syntax from `Markdown Snippets.md` as filtered by `vault-syntax`: `> [!note]` for definitions, `> [!question]` for exam traps, `> [!Equation]` + `align*` for derivations, pdf++ page links (not bare `[[file.pdf]]`). `/preview` before math-heavy writes. TikZ only when the picture *is* the claim.
- The filename must equal the exact course name "$1" (Bases join key). Edit in place; never duplicate.
- When we stop, record what locked, what's still `edge`, and the next node.
