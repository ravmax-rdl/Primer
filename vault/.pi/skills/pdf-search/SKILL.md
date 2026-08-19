---
name: pdf-search
description: >
  Search and index vault PDFs by extracted text. Resolves Obsidian URI-shortcut
  PDFs when present, extracts with pdftotext, and can use a text-extractor OCR
  cache for scan-only documents. Emits page evidence in Obsidian link syntax.
---

# PDF search

## What it does

- Indexes page text for PDFs found under the current vault.
- Resolves an Obsidian URI-shortcut PDF to its local target when the user has configured one.
- Tries the optional text-extractor OCR cache when `pdftotext` finds no readable pages.
- Stores generated index data under `.pi/cache/pdf-index/`, never beside source PDFs.

## Script

Run from the vault root:

```bash
python .pi/skills/pdf-search/index.py index
python .pi/skills/pdf-search/index.py search "equivalence relation"
python .pi/skills/pdf-search/index.py pages "Study Notes/BSc/S01_2026/Discrete Mathematics/Lecture.pdf"
```

`index.py` discovers the vault through `.pi/settings.json`. Set `VAULT_ROOT` only when running the script from outside the vault.

## Citations

Cite every page hit with an Obsidian page link:

```text
[[Name.pdf#page=N|Name, p.N]]
```

Add `rect=x,y,w,h` only when a PDF tool supplied exact coordinates. Never invent a region.
