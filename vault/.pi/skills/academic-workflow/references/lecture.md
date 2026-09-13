---
description: Scaffold a lecture note from a lecture PDF with correct frontmatter
argument-hint: "<course> [week] [day]"
---
Load `vault-syntax`. Create the lecture note `Study Notes/Programme/Y01_S01/W${2:-##}/D${3:-##}/$1.md` — ask me the week/day if not given.

- The filename MUST equal the exact course name "$1" (Bases join key), or the note vanishes from its `Lecture Notes.base`.
- Use the Y01_S01 frontmatter shape from `vault-syntax`: `created`/`updated` (today), `course: Programme`, `subject:` (the code for $1), `type: lecture`, `status: [in-progress]`, `tags`, `banner`, `background`. Do not drop `banner`/`background` — the Bases cards read them.
- If a lecture PDF for this session is in the course folder or `Bin/`, embed it with a pdf++ link (`![[Name.pdf#page=1|Name, p.1]]` — `rect=` only if copied from pdf++) and outline its sections as headings. Put an empty `## Understanding map` with `- [?]` stubs for the main strands so `teach.md` has somewhere to write.
- Do NOT overwrite an existing note — edit it. Then offer to run `teach.md $1` to fill it.
