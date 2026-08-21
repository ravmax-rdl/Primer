---
description: Classify assessment errors and choose an evidence-backed card action
argument-hint: <attempt-or-target-note>
---

Use the `past-papers`, `spaced-repetition`, and `academic-workflow` skills.
Postmortem the supplied attempt against its cited grading source.

For every lost mark, select one or more exact labels and give a one-line reason
tied to the observed answer or faulty step:

- `recall`
- `concept`
- `translation`
- `procedure`
- `calculation`
- `misread`
- `incomplete-justification`
- `time-management`

Check prior evidence and related card state. Run `learning_state.py decide-card`;
do not choose `create`, `revise`, `suspend`, or `none` by intuition. A
non-recall/non-concept error receives a targeted practice intervention instead
of a card. Show proposed card content before any card note is written.

Return the structured attempt evidence and one next action to the calling
`exam.md` or `study.md` workflow. Do not write another note directly.
