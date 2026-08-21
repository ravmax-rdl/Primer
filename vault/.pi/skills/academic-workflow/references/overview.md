---
description: Build a course concept Canvas with prerequisite edges
argument-hint: "<course> [--exam]"
---
Load `canvas-gen` and `vault-syntax`; load `past-papers` when `$1` includes `--exam`. Build `Study Notes/Programme/TERM_01/<Course>/Overview.canvas`.

1. Walk matching `W##/D##/<Course>.md` notes and cluster their concepts.
2. Add prerequisite edges. Represent a syllabus topic with no note as `kind: gap`.
3. Use course data or `crosswalk.json` for colors, not CSS.
4. Write graph JSON and run `.pi/skills/canvas-gen/layout.py` with `--merge` and `--write` pointing to the course Canvas. Preserve manual placement.
5. In exam mode, annotate from classified frequency and lapses under `Study Notes/Review/<Course>/`. The script still owns coordinates.

Do not use a Canvas tool that writes to the vault root or overwrites existing placement.
