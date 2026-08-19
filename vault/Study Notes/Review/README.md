---
type: reference
tags:
  - meta/vault
  - review/spaced-repetition
---
# Review

Vault-native SM-2 cards live under `Study Notes/Review/<Course>/`. Each note has `due`, `interval`, `ease`, `reps`, `lapses`, and a `source` link.

> [!todo] Daily review
> Open [[Due.base]] and drill the *Due today* view with `/review`. Grade recall from 0 to 5. `sm2.py` writes the new schedule; do not edit `due` by hand.

After `/teach`, `/cards <note>` reads the target note's understanding map. Edge and freshly locked ideas may become cards after approval. Unknown ideas wait until they are taught.

Scheduling code: `.pi/skills/spaced-repetition/sm2.py`.
