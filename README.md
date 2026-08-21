# Primer

Primer is a publishable Pi and Obsidian academic-agent kit. It keeps source
handling, learning evidence, assessment postmortems, and spaced repetition in a
portable vault without shipping personal learner data or credentials.

## Academic loop

```text
/study COURSE102 45 "Study Notes/Programme/TERM_01/W01/D01/Foundations of Logic.md"
      ↓
/exam COURSE102 "LEGACY102" "Study Notes/Programme/TERM_01/W01/D01/Foundations of Logic.md"
      ↓
/research "unresolved claim" "Research/Claim matrix.md"
```

Five commands are visible:

| Command | Purpose |
|---|---|
| `/study <course> <minutes> [target-note]` | Probe, teach, practice, validate evidence, set one next action |
| `/capture [source] [course] [target-note]` | Normalize one source into one note |
| `/research <question-or-topic> [target-note]` | Build claim–evidence rows and supported prose |
| `/exam <course> [question-or-paper] [target-note]` | Time, grade, classify errors, and choose a card action |
| `/doctor` | Report PDF index states without repairing data |

The 25 specialist procedures remain under the academic-workflow skill as
internal references. They do not clutter Pi's slash-command list.

## What is deterministic

Python utilities own:

- PDF resolution, provenance, states, search, and doctor output
- Evidence validation and stable record IDs
- Latest concept evidence
- Postmortem card decisions
- SM-2 schedule arithmetic
- Canvas placement
- Course-code crosswalk lookup

The model owns explanation, questioning, source comparison, and feedback. It
cannot replace deterministic outcomes with intuition.

## Install

1. Copy `vault/` to a new Obsidian vault or merge it into a version-controlled
   test vault.
2. Follow [setup](docs/setup.md).
3. Customize the generic term, course, and path fixtures before live use.
4. Run:

```bash
python -m unittest discover -s tests -v
python scripts/verify.py
```

5. Open `vault/START HERE.md` and run `/doctor` before source-dependent work.

## Safety

- One note per turn; no autonomous bulk rewrites.
- Dynamic mastery stays in validated target-note evidence, not `LEARNER.md`.
- Missing sources are not mislabeled as OCR work.
- Grading names its source and confidence.
- Assignment help critiques and teaches; it does not ghost-write submissions.
- Generated indexes and caches stay under `.pi/cache/` and are rejected from a
  release checkout.

See [workflows](docs/workflows.md), [customization](docs/customization.md), and
[troubleshooting](docs/troubleshooting.md). Contributions follow
[CONTRIBUTING.md](CONTRIBUTING.md). Code and content licenses are in
[LICENSE-CODE](LICENSE-CODE) and [LICENSE-CONTENT](LICENSE-CONTENT).
