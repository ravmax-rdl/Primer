# Primer vault

This is the portable Obsidian fixture installed with Primer.

## Commands

| Command | Purpose |
|---|---|
| `/study <course> <minutes> [target-note]` | Closed-loop learning and evidence |
| `/capture [source] [course] [target-note]` | One-source, one-note ingestion |
| `/research <question-or-topic> [target-note]` | Claim–evidence research |
| `/exam <course> [question-or-paper] [target-note]` | Timed attempt and postmortem |
| `/doctor` | Read-only PDF source health |

## Fixture paths

- Term: `Study Notes/Programme/Y01_S01/`
- Demo course: `Foundations of Logic`
- Demo day note: `W01/D01/Foundations of Logic.md`
- Cards: `Study Notes/Review/Foundations of Logic/`
- Crosswalk: `Papers & Reviews/Programme/crosswalk.json`
- Answer scripts: `Papers & Reviews/Programme/Y01_S01/Answer Scripts/<year>/`

Replace fictional values before live use. A day-note filename must equal its
course Base join key.

## Rules

- One note per turn.
- Dynamic state is validated evidence in the target note, not learner-profile
  prose.
- Missing PDFs are not OCR work.
- Scan OCR resolves PDF++ placeholders and renders the real target with
  `pdf-search/index.py ocr-pages`.
- Grading states source and confidence.
- Cards require deterministic postmortem action.
- Credentials and recovery material do not belong in the vault.
