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
python .pi/skills/pdf-search/index.py ocr-pages "Papers & Reviews/Programme/Y01_S01/2025/COURSE101.pdf" --dpi 180
python .pi/skills/pdf-search/index.py doctor
```

Generated manifests, extracted text, and rendered OCR pages stay under
`.pi/cache/pdf-index/` rather than synced notes. Incremental stamps include the
shortcut and resolved target.

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

When `pages` reports `no_text_layer`, run `ocr-pages` on the vault PDF path.
The command resolves a PDF++ or Obsidian URI-shortcut, verifies the resolved
target is a readable PDF, and passes that real file to `pdftoppm`. It returns
JSON containing ordered page-image paths for the vision/OCR pass.

Read every returned image in order. Never pass the small shortcut file to an
OCR backend, never skip unreadable pages silently, and never route any state
other than `no_text_layer` into OCR. Pages are cached by source stamp; `--dpi`
defaults to 200. Rendering does not rewrite the PDF or manifest.

`pdftoppm executable not found` means Poppler is unavailable. Install Poppler
or repair `PATH`; do not relabel the source to hide the failure.

Cite page-level hits using the vault's established PDF-link syntax. Never invent
questions, quotations, page numbers, or regions when a source is unavailable.
