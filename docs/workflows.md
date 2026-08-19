# Workflows

Primer keeps the conversation, source note, review cards, and exam artifacts connected. Start every session by naming one target note.

## Probe, teach, retain

1. Open the day's course note.
2. Run `/probe <course> [note]`.
3. Confirm the understanding map. Correct a strand label before teaching if needed.
4. Run `/teach <course> [note]`.
5. Pi shows a Mermaid dependency plan, teaches one reasoning step, and asks one lock-in question through `ask_user`.
6. After a strand is locked, run `/cards <note>`.
7. Use `/review [course] [count]` to grade due cards from 0 to 5. `sm2.py` writes the next schedule.

Understanding-map states:

| Marker | State | Meaning |
|---|---|---|
| `- [x]` | known | The learner can retrieve and use it. |
| `- [/]` | edge | Partly available; one targeted step may lock it. |
| `- [?]` | unknown | Not established yet. |
| `- [!]` | blocked | A prerequisite or source is missing. |

## Review

Cards live under `Study Notes/Review/<Course>/`. Each card tests one fact or operation and has a `source` link to the lesson note. Do not calculate `due`, `interval`, `ease`, `reps`, or `lapses` by hand.

```bash
python .pi/skills/spaced-repetition/sm2.py due "Study Notes/Review"
python .pi/skills/spaced-repetition/sm2.py peek "Study Notes/Review/Discrete Mathematics/Implication.md"
```

`Study Notes/Review/Due.base` gives an Obsidian view of the queue. Pi still owns grading and scheduling.

## Exercises and assignments

Use `/exercises <course> [topic]` after teaching and recall. Attempt each problem before asking for feedback.

For an assignment, Primer may identify gaps, explain a method, or critique a learner-authored attempt. It must not write a submission for the learner.

## Past papers and mocks

1. Run the course-code lookup before mixing legacy and current papers.
2. Use `/classify <course>` to create one topic bank per turn.
3. Use `/mock <course> [minutes]` for timed, one-question-at-a-time practice.
4. Use `/postmortem <mock>` to label each miss as a knowledge gap, misconception, or careless error.
5. Create cards for gaps and misconceptions, not every careless error.

```bash
python .pi/skills/past-papers/lookup.py "SCS 1204"
```

The included classified-paper note is fictional. Real exam files and marking schemes are not part of Primer.

## Maps and research

- `/overview <course>` builds or merges a concept Canvas. `layout.py` owns coordinates.
- `/gap <course>` reports source material without a matching day note.
- `/paper <source>` creates a literature note from a URL, DOI, or local PDF.
- `/find <query>` searches notes and configured source indexes.
- `/cite <query>` creates a citation note from a verified Zotero record.
- `/source <claim>` traces a claim back to a note or page.

Network and source extensions are optional. Read the [privacy section](../README.md#privacy-and-security) before enabling them.
