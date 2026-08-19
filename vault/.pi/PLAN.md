# Primer Pi runtime guide

The runtime is already packaged in this vault. Keep this file as a short inventory and rebuild reference. Daily use starts at `START HERE.md`.

## What loads in a session

- `CLAUDE.md`: vault structure and safety rules
- `.pi/APPEND_SYSTEM.md`: teaching protocol and hard rules
- `.pi/LEARNER.md`: editable learner preferences
- `.pi/settings.json`: project settings
- `.pi/prompts/*.md`: slash commands
- `.pi/skills/*/SKILL.md`: vault syntax and deterministic tools
- `.pi/agents/academic.md`: the `@academic` tutor agent
- `.pi/extensions/guard/`: generic credential and recovery path blocking

Vault-visible runtime files include `Study Notes/Review/Due.base`, `Papers & Reviews/BSc/Crosswalk.md`, and `Papers & Reviews/BSc/crosswalk.json`.

## Rebuild outline

1. Install Pi and the required packages listed in the repository's `docs/setup.md`.
2. Run Pi from the `vault/` directory and review the project trust prompt.
3. Confirm Pi discovers this project's prompts, skills, agent, extension, and settings once each.
4. Run `python .pi/skills/spaced-repetition/sm2.py new`.
5. Follow the fictional demo in `START HERE.md` before adding personal notes.

Provider connectors, PDF tools, Zotero, Canvas helpers, and visual Obsidian plugins are optional. Add them only for the workflows that use them.
