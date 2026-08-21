---
description: Build or refresh the Programme legacy→current course-code map
---
Load `past-papers` and `pdf-search`. Refresh `Papers & Reviews/Programme/Crosswalk.md` and `crosswalk.json`.

Rules:
- Current codes come from lecture-note `subject:` frontmatter and the Programme Portal Y1 S1 timetable, not from filenames alone.
- Map every `SCS/ENH/EN 11xx/12xx/13xx` code in `Papers & Reviews/Programme/Y01_S01/`. Flag `low` confidence and empty-current rows explicitly.
- Do not bulk-rename papers. One note: edit Crosswalk.md (and the JSON if the map changed).
- Show me any row whose confidence is not `high` and wait before using it in `classify.md` or `mock.md`.
