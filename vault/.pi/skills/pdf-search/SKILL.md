---
name: pdf-search
description: >
  Resolve and search vault PDFs with explicit source states and page-level
  provenance. Never treat a missing target as an OCR candidate.
---

# PDF search

Run from the vault root:

```bash
python .pi/skills/pdf-search/index.py index --root "Courses"
python .pi/skills/pdf-search/index.py search "query" --path "Course"
python .pi/skills/pdf-search/index.py resolve "path/to/source.pdf"
python .pi/skills/pdf-search/index.py pages "path/to/source.pdf"
python .pi/skills/pdf-search/index.py doctor
```

Generated manifests and text stay under `.pi/cache/pdf-index/` rather than
synced notes. Incremental stamps include the shortcut and resolved target.

Each record is exactly one of:

- `indexed`
- `missing_target`
- `unsupported_uri`
- `unreadable`
- `no_text_layer`
- `ocr_pending`
- `failed`

Only `no_text_layer` may lead to OCR. Run `doctor` before source-dependent work.
It reports but never repairs or rewrites the manifest.

Cite page-level hits using the vault's established PDF-link syntax. Never invent
questions, quotations, page numbers, or regions when a source is unavailable.
