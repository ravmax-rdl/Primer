#!/usr/bin/env python3
"""Check that a Primer checkout is complete, portable, and safe to publish."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

REQUIRED_FILES = ("README.md", "LICENSE", "LICENSE-CODE",
"LICENSE-CONTENT",
"CONTRIBUTING.md",
"CHANGELOG.md",
"docs/setup.md",
"docs/workflows.md",
"docs/customization.md",
"docs/troubleshooting.md",
"assets/hero.svg",
"assets/social-preview.svg",
"assets/architecture.svg",
"vault/START HERE.md",
"vault/.pi/settings.json",
"vault/.pi/APPEND_SYSTEM.md",
"vault/.pi/LEARNER.md",
"vault/.obsidian/app.json",)

TEXT_SUFFIXES = {
    ".base",
    ".canvas",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}
PORTABLE_CONTENT_SUFFIXES = {
    ".base",
    ".canvas",
    ".css",
    ".html",
    ".json",
    ".md",
    ".svg",
    ".txt",
    ".yaml",
    ".yml",
}

IGNORED_PARTS = {".git", ".superpowers", "__pycache__"}
SENSITIVE_NAME = re.compile(
    r"(?:recovery[-_ ]?(?:code|codes|phrase)|private[-_ ]?key|id_(?:rsa|dsa|ecdsa|ed25519)|credentials?|secrets?|auth[-_ ]?token)",
    re.IGNORECASE,
)
PERSONAL_PATHS = (
    re.compile(r"[A-Za-z]:/Users/[^/\s]+/", re.IGNORECASE),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\", re.IGNORECASE),
    re.compile(r"/Users/[^/\s]+/"),
    re.compile(r"/home/[^/\s]+/"),
    re.compile(r"file:///", re.IGNORECASE),
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_ignored(path: Path, root: Path) -> bool:
    parts = path.relative_to(root).parts
    return any(part in IGNORED_PARTS for part in parts) or parts[:2] == ("docs", "superpowers")


def is_forbidden_generated_file(path: Path, root: Path) -> bool:
    parts = path.relative_to(root).parts
    if ".pi" in parts and "cache" in parts[parts.index(".pi") + 1 :]:
        return True
    if ".obsidian" not in parts:
        return False
    obsidian_parts = parts[parts.index(".obsidian") + 1 :]
    if not obsidian_parts:
        return False
    return (
        obsidian_parts[0] in {"cache", "plugins"}
        or obsidian_parts[0] in {"workspace.json", "workspace-mobile.json"}
    )


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and not is_ignored(path, root):
            yield path


def check_links(root: Path) -> list[str]:
    errors: list[str] = []
    documents = [root / "README.md", root / "vault/START HERE.md"]
    docs = root / "docs"
    if docs.exists():
        documents.extend(sorted(docs.glob("*.md")))

    for document in documents:
        if not document.exists():
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            local_target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if local_target and not (document.parent / local_target).resolve().exists():
                errors.append(f"Broken link in {relative(document, root)}: {target}")
    return errors


def verify_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for required in REQUIRED_FILES:
        if not (root / required).is_file():
            errors.append(f"Missing required file: {required}")

    for path in iter_files(root):
        display_path = relative(path, root)
        if is_forbidden_generated_file(path, root):
            errors.append(f"Forbidden generated file: {display_path}")
            continue
        if SENSITIVE_NAME.search(path.name):
            errors.append(f"Sensitive filename: {display_path}")
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                errors.append(f"Invalid JSON: {display_path}: {error}")
                continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"LICENSE-CODE", "LICENSE-CONTENT"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix.lower() in PORTABLE_CONTENT_SUFFIXES and any(
            pattern.search(text) for pattern in PERSONAL_PATHS
        ):
            errors.append(f"Personal or external absolute path: {display_path}")

    errors.extend(check_links(root))
    return sorted(set(errors))


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1]
    errors = verify_repository(root)
    if errors:
        print("Primer release check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Primer release check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
