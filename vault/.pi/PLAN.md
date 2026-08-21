# Academic-agent runtime map

## Public commands

| Command | Purpose |
|---|---|
| `/study <course> <minutes> [target-note]` | Probe, teach, practice, record evidence, set next action |
| `/capture [source] [course] [target-note]` | Normalize one source into one note |
| `/research <question-or-topic> [target-note]` | Build traceable claims and synthesis |
| `/exam <course> [question-or-paper] [target-note]` | Time, grade, classify errors, choose card action |
| `/doctor` | Report PDF manifest health without repairs |

The 25 specialist workflows are internal references under
`.pi/skills/academic-workflow/references/`.

## Deterministic runtime

- `.pi/lib/vault.py`: portable vault discovery
- `.pi/skills/pdf-search/index.py`: source states, extraction, search, doctor
- `.pi/skills/academic-workflow/learning_state.py`: evidence, IDs, validation,
  latest concept state, card decisions
- `.pi/skills/spaced-repetition/sm2.py`: card scheduling
- `.pi/skills/canvas-gen/layout.py`: canvas placement
- `.pi/skills/past-papers/lookup.py`: course mapping

## Contracts

PDF statuses are `indexed`, `missing_target`, `unsupported_uri`, `unreadable`,
`no_text_layer`, `ocr_pending`, and `failed`. Zero pages do not imply OCR.

Assessment errors are `recall`, `concept`, `translation`, `procedure`,
`calculation`, `misread`, `incomplete-justification`, and `time-management`.
Card actions are `create`, `revise`, `suspend`, and `none`.

Dynamic state stays in the selected note. A turn writes one note. Distribution
runtime contains no personal paths, credentials, source manifests, or learner
evidence.

## Verification

```bash
python -m unittest discover -s tests -v
python scripts/verify.py
```
