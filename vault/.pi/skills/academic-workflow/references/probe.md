---
description: Probe the edge of current understanding without teaching ahead
argument-hint: <course> <target-note>
---

Load the `probe` and `academic-workflow` skills. Read stable preferences from
`.pi/LEARNER.md` and recent concept evidence from the target note.

Use graded MCQs or short retrieval questions through `ask_user`; always include
"I don't know" where appropriate. Anchor questions on the target note and its
available cited sources. Ask 2–4 questions per round until the relevant strands
and prerequisites are distinguished.

Measure first. After each answer, give at most a one-line correction. Return
observed evidence as known, edge, unknown, or prerequisite-blocked strands, with
the exact answer that supports each classification.

Do not write an Understanding map or update learner traits. Return the evidence
to `study.md`, which records the validated session or attempt in the one target
note after practice and grading.
