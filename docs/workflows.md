# Workflows

## Study

```text
/study <course> <minutes> [target-note]
```

The workflow resolves one note, checks cited PDF states, reads recent evidence,
probes before teaching, teaches only the demonstrated gap, requires practice,
grades against a named source, applies the fixed error taxonomy, runs the card
decision, and appends validated evidence with one next action.

Stable preferences remain in `.pi/LEARNER.md`. Dynamic state uses
`academic-evidence` fenced JSON records in the target note.

## Exam

```text
/exam <course> [question-or-paper] [target-note]
```

Capture confidence and start time before the answer. Record marks, elapsed
seconds, grading source and confidence, concept IDs, observed feedback, and any
of these errors:

- `recall`
- `concept`
- `translation`
- `procedure`
- `calculation`
- `misread`
- `incomplete-justification`
- `time-management`

Card actions are `create`, `revise`, `suspend`, or `none`. Recall and concept
failures may justify cards; other errors normally justify targeted practice.

### Scanned paper to answer script

When a paper reports `no_text_layer`, run:

```bash
python .pi/skills/pdf-search/index.py ocr-pages \
  "Papers & Reviews/Programme/Y01_S01/2025/COURSE101.pdf" --dpi 180
```

The command resolves a PDF++ shortcut and renders the real target. Read every
returned page image, preserve question order and marks, then write one note to
`Papers & Reviews/Programme/Y01_S01/Answer Scripts/<year>/`. Link the question
paper and checking source, set `ocr-route: resolved-pdf-raster`, separate the
transcription from authored answers, and mark unreadable text rather than
inventing it.

## Capture

```text
/capture [source] [course] [target-note]
```

Resolve one destination, preserve page or timestamp provenance, normalize the
note, and write only after the source state is truthful. Missing targets and
unsupported URIs are source repairs, not OCR candidates.

## Research

```text
/research <question-or-topic> [target-note]
```

Build claim–evidence rows before prose. Separate direct support, derivation,
external corroboration, inference, and unverified claims. Preserve
counterevidence and unresolved gaps.

## Doctor

```text
/doctor
```

Reports `indexed`, `missing_target`, `unsupported_uri`, `unreadable`,
`no_text_layer`, `ocr_pending`, and `failed`. It does not reindex, queue OCR, or
repair files.

## Internal references

Specialist files under `.pi/skills/academic-workflow/references/` implement the
five workflows. They are not callable slash commands. Customize their source
and note conventions through the five front-door prompts rather than exposing
more top-level commands.
