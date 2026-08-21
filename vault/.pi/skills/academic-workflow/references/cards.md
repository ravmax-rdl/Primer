---
description: Apply an approved deterministic card action to one atomic concept
argument-hint: <target-note> <concept-id> <card-action>
---

Load `spaced-repetition` and `academic-workflow`. Accept only a `create`,
`revise`, `suspend`, or `none` action returned by `learning_state.py decide-card`.

- `create`: propose one atomic recall or concept card when supported failure has
  no related card.
- `revise`: update the one related card that failed or duplicated the concept.
- `suspend`: mark a misleading card for correction before future review.
- `none`: prescribe the recorded practice intervention and create no card.

Every card links to the target note and evidence source. Use `sm2.py` for initial
or revised scheduling values; never calculate dates by hand. Show the exact card
change for approval before writing. Never create cards from an Understanding map
or source text without assessment evidence.
