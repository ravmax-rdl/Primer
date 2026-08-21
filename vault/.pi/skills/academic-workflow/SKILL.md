---
name: academic-workflow
description: >
  Run evidence-backed study, capture, research, exam, and PDF-health workflows.
  Use internal specialist references without exposing each operation as a slash
  command.
---

# Academic workflow

Public commands are `/study`, `/capture`, `/research`, `/exam`, and `/doctor`.
Files under `references/` are internal instructions, not callable commands.

## Routing

- `/study`: `probe.md`, `teach.md`, `exercises.md`, `worked.md`, `feynman.md`,
  `review.md`, `postmortem.md`, `cards.md`, `weakspots.md`, `cram.md`.
- `/capture`: `lecture.md`, `lecture-video.md`, `source.md`, `summary.md`,
  `find.md`.
- `/research`: `find.md`, `source.md`, `cite.md`, `synth.md`, `summary.md`,
  `gap.md`, `paper-review.md`, `overview.md`.
- `/exam`: `paper.md`, `mock.md`, `classify.md`, `crosswalk.md`, `predict.md`,
  `postmortem.md`, `cards.md`.
- `/doctor`: deterministic PDF manifest diagnosis only.

## Evidence contract

Keep stable preferences and constraints in `.pi/LEARNER.md`. Put dynamic study
and assessment evidence in the one note being studied:

````text
```academic-evidence
{"record_type":"study_session",...}
```
````

Use the deterministic utility:

```bash
python .pi/skills/academic-workflow/learning_state.py validate "path/to/note.md"
python .pi/skills/academic-workflow/learning_state.py latest "path/to/note.md" concept-id
python .pi/skills/academic-workflow/learning_state.py decide-card --errors recall
python .pi/skills/academic-workflow/learning_state.py append "path/to/note.md" -
```

Pass one JSON object on stdin for `append`. A turn may append only to its selected
target note. Validation failure leaves the note unchanged.

## Error taxonomy

Use only `recall`, `concept`, `translation`, `procedure`, `calculation`,
`misread`, `incomplete-justification`, and `time-management`. Feedback names the
observed answer or faulty step. Never convert one attempt into a learner trait.

## Card decisions

- First supported recall or concept failure without a card: `create`.
- Repeated supported failure or existing related card: `revise`.
- Misleading card: `suspend`.
- Passing attempt or another error type alone: `none` and targeted practice.

Run the utility instead of choosing manually. Never bulk-create cards from source
text or an inferred Understanding map.
