# Troubleshooting

Run the release check first:

```bash
python scripts/verify.py .
```

Use `python3` on systems where `python` is not Python 3.

## Pi does not load Primer commands

**Check:** `pwd` or the Windows terminal path must end in `Primer/vault` before `pi` starts.

**Fix:** exit Pi, change into `vault/`, and launch it again. Do not add duplicate prompt or skill paths to `.pi/settings.json`.

## Pi reports an untrusted project

Primer contains executable Python and TypeScript. Inspect `.pi/`, confirm the checkout source, then accept Pi's trust prompt. Do not trust a modified archive you have not reviewed.

## `/teach` prints choices instead of opening a picker

Install `pi-ask-user` and restart Pi:

```bash
pi install npm:pi-ask-user
```

The `/quiz` command from `pi-quiz` is user-invoked revision. It does not replace the model-callable `ask_user` tool used by `/probe` and `/teach`.

## Obsidian cannot open a Base

Update Obsidian and enable the Bases core plugin under **Settings → Core plugins**. Primer targets Obsidian 1.13.0 or newer. Open `Study Notes/BSc/S01_2026/Discrete Mathematics/Lecture Notes.base` directly to test it.

If the table is empty, confirm the day note is named `Discrete Mathematics.md`. The filename is the join key.

## Minimal is missing or the vault looks different

Primer references Minimal but does not bundle it. Install Minimal from **Settings → Appearance → Themes → Manage**, choose Baseline as an alternative, or use Obsidian's default theme. No custom CSS is required.

## Review cards do not appear

Check the card's YAML fields and folder:

```yaml
due: 2026-08-19
interval: 0
ease: 2.5
reps: 0
lapses: 0
source: "[[Study Notes/BSc/S01_2026/W01/D01/Discrete Mathematics]]"
```

Cards belong under `Study Notes/Review/<Course>/`. `Due.base` shows cards whose `due` date is today or earlier.

## `pdftotext` is not found

PDF indexing is optional. Install Poppler, put `pdftotext` on `PATH`, and restart the terminal. Confirm with `pdftotext -v` before running the indexer.

A scan may produce no text even when Poppler is installed. Configure an OCR source or skip the file; Primer must not invent missing pages.

## Zotero lookup cannot find its database

Close no files and do not point the script at a synced copy. Set the path for the current shell:

```bash
# macOS or Linux
export ZOTERO_DB="$HOME/Zotero/zotero.sqlite"

# PowerShell
$env:ZOTERO_DB = "$HOME\Zotero\zotero.sqlite"
```

The query helper copies the database to a temporary location before reading it.

## The secrets guard blocks an ordinary file

Read the blocked path without opening the file. If the name is safe but matches a broad rule, add a focused test to `tests/guard.test.mjs`, then narrow `vault/.pi/extensions/guard/patterns.ts`. Do not disable the extension to get past an unexplained block.

## The verifier flags local Obsidian state

Delete generated workspace or cache files from the checkout after closing Obsidian. The repository ignores them, but the verifier reports them if they remain in the release tree. Never force-add workspace, sync, plugin binary, or `.pi/cache` files.

## A command uses the wrong provider or model

Primer is provider neutral. Inspect Pi's active provider and user-level settings. Project files should not force Anthropic, Cursor, or another subscription connector. Re-run `/login` if the selected provider is unavailable.
