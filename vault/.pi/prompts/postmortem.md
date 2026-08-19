---
description: Classify mock errors and encode gap or misconception cards
argument-hint: "<mock-or-note>"
---
Load `past-papers` and `spaced-repetition`. Run a postmortem on **$1**.

For each missed question, add one label and a one-line reason tied to a lecture note:

- `- [?]` gap: never taught or written up
- `- [/]` misconception: taught but still wrong
- `- [-]` careless: known but executed poorly

For a gap or misconception, use `sm2.py new` and propose an atomic card under `Study Notes/Review/<Course>/`. Show cards for approval before writing. A careless error does not become a card.

Do not reteach the whole topic. Offer a targeted `/teach` on the worst strand.
