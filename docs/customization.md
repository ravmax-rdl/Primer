# Customization

## Course and term paths

The distribution uses `Study Notes/Programme/Y01_S01/` and fictional course IDs.
Term folders follow `Y##_S##` — academic year, then term within that year, so a
second-year first term is `Y02_S01`. Replace them before live use:

1. Choose one canonical term path. Keep the `Y##_S##` shape if you want later
   terms to sort correctly and stay distinguishable in Base filters.
2. Rename course folders and their course-index notes together.
3. Update each `Lecture Notes.base` filename filter.
4. Replace `Papers & Reviews/Programme/crosswalk.json` from official programme
   evidence.
5. Run the release verifier and open every Base after each course migration.

Do not bulk-rename a synced live vault. Migrate one course, verify links and
views, then continue.

## Learning evidence

Keep the record schemas and eight error labels stable. Add domain-specific
concept IDs and source conventions, not new free-form mastery fields. If you add
a record field, update `learning_state.py`, tests, prompts, and docs together.

## Interactive prompts

Keep the terminal-rendering and answer-leak rules in `.pi/APPEND_SYSTEM.md` if
you rewrite that file. They describe the `ask_user` surface itself, not this
distribution's course conventions, so removing them reintroduces mangled math
and questions that print their own answers.

## Workflow prompts

Keep five visible prompts. Customize internal references under
`.pi/skills/academic-workflow/references/` or adjust routing in the skill. Do not
restore specialist aliases under `.pi/prompts/`.

## PDF sources

Use `VAULT_ROOT` for portable script execution. Keep generated manifests, page
text, and OCR renderings under `.pi/cache/`. Preserve
`Papers & Reviews/Programme/Y01_S01/Answer Scripts/<year>/` or replace it with
one documented year-scoped equivalent. An answer-script note links its
question paper and checking source and sets `ocr-route: resolved-pdf-raster`.
Add extraction backends only when they return an explicit failure reason and
map cleanly to the seven-state model.
