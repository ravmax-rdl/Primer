---
description: Year-ordered papers → topic-ordered question bank + frequency
argument-hint: "<course>"
---
Load `past-papers`, `pdf-search`, and `vault-syntax`. Classify past papers for **$1**.

1. Resolve $1 through `Papers & Reviews/Programmecrosswalk.md.json`. Refuse if the only matches are `confidence: low` or have no current equivalent (e.g. Database I).
2. Index/search the mapped PDFs. Skip files with 0 extracted pages — list them as "needs OCR" instead of inventing questions.
3. Write **one** topic note at `Papers & Reviews/Programme/Classified/$1/<Topic>.md` this turn (filename = topic). Each question as a `> [!question]` (or a quote callout) with year, q-number, pdf++ page link (`[[Paper.pdf#page=N|Paper, p.N]]`), and `[[lecture note]]`. Unreadable scans: `- [!]` "needs OCR" — do not invent the stem.
4. End with a running frequency table for that topic. Offer the next topic; do not dump the whole course in one write.
