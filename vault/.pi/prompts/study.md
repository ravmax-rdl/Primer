---
description: Run one evidence-backed study session from probe through next action
argument-hint: <course> <minutes> [target-note]
---

Run a closed-loop study session for `$ARGUMENTS`.

Use `probe.md`, `teach.md`, `exercises.md` or `worked.md`, `postmortem.md`, and
`cards.md` from the academic-workflow internal references. They are references,
not commands.

1. Parse course, positive integer minutes, and optional target note. Resolve one
   target note from the active note and vault context. Ask one focused question
   only if course or target remains ambiguous.
2. Read `.pi/LEARNER.md` for stable preferences and constraints. Never write
   dynamic mastery there.
3. Run `python .pi/skills/pdf-search/index.py doctor` when the session cites PDF
   sources. Stop source-dependent work if its record is blocked.
4. Run `python .pi/skills/academic-workflow/learning_state.py latest
   "$TARGET_NOTE" "$CONCEPT_ID"` for relevant concepts.
5. Probe before teaching. Record the observed answer. Teach only the
   demonstrated gap, then require retrieval or application within the remaining
   time.
6. Grade against an explicit source or rubric. If an assessment attempt occurs,
   use only the error labels defined by the academic-workflow skill and obtain
   the card action through `learning_state.py decide-card`.
7. Prepare one `study_session` record and, when applicable, one
   `assessment_attempt` record. Include stable IDs, source references, observed
   feedback, and one concrete `next_action`.
8. Run `python .pi/skills/academic-workflow/learning_state.py validate
   "$TARGET_NOTE"` before the write. Append each prepared record with
   `python .pi/skills/academic-workflow/learning_state.py append
   "$TARGET_NOTE" -`, passing the JSON object on stdin. Validate again after
   append.

Write only one target note during this turn. Propose the deterministic card
change in that note; do not bulk-create cards or edit unrelated notes. End with
results, evidence recorded, and the single next action.
