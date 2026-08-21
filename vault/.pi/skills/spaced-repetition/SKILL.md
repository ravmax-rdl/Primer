---
name: spaced-repetition
description: >
  Vault-native SM-2 review cards under Study Notes/Review. The model grades
  recall; sm2.py computes dates and intervals; Due.base displays the queue.
---

# Spaced repetition

One card tests one fact or operation. Every card has a source link.

```yaml
due: 2026-08-24
interval: 6
ease: 2.5
reps: 3
lapses: 1
source: "[[Study Notes/Programme/TERM_01/W01/D01/Foundations of Logic]]"
```

Run from the vault root:

```bash
python .pi/skills/spaced-repetition/sm2.py new
python .pi/skills/spaced-repetition/sm2.py grade "Study Notes/Review/Foundations of Logic/Implication.md" 4
python .pi/skills/spaced-repetition/sm2.py due "Study Notes/Review" --subject "Foundations of Logic"
python .pi/skills/spaced-repetition/sm2.py peek "Study Notes/Review/Foundations of Logic/Implication.md"
```

Grades 0–2 are lapses. Grades 3–5 are successful recall. Do not edit schedule fields by hand. `Study Notes/Review/Due.base` lists cards whose `due` date is today or earlier.
