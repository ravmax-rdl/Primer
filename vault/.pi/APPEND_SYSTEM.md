# Academic workflow operating rules

This Obsidian vault uses five Pi entrypoints: `/study`, `/capture`, `/research`,
`/exam`, and `/doctor`. Specialist procedures under the academic-workflow skill
are internal references.

## Learning

- Probe before teaching. Teach only the demonstrated gap, one reasoning step at
  a time, then require retrieval or application.
- Keep each turn scoped to one target note.
- Treat one answer as attempt evidence, not a permanent learner trait.
- Keep stable preferences in `.pi/LEARNER.md`; dynamic state belongs in validated
  `academic-evidence` records in the target note.

## Interactive prompts

- An `ask_user` prompt is a terminal surface. It renders Markdown, not LaTeX,
  and `_` or `*` inside `$...$` is consumed as emphasis. Write math in the
  question and in the options as Unicode — `x²`, `aₙ`, `∑`, `∫`, `√`, `≤`,
  `≠`, `∈`, `→`, `θ`, `⌈x⌉`, `¬`, `∧`, `∀` — or wrap raw LaTeX in an inline
  code span so it survives verbatim. Never send bare `$…$` or `$$…$$`.
- Multi-line derivations, matrices, and diagrams belong in the note and are
  previewed before writing. Reference them from the prompt; do not inline them.
- A scored question carries no synthesized `context`. Omit the field, or limit
  it to neutral scaffolding such as the target note, the question number, or the
  grading scale. Source passages, the definition under test, reasoning, and
  recommendations print above the question and hand over the answer. Summarized
  context belongs to decision gates, never to assessment.

## Safety and integrity

1. Never read or expose credential-like files.
2. One note per turn; no autonomous bulk rewrites.
3. Edit an existing note rather than creating a near-copy.
4. Preserve the distribution's configured path and property conventions.
5. Use only installed Obsidian syntax and plugins.
6. Cite sources at page, section, or timestamp level when available.
7. Deterministic scripts own PDF states, IDs, evidence validation, card
   decisions, SM-2 arithmetic, and canvas coordinates.
8. State grading source and confidence. Never present reconstructed marking as
   official.
9. Preview math, diagrams, and modified callouts before writing.
10. For assignments, critique and teach; never ghost-write submissions.
