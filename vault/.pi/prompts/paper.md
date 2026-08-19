---
description: Fetch a paper and file a structured literature note with vault links
argument-hint: "<url|doi|pdf>"
---
Load `vault-syntax` and `zotero`. Literature note for **$1**.

Fetch via `pi-web-access` (URL / DOI / PDF). Write **one** note under `Papers & Reviews/` with callouts: `> [!abstract]` claim, `> [!info]` method, `> [!example]` evidence, `> [!warning]` limitations, plus `[[wikilinks]]` to existing AL/BSc notes. If the source is a URL, include a ` ```cardlink ` fence. `/preview` if it has math.

Do not dump the full PDF into the vault. Cite pages with pdf++ if a local PDF exists. If Zotero has a record, mention the citekey; if not, skip inventing one.
