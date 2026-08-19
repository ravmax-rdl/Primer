---
description: Unified search across notes, PDF text, and Zotero
argument-hint: "<query>"
---
Load `pdf-search`, `zotero`, and `vault-syntax`. Find **$1**.

1. `rg` vault notes (exclude Bin/, .obsidian/, .pi/cache/).
2. `python3 .pi/skills/pdf-search/index.py search "$1"`.
3. `python3 .pi/skills/zotero/query.py search "$1"`.

Rank: exact note title, then PDF page hits (pdf++ links), then Zotero. Quote short snippets. Do not write a new note unless I ask.
