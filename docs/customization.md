# Customization

Change Primer in small, reviewable steps. Keep the fictional demo until your first course works end to end.

## Learner profile

Edit `vault/.pi/LEARNER.md`. Describe durable preferences such as prior knowledge, pacing, notation, accessibility needs, and how quickly Pi should move after a correct answer. Do not put credentials, medical records, student IDs, or private account data in the profile. Hosted models may receive it in session context.

## Semester and course names

The starter paths use `Study Notes/BSc/S01_2026/`. To use another semester:

1. Copy the folder structure to a new semester code.
2. Update template frontmatter and the affected `.base` folder filters.
3. Keep every day-note filename equal to its course name.
4. Update `Papers & Reviews/BSc/crosswalk.json` only from a verified UCSC source.

Do not bulk-rename a live synced vault. Migrate one course, verify its Bases view, then continue.

## Commands and skills

- Slash commands live in `vault/.pi/prompts/`.
- Skill instructions and deterministic helpers live in `vault/.pi/skills/`.
- The academic sub-agent lives at `vault/.pi/agents/academic.md`.
- Tool-call safety lives in `vault/.pi/extensions/guard/`.

Pi discovers these project-local resources automatically when launched from `vault/`. Do not register the same paths again in settings; duplicate resource loading causes ambiguous commands.

## Providers

Primer does not select a model provider. Use Pi's `/login` flow for a supported provider and review that provider's retention, training, and regional processing terms. Keep provider connectors in the user's Pi configuration unless the entire class or team has agreed to a project-level dependency.

## Sensitive path rules

`vault/.pi/extensions/guard/patterns.ts` blocks common credential, recovery, token, environment, and private-key paths. Add a pattern only when it names a real risk without blocking normal course files. Run `node --test tests/guard.test.mjs` after every change.

The guard is a last line of defense. It does not make a vault safe for credentials.

## Obsidian themes and plugins

Primer commits portable core settings only. It does not bundle CSS, themes, plugin binaries, workspace state, or sync settings.

The screenshots use **Minimal**. **Baseline** is a tested visual alternative from the source vault. Install themes through Obsidian's theme browser. Keep `vault/.obsidian/appearance.json` readable without either theme.

Add a community plugin only when a documented workflow requires it. Record the plugin ID, purpose, minimum version, stored data, and network behavior in the setup and privacy docs. Never commit a plugin's `main.js` or local `data.json` to Primer.

## Course colors and Canvas

Course colors belong in course data or generated Canvas nodes, not custom CSS. Use `.pi/skills/canvas-gen/layout.py` for coordinates and `--merge` when updating an existing Canvas. Manual node positions are user data and must survive regeneration.
