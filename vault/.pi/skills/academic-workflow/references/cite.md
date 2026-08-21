---
description: Zotero search → literature note + pasteable wikilink
argument-hint: "<query>"
---
Load `zotero` and `vault-syntax`. Cite **$1**.

`python3 .pi/skills/zotero/query.py search "$1"`. On a hit, write `Papers & Reviews/@<citekey>.md` (one note) with title, creators, year, DOI, related course wikilinks, and a ` ```cardlink ` fence if there is a URL. If the library misses it, say so and search vault PDFs with `pdf-search` — do not invent a citekey.
