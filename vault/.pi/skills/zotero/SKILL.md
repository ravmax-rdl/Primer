---
name: zotero
description: >
  Read-only Zotero lookup for cite, find, and source workflows. The helper copies
  zotero.sqlite to a temporary file before querying it.
---

# Zotero

The helper returns bibliographic metadata without querying Zotero's live database in place.

Run from the vault root:

```bash
python .pi/skills/zotero/query.py search "discrete mathematics"
python .pi/skills/zotero/query.py collections
python .pi/skills/zotero/query.py get "citekey-or-item-id"
```

Set `ZOTERO_DB` when the database is outside the default Zotero directory. If Zotero has no result, use `pdf-search` over user-supplied vault PDFs. Never invent a citation key or bibliographic record.
