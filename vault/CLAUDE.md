# Primer vault conventions

This vault uses Pi for an academic learning workflow. Work consists of reading and editing Markdown, Bases, and Canvas files while preserving Obsidian syntax and the vault's joins.

## Safety

- Never read, print, copy, move, or transmit credentials, recovery material, private keys, tokens, or `.env` files.
- Treat hosted model calls and network tools as data disclosure. Use only the note content required for the current task.
- If a task may touch sensitive material, stop and ask the user before continuing.

## Integrity and structure

- Work on one target note per turn. Avoid bulk edits and renames.
- Edit an existing note instead of creating a near-copy.
- Notes under `Study Notes/BSc/S01_2026/W##/D##/` must use the exact course name. `Lecture Notes.base` uses the filename as its join key.
- Put attachments in `Bin/` and review cards in `Study Notes/Review/<Course>/`.

## Syntax sources

- `Markdown Snippets.md` is the human-readable syntax catalog.
- `.pi/skills/vault-syntax/SKILL.md` defines the subset agents may emit.
- `.pi/APPEND_SYSTEM.md` and `.pi/LEARNER.md` define the learning protocol.
