# Troubleshooting

## `/study` cannot ask interactive questions

Install or enable `pi-ask-user`, restart Pi, and confirm the `ask_user` tool is
available. `pi-quiz` is user-invoked revision; it does not replace the
model-callable tool used during a study turn.

## `/doctor` reports `missing_target`

Restore the file or update the shortcut/path mapping. Do not queue OCR; no
readable source exists.

## `/doctor` reports `no_text_layer`

The source is readable but extraction found no text. OCR may be appropriate.
After OCR completes, reindex the source and rerun `/doctor`.

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

## `pdftotext` is missing

Install Poppler for the current platform and confirm `pdftotext` is on `PATH`.
A missing backend is `failed`, not `no_text_layer`.

## Release verifier fails

Run `python scripts/verify.py`. It reports generated state, personal paths,
private fixture values, stale visible prompts, missing internal references,
invalid JSON, and broken documentation links with exact paths.
