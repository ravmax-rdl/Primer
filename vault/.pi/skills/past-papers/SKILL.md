---
name: past-papers
description: >
  Map source course codes, classify real questions, grade with explicit evidence,
  and support exam postmortems. Used internally by /exam.
---

# Past papers

1. Read `Papers & Reviews/Programme/Crosswalk.md` and `crosswalk.json` before
   using a source-paper code. Low confidence or no current mapping blocks it.
2. Require `indexed` text before quoting a question. If the only failure is
   `no_text_layer`, run `pdf-search/index.py ocr-pages` and transcribe every
   rendered page from the resolved target. Other source states block quoting;
   never reconstruct unreadable stems.
3. Cite official marking schemes when available. Otherwise grade from a named
   source, state confidence, and do not call the result official.
4. Write at most one approved classified topic note per turn.

Internal references `crosswalk.md`, `classify.md`, `paper.md`, `mock.md`,
`predict.md`, `paper-review.md`, and `postmortem.md` run through `/exam`; they are
not slash commands.

## Lookup

```bash
python .pi/skills/past-papers/lookup.py "LEGACY102"
python .pi/skills/past-papers/lookup.py "Foundations of Logic"
```

## Answer scripts

For a full scanned paper, write one Markdown note at:

```text
Papers & Reviews/Programme/Y01_S01/Answer Scripts/<year>/<course> Answer Script.md
```

The note must link the full vault-relative `question-paper` and named
`checking-source`, set `ocr-route: resolved-pdf-raster`, preserve question
order, options, and marks, and separate OCR transcription from authored
answers. Use a YAML list for multipart papers. Cite an official marking scheme
when one exists; otherwise name the checking evidence and label the answers
unofficial. Mark genuinely unreadable text `[OCR uncertain: …]` instead of
inventing it.

Write one note per paper. Keep rendered images and extracted text under
`.pi/cache/pdf-index/`, never beside source PDFs.

