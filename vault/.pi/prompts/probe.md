---
description: Diagnostic-only map of what I know on a topic (no teaching)
argument-hint: "<course> [target-note]"
---
Load the `probe` skill. Map the edge of my understanding of **$1** with graded MCQs via the `ask_user` tool (always include "I don't know"). Measure first — do not teach beyond a one-line correction after I answer.

Write the result as an `## Understanding map` in ${2:-today's subject note for $1} using the checkbox markers from `vault-syntax` / `Markdown Snippets.md`:

```
- [x] <strand> — known: <one-line evidence>
- [/] <strand> — edge: <what works / what fails>
- [?] <strand> — unknown
- [!] <strand> — blocked on <prerequisite>
```

End by saying which strands a lesson should start from. Read `.pi/LEARNER.md` first.
