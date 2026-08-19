---
description: Turn a note's edge and locked strands into SM-2 review cards
argument-hint: "<note>"
---
Load the `spaced-repetition` skill. Read **$1**, including its `## Understanding map` when present. Treat `- [/]` as edge, `- [x]` as known, `- [?]` as teach first, and `- [!]` as blocked.

For each edge strand or freshly locked concept, propose one atomic card under `Study Notes/Review/<Course>/`.

Rules:
- One fact or operation per card. Split compound prompts.
- Every card links to `$1` through `source: "[[$1]]"`.
- Use `sm2.py new` for initial schedule values. Never calculate dates by hand.
- Show every proposed card for approval before writing.
