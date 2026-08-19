---
type: reference
tags:
  - primer/onboarding
---
# Start here

Primer is an Obsidian vault with a Pi tutor attached. The included lesson is fictional. Use it to test the workflow before adding personal notes.

> [!warning] Read before running an agent
> Obsidian files stay on this machine unless you configure sync. A hosted model receives the prompts, note excerpts, tool output, and attachments that Pi puts in context. Web, PDF, Zotero, and provider extensions may contact other services. Do not store credentials, recovery material, private keys, tokens, or `.env` files in this vault.

## First five minutes

- [ ] Open this `vault/` folder as an Obsidian vault.
- [ ] Leave Restricted Mode on unless you intentionally install a community plugin. Primer's demo needs no community plugin.
- [ ] From the repository root, run `python scripts/verify.py .` on Windows or `python3 scripts/verify.py .` on macOS/Linux.
- [ ] Install Pi and the core packages from the repository's [setup guide](../docs/setup.md).
- [ ] Open a terminal in this `vault/` folder and run `pi`.
- [ ] Review Pi's project trust prompt. Trust only the checkout you inspected.

## Run the demo

1. Open [[Study Notes/BSc/S01_2026/W01/D01/Discrete Mathematics]].
2. Open [[Study Notes/BSc/S01_2026/Discrete Mathematics/Lecture Notes.base]] and confirm the day note appears.
3. In Pi, run `/probe Discrete Mathematics` and name the open day note when asked.
4. Run `/teach Discrete Mathematics` for one reasoning step and one lock-in question.
5. Run `/cards Study Notes/BSc/S01_2026/W01/D01/Discrete Mathematics.md` only after the idea is locked.
6. Open [[Study Notes/Review/Due.base]] to inspect the two included sample cards.

The demo may change its note and cards. Use Git to reset the fictional files after testing.

## Appearance

Primer does not ship custom CSS or third-party theme files. `.obsidian/appearance.json` references **Minimal** because it is the theme used in the project screenshots. The source vault also has **Baseline** as an alternative. Install either from Obsidian's theme browser, or keep the default theme; the workflow and demo remain readable.

Observed source-vault versions at packaging time:

| Theme | Author | Observed version | Minimum Obsidian |
|---|---|---:|---:|
| Minimal | `@kepano` | 9.0.2 | 1.13.0 |
| Baseline | Alexis C | 3.2.12 | 1.13.4 |

These are references, not bundled dependencies or version pins.

## Add your first course

1. Copy `Templates/Lecture note.md` into `Study Notes/BSc/S01_2026/W01/D01/`.
2. Rename it to the exact course name.
3. Create or update the course's `Lecture Notes.base` with the same filename filter.
4. Replace the demo frontmatter with your course, week, day, and date.
5. Keep source links at the top and generated teaching sections below them.

## When something breaks

- Pi cannot see project commands: confirm the terminal's current directory is this `vault/` folder.
- Bases is missing: update Obsidian and enable the Bases core plugin.
- Minimal is not installed: choose the default theme or install Minimal from Appearance settings.
- A PDF has no text: install `pdftotext` or configure the optional OCR path.
- A guard block is wrong: inspect the path first, then change `.pi/extensions/guard/patterns.ts` deliberately.

Full references: [setup](../docs/setup.md), [workflows](../docs/workflows.md), [customization](../docs/customization.md), and [troubleshooting](../docs/troubleshooting.md).
