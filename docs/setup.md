# Setup

Primer's repository root contains public documentation and release checks. The `vault/` directory is the Obsidian vault and Pi project.

## Core requirements

| Requirement | Minimum or tested version | Needed for |
|---|---:|---|
| Obsidian | 1.13.0 or newer | Notes, Bases, Canvas, and the demo |
| Node.js | 22.19.0 or newer | Pi's declared runtime requirement |
| Pi | Tested with 0.84.2 | Agent workflow |
| Python | 3.10 or newer | SM-2, crosswalk, PDF, Zotero, Canvas, and release scripts |
| Git | Current supported release | Clone, updates, and demo reset |

Primer targets Windows, macOS, and Linux. The Python scripts use only the standard library.

## Install

Use GitHub's **Code** menu to copy this repository's clone URL, clone it into a folder named `Primer`, then check the checkout:

```bash
cd Primer
python scripts/verify.py .
```

On macOS or Linux, use `python3` when `python` is not mapped to Python 3.

Install Pi from its published npm package:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
pi --version
```

Install the two packages used by the core demo:

```bash
pi install npm:pi-obsidian
pi install npm:pi-ask-user
```

The package versions observed during release preparation were `pi-obsidian` 0.2.3 and `pi-ask-user` 0.14.0. They are compatibility evidence, not permanent pins.

Open `vault/` in Obsidian. Then start Pi from the same directory:

```bash
cd vault
pi
```

Review Pi's project trust prompt. Pi discovers `.pi/prompts`, `.pi/skills`, `.pi/extensions`, and `.pi/settings.json` from the current project directory. Configure any Pi-supported provider through Pi's `/login` flow. Primer does not require a particular provider or subscription.

Open `START HERE.md` and run the fictional demo before adding private notes.

## Optional features

| Feature | Package or tool | Observed package version | Notes |
|---|---|---:|---|
| Web and remote sources | `pi-web-access` | 0.24.0 | Network requests may disclose queries and fetched URLs. |
| Markdown preview | `pi-markdown-preview` | 0.14.1 | Useful before writing Mermaid or math-heavy notes. |
| User-invoked self-test | `pi-quiz` | Not pinned | Separate from the model-callable `pi-ask-user` tool. |
| Academic sub-agent | `@tintinweb/pi-subagents` | Not pinned | Enables `.pi/agents/academic.md`. |
| PDF extraction | `pdftotext` from Poppler | OS package | Required only for PDF indexing. |
| Document export | Pandoc | OS package | Required only for export workflows. |
| Zotero lookup | Zotero desktop | Local application | Set `ZOTERO_DB` if the database is outside the default Zotero folder. |

Install only the Pi packages you use:

```bash
pi install npm:pi-web-access
pi install npm:pi-markdown-preview
pi install npm:pi-quiz
pi install npm:@tintinweb/pi-subagents
```

## Optional PDF tools

- Windows: install a maintained Poppler build and put `pdftotext.exe` on `PATH`.
- macOS with Homebrew: `brew install poppler pandoc`.
- Debian or Ubuntu: `sudo apt install poppler-utils pandoc`.

Check the commands before indexing:

```bash
pdftotext -v
pandoc --version
python .pi/skills/pdf-search/index.py index --limit 1
```

Generated PDF text lives under `.pi/cache/` and is ignored by Git.

## Obsidian appearance

Primer does not bundle custom CSS, themes, or plugin binaries. The committed appearance setting references **Minimal**, the theme used in the screenshots. The source vault also has **Baseline** installed as an alternative.

- Minimal by `@kepano`: observed at 9.0.2, minimum Obsidian 1.13.0.
- Baseline by Alexis C: observed at 3.2.12, minimum Obsidian 1.13.4.

Install either through **Settings → Appearance → Themes → Manage**. The default Obsidian theme remains supported. No community plugin is required for the demo.

## Update

Pull repository changes separately from Pi and package updates:

```bash
git pull
pi update --self
pi update --extensions
python scripts/verify.py .
```

Review changes to `.pi/`, `.obsidian/`, and your note schemas before merging them into a live student vault.
