# Changelog

Primer follows semantic versioning for published releases.

## Unreleased

- Replaced specialist slash-command clutter with `/study`, `/capture`,
  `/research`, `/exam`, and `/doctor`.
- Added explicit PDF source states, provenance fields, canonical manifest paths,
  and a read-only doctor.
- Added resolved-target scan rendering and year-scoped answer-script guidance
  for PDF++ placeholder papers.
- Added validated study and assessment evidence, stable IDs, a fixed error
  taxonomy, and deterministic postmortem card actions.
- Moved 25 specialist workflows into internal academic-workflow references.
- Genericized the term, course, crosswalk, learner, and source fixtures.
- Renamed the term fixture tree `TERM_01` to `Y01_S01`, matching the
  `Y##_S##` convention already used by `Papers & Reviews/Programme/`.
- Swapped the dead `S01_2026` private-value canary for `BSc`, which is the
  token that now distinguishes an upstream path from a distribution path.
- Extended tests and the release verifier for workflow completeness, private
  template values, and stale callable commands.

## 0.1.0 - 2026-08-19

- Packaged a provider-neutral Pi runtime for an Obsidian vault.
- Added a safe Obsidian configuration with optional theme references and no
  custom CSS.
- Added `START HERE.md` and a fictional learning path.
- Added deterministic review, crosswalk, PDF, Zotero, and Canvas helpers.
- Added a release verifier for unsafe files, personal paths, invalid JSON, and
  broken links.
- Added setup, workflow, customization, troubleshooting, privacy,
  compatibility, and contribution guidance.
- Added MIT code and CC BY 4.0 content licensing.
- Added launch visuals and three product screenshots.
