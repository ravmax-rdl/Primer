---
description: Run a timed mock from verified questions and grade with stated confidence
argument-hint: "<course> [minutes]"
---
Load `past-papers`, `pdf-search`, and `vault-syntax`. Run a mock for **$1** with a ${2:-180}-minute limit.

1. Resolve the course crosswalk. Use only high-confidence or user-confirmed mappings.
2. Prefer classified-bank questions, weighted by frequency and lapses under `Study Notes/Review/$1/`. If no bank exists, use verified mapped papers. Never generate a question and present it as a real paper.
3. Serve one question at a time. Do not hint before the learner commits.
4. Use an official scheme when one exists. Otherwise grade from a cited lecture note, state confidence, and never call the result an official mark.
5. Offer `postmortem.md` after the final question.
