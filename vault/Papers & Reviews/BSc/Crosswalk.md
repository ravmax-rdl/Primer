---
type: reference
course: BSc.
tags:
  - meta/vault
  - papers/crosswalk
---
# BSc course-code crosswalk

> [!danger] Validate `low` rows before `/mock` or `/classify`
> A wrong link silently poisons every downstream exam command. Today that is **SCS 1104** (Mathematical Methods I). Database I (`SCS 1103` / `SCS 1203`) has no Y1 S1 successor — exclude it.

UCSC codes: prefix `SCS` / `ENH` / `EN`; first digit = year; **second digit = syllabus revision** (1 = 1100, 2 = 1200, 3 = 1300). Filenames like `SCS 1201-SCS 1101` are the same paper sitting on a revision boundary.

## Current semester (S01_2026)

| Code | Course (filename = Bases join key) | Evidence |
|---|---|---|
| SCS 1301 | Data Structures and Program Design in C | Lecture `subject:` + UGVLE 2025 timetable |
| SCS 1302 | Discrete Mathematics | Lecture `subject:` + UGVLE |
| SCS 1303 | Introduction to Software Engineering | Lecture `subject:` + UGVLE |
| SCS 1304 | Problem Solving Strategies and Computation Approaches | Lecture `subject:` + UGVLE |
| SCS 1305 | Computer Systems | Lecture `subject:` + UGVLE |
| SCS 1306 | Linear Algebra | Lecture `subject:` + UGVLE |
| SCS 1307 | Probability and Statistics | Lecture `subject:` + UGVLE |
| ENH 1301 | Application Laboratory | Lecture `subject:` + UGVLE |
| ENH 1302 | Communication Skills | Lecture `subject:` + UGVLE |

Machine copy: [[crosswalk.json]]

## Legacy → current

| Legacy | Legacy title | Current | Confidence | Notes |
|---|---|---|---|---|
| SCS 1101 | Data Structures and Algorithms I | SCS 1301 | high | Dual-coded with 1201. 1301 also absorbs Programming. |
| SCS 1102 | Programming I | SCS 1301 | high | Via 1202 Programming Using C. |
| SCS 1103 | Database I | — | high | Dual-coded with 1203. **No Y1 S1 successor.** |
| SCS 1104 | Mathematical Methods I | SCS 1306 / 1307? | **low** | Do not auto-include in mocks. Confirm from paper contents. |
| SCS 1105 | Computer Systems | SCS 1305 | high | Via 1205. |
| SCS 1106 | Laboratory I | ENH 1301 | high | Via 1206. |
| ENH 1101 | Enhancement (communication line) | ENH 1302 | medium | Confirm from paper header. |
| EN 1101 | Communication Skills | ENH 1302 | high | Via EN 1201. |
| SCS 1201 | Data Structures & Algorithms I | SCS 1301 | high | Merged with 1202 into 1301. |
| SCS 1202 | Programming Using C | SCS 1301 | high | |
| SCS 1203 | Database I | — | high | **Exclude from current-semester mocks.** |
| SCS 1204 | Discrete Mathematics I | SCS 1302 | high | |
| SCS 1205 | Computer Systems | SCS 1305 | high | |
| SCS 1206 | Laboratory I | ENH 1301 | high | |
| SCS 1207 | Software Engineering I | SCS 1303 | high | |
| ENH 1201 | Communication Skills | ENH 1302 | high | |
| EN 1201 | Communication Skills | ENH 1302 | high | 2025 timetable alias. |
| EN 1202 | Application Laboratory | ENH 1301 | high | 2025 timetable alias. |

## Gaps

- **No current equivalent:** SCS 1103 / SCS 1203 Database I.
- **No historical Y1 S1 papers in the typical 2017–2025 Y01_S01 corpus:** SCS 1304, SCS 1306, SCS 1307 (unless 1104 is later confirmed).

## Sources

- Vault lecture frontmatter (`subject:`).
- [UGVLE 2025 Y1 S1 timetable](https://ugvle.ucsc.cmb.ac.lk/pluginfile.php/2/course/section/2/CS%20%20IS%20Undergraduate%20Time%20Table%20-%20First%20Semester%202025.pdf)
- [UCSC BSc CS programme page](https://ucsc.cmb.ac.lk/ug-computer-science/) (1200 titles)
- UCSC Undergraduate Handbook 2014 (1100 titles)
