# Troubleshooting

## `/study` cannot ask interactive questions

Install or enable `pi-ask-user`, restart Pi, and confirm the `ask_user` tool is
available. `pi-quiz` is user-invoked revision; it does not replace the
model-callable tool used during a study turn.

## A prompt shows raw LaTeX or reveals the answer

The `ask_user` surface renders Markdown, not LaTeX, and it prints `context`
above the question. Send math as Unicode or inside an inline code span, keep
multi-line derivations in the note, and give a scored question no synthesized
`context`. See the interactive-prompt rules in `vault/.pi/APPEND_SYSTEM.md`.

## `/doctor` reports `missing_target`

Restore the file or update the shortcut/path mapping. Do not queue OCR; no
readable source exists.

## `/doctor` reports `no_text_layer`

The source is readable but extraction found no text. From the vault root, run
`python .pi/skills/pdf-search/index.py ocr-pages "<vault PDF>" --dpi 180`.
Read every returned page image, create the intended note, then reindex only if
you also produced searchable OCR text. The renderer does not rewrite the PDF or
manifest.

## `/doctor` reports legacy records

Re-run the index command for the source directories represented by the old
manifest. The doctor never migrates records automatically.

## Evidence validation fails

Run:

```bash
python .pi/skills/academic-workflow/learning_state.py validate "path/to/note.md"
```

Fix the named field, unknown error label, invalid marks/confidence, duplicate ID,
or malformed JSON. Validation failure leaves the note unchanged.

## Obsidian Base is empty

Enable the Bases core plugin. Confirm the note path matches your configured term
and the filename equals the Base's join key.

## `pdftotext` or `pdftoppm` is missing

Install Poppler for the current platform and confirm both executables are on
`PATH`. `pdftotext` extracts existing text; `pdftoppm` renders scan-only sources
for vision/OCR. A missing `pdftotext` records `failed`, never `no_text_layer`; a
missing `pdftoppm` fails rendering without changing the manifest.

## Release verifier fails

Run `python scripts/verify.py`. It reports generated state, personal paths,
private fixture values, stale visible prompts, missing internal references,
invalid JSON, and broken documentation links with exact paths.
