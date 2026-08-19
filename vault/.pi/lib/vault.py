#!/usr/bin/env python3
"""Resolve the Obsidian vault that owns this .pi tree.

Scripts live under `.pi/skills/<name>/`. Call `find_vault()` instead of a
hardcoded path so the kit works after a student copies `vault/` elsewhere.

Resolution order:
  1. VAULT_ROOT environment variable
  2. Walk up from the current working directory looking for `.pi/settings.json`
  3. Walk up from this file
"""

from __future__ import annotations

import os
from pathlib import Path


def find_vault(start: Path | None = None) -> Path:
    env = os.environ.get("VAULT_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if not (p / ".pi" / "settings.json").is_file():
            raise SystemExit("VAULT_ROOT=%s has no .pi/settings.json" % p)
        return p

    starts: list[Path] = []
    if start is not None:
        starts.append(Path(start).resolve())
    starts.append(Path.cwd().resolve())
    starts.append(Path(__file__).resolve().parent)

    seen: set[Path] = set()
    for s in starts:
        for p in [s, *s.parents]:
            if p in seen:
                continue
            seen.add(p)
            if (p / ".pi" / "settings.json").is_file():
                return p

    raise SystemExit(
        "Could not find the vault root (.pi/settings.json). "
        "cd into the vault, or set VAULT_ROOT to that folder."
    )


def zotero_db() -> Path:
    env = os.environ.get("ZOTERO_DB")
    if env:
        return Path(env).expanduser()
    return Path.home() / "Zotero" / "zotero.sqlite"


def pi_on_path() -> None:
    """Put `.pi/` on sys.path so `from lib.vault import ...` works."""
    import sys

    pi = Path(__file__).resolve().parent.parent
    if str(pi) not in sys.path:
        sys.path.insert(0, str(pi))
