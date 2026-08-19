---
name: past-papers
description: >
  Past-paper workflow for the UCSC BSc learning vault. Owns the course-code
  crosswalk, grading-confidence gates, classified question bank layout, and
  the review-canvas workflow.
---

# Past papers

## What it owns

- Course-code crosswalk (`Papers & Reviews/BSc/crosswalk.json`)
- `/lookup` through codes or course names
- `/classify`, `/mock`, and exam-related workflows

## Crosswalk first (hard gate)

Always resolve a legacy code (e.g. `SCS 11xx`/`12xx`) into the current semester codes
using:

- `Papers & Reviews/BSc/Crosswalk.md`
- `Papers & Reviews/BSc/crosswalk.json`

If the resolved row has `confidence: low` or an empty `current`, treat the paper
as excluded for current-semester workflows.

## Classified question bank layout

Write one note per topic at:

`Papers & Reviews/BSc/Classified/<Course>/<Topic>.md`

Where:
- `<Course>` is the current filename/join key (e.g. `Discrete Mathematics`)
- `<Topic>` is the topic label chosen by the workflow

Notes should use pdf++ links for page evidence and link back to the lecture notes
that cover the topic.

## Review canvas

The review-canvas workflow embeds question crops with pdf++ page links and places
worked solutions in adjacent nodes. Geometry comes from `canvas-gen` (never
hand-placed coordinates).

