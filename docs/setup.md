# Setup

1. Copy `vault/` to a version-controlled test location.
2. Open it in Obsidian and enable the Bases core plugin.
3. Install Pi and the packages listed in `vault/.pi/settings.json`.
4. Copy `.pi/LEARNER.md` fields from the generic template; do not add dynamic
   mastery.
5. Replace the fictional term, course, and crosswalk fixtures.
6. Install Poppler (`pdftotext` and `pdftoppm`) if PDF extraction or scan OCR is
   required.
7. From the repository root, run:

```bash
python -m unittest discover -s tests -v
python scripts/verify.py
```

8. From the vault root, run:

```bash
python .pi/skills/pdf-search/index.py doctor
python .pi/skills/academic-workflow/learning_state.py --help
```

An absent manifest is expected before indexing. Index only source directories
you intend to use, then rerun `/doctor`.

## First live test

Use the fictional `Foundations of Logic` note or a copied course fixture:

```text
/study COURSE102 20 "Study Notes/Programme/Y01_S01/W01/D01/Foundations of Logic.md"
```

Confirm that the session writes only the selected note and appends a valid
`academic-evidence` record. Reset the fictional fixture with Git after testing.
