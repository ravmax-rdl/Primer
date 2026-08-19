---
description: Reverse lookup — which PDF/note a claim came from
argument-hint: "<claim>"
---
Load `pdf-search`. Given this claim: $@

Search notes and the PDF index for the closest quote. Return the `[[note]]` and a pdf++ page link if a PDF backs it. If nothing matches, say so — do not fabricate a source.
