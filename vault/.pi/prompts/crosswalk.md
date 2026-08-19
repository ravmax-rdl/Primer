---
description: Build or refresh the BSc legacy→current course-code map
---
Load `past-papers` and `pdf-search`. Refresh `Papers & Reviews/BSc/Crosswalk.md` and `crosswalk.json`.

Rules:
- Current codes come from lecture-note `subject:` frontmatter and the UGVLE Y1 S1 timetable, not from filenames alone.
- Map every `SCS/ENH/EN 11xx/12xx/13xx` code in `Papers & Reviews/BSc/Y01_S01/`. Flag `low` confidence and empty-current rows explicitly.
- Do not bulk-rename papers. One note: edit Crosswalk.md (and the JSON if the map changed).
- Show me any row whose confidence is not `high` and wait before using it in `/classify` or `/mock`.
