---
description: Run or review an assessment with structured evidence and card decisions
argument-hint: <course> [question-or-paper] [target-note]
---

Run an evidence-backed assessment workflow for `$ARGUMENTS`.

Use `mock.md` or `paper.md`, `classify.md` or `crosswalk.md`, `postmortem.md`,
and `cards.md` from the academic-workflow internal references.

1. Resolve one course, stable question identity, source or rubric, and one target
   note. Ask only when one of these remains ambiguous.
2. Before showing the answer, capture start time and confidence from 0 to 1.
3. Grade marks against an explicit marking source. If no authoritative marking
   source exists, lower `grading_confidence` and label the grading as provisional.
4. Classify observed errors using only: `recall`, `concept`, `translation`,
   `procedure`, `calculation`, `misread`, `incomplete-justification`, and
   `time-management`. The feedback must name the observed answer or faulty step.
5. Determine recurrence from prior evidence in the target note. Run
   `python .pi/skills/academic-workflow/learning_state.py decide-card` with the
   exact errors and real card state. Accept only `create`, `revise`, `suspend`,
   or `none`.
6. Build one `assessment_attempt` record containing question ID, course and
   concept IDs, marks, elapsed seconds, prior confidence, grading source and
   confidence, error labels, feedback, and card action.
7. Run `python .pi/skills/academic-workflow/learning_state.py validate
   "$TARGET_NOTE"` before writing. Append with
   `python .pi/skills/academic-workflow/learning_state.py append
   "$TARGET_NOTE" -`, passing the JSON record on stdin. Validate again.

Write only the target note. A non-card error produces a concrete practice
intervention, not a manufactured recall card. End with score, time, calibration,
error evidence, card action, and next practice action.
