#!/usr/bin/env python3
"""Sidecar plaintext index for vault PDFs.

Resolves Obsidian URI-shortcut .pdf files (file:///...) to the real PDF,
extracts page text with pdftotext, and falls back to the text-extractor OCR
cache. Never writes next to the PDF (sidecars would sync as junk).

Usage:
  python3 index.py index [--root DIR] [--limit N]
  python3 index.py search <query> [--path SUBSTR] [--n 20]
  python3 index.py resolve <vault-relative-or-abs.pdf>
  python3 index.py pages <vault-relative-or-abs.pdf>
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib.vault import find_vault  # noqa: E402

VAULT = find_vault()
CACHE = VAULT / ".pi" / "cache" / "pdf-index"
OCR_CACHE = VAULT / ".obsidian" / "plugins" / "text-extractor" / "cache"
PAGE_RE = re.compile(r"# Page (\d+)\^page=\d+")
CODE_RE = re.compile(r"(SCS|ENH?|EN|IS)[ _-]?(\d{4})", re.I)


def cache_dir() -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "pages").mkdir(exist_ok=True)
    return CACHE


def rel(p: Path) -> str:
    try:
        return p.relative_to(VAULT).as_posix()
    except ValueError:
        return str(p)


def is_uri_shortcut(path: Path) -> str | None:
    try:
        data = path.read_bytes()[:400]
    except OSError:
        return None
    if data.startswith(b"%PDF"):
        return None
    text = data.decode("utf-8", errors="replace").strip()
    if text.startswith("file:"):
        return text.splitlines()[0].strip()
    return None


def uri_to_path(uri: str) -> Path:
    parsed = urllib.parse.urlparse(uri)
    raw = urllib.parse.unquote(parsed.path)
    if re.match(r"^/[A-Za-z]:", raw):
        raw = raw[1:]
    return Path(raw)


def resolve_pdf(path: Path) -> tuple[Path | None, str]:
    """Return (real_pdf_or_none, kind). kind: pdf | shortcut | missing | unreadable."""
    try:
        uri = is_uri_shortcut(path)
    except OSError:
        return None, "unreadable"
    if uri:
        target = uri_to_path(uri)
        if target.exists() and target.stat().st_size > 200:
            return target, "shortcut"
        return None, "missing"
    try:
        if path.stat().st_size > 200 and path.read_bytes()[:4] == b"%PDF":
            return path, "pdf"
    except OSError:
        return None, "unreadable"
    return None, "unreadable"


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def pdftotext_pages(pdf: Path) -> list[str]:
    out = cache_dir() / "pages" / (sha1(str(pdf)) + ".extract.txt")
    try:
        r = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), str(out)],
            capture_output=True,
            text=True,
            timeout=90,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    if r.returncode not in (0, 1) or not out.exists():
        return []
    text = out.read_text(encoding="utf-8", errors="replace")
    pages = text.split("\f")
    cleaned = [p.strip() for p in pages]
    while cleaned and not cleaned[-1]:
        cleaned.pop()
    if len(cleaned) == 1 and len(cleaned[0]) <= 1:
        return []
    return cleaned


def ocr_pages_for(vault_rel: str) -> list[str]:
    if not OCR_CACHE.exists():
        return []
    needle = vault_rel.replace("\\", "/")
    for cache_file in OCR_CACHE.glob("*.json"):
        try:
            data = json.loads(cache_file.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            continue
        path = str(data.get("path", "")).replace("\\", "/")
        if path != needle and not path.endswith(needle.split("/")[-1]):
            continue
        raw = data.get("text") or ""
        chunks = PAGE_RE.split(raw)
        # split keeps capture groups: [pre, n, body, n, body, ...]
        pages: dict[int, str] = {}
        i = 1
        while i + 1 < len(chunks):
            try:
                n = int(chunks[i])
            except ValueError:
                i += 2
                continue
            pages[n] = chunks[i + 1].strip()
            i += 2
        if pages:
            max_n = max(pages)
            return [pages.get(k, "") for k in range(1, max_n + 1)]
    return []


def extract(vault_pdf: Path) -> tuple[list[str], str, str]:
    real, kind = resolve_pdf(vault_pdf)
    pages: list[str] = []
    if real is not None:
        pages = pdftotext_pages(real)
        source = "pdftotext"
    else:
        source = kind
    if not pages:
        ocr = ocr_pages_for(rel(vault_pdf))
        if ocr:
            pages = ocr
            source = "ocr-cache"
    return pages, kind if real is None and source != "ocr-cache" else kind, source


def store_pages(vault_rel: str, pages: list[str]) -> Path:
    dest = cache_dir() / "pages" / (sha1(vault_rel) + ".txt")
    parts = []
    for i, page in enumerate(pages, 1):
        parts.append("===== PAGE %d =====\n%s" % (i, page))
    dest.write_text("\n\n".join(parts), encoding="utf-8")
    return dest


def iter_pdfs(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", ".obsidian", ".pi", ".trash", "Bin"}]
        for name in filenames:
            if name.lower().endswith(".pdf"):
                yield Path(dirpath) / name


def cmd_index(root: Path, limit: int | None) -> None:
    manifest_path = cache_dir() / "manifest.jsonl"
    seen: dict[str, dict] = {}
    if manifest_path.exists():
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            seen[rec["path"]] = rec
    n = 0
    updated = 0
    for pdf in iter_pdfs(root):
        vault_rel = rel(pdf)
        try:
            st = pdf.stat()
        except OSError:
            continue
        prev = seen.get(vault_rel)
        stamp = "%s:%s" % (int(st.st_mtime), st.st_size)
        if prev and prev.get("stamp") == stamp and prev.get("pages", 0) >= 0:
            n += 1
            if limit and n >= limit:
                break
            continue
        pages, kind, source = extract(pdf)
        if pages:
            store_pages(vault_rel, pages)
        rec = {
            "path": vault_rel,
            "kind": kind,
            "source": source,
            "pages": len(pages),
            "chars": sum(len(p) for p in pages),
            "stamp": stamp,
        }
        seen[vault_rel] = rec
        updated += 1
        n += 1
        print("%s\t%s\t%d pages\t%s" % (source, vault_rel, len(pages), kind))
        if limit and n >= limit:
            break
    with manifest_path.open("w", encoding="utf-8") as f:
        for rec in sorted(seen.values(), key=lambda r: r["path"]):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("# indexed %d files, wrote %d, manifest %d" % (n, updated, len(seen)), file=sys.stderr)


def snippet(text: str, query: str, width: int = 180) -> str:
    low = text.lower()
    q = query.lower()
    i = low.find(q)
    if i < 0:
        return " ".join(text.split())[:width]
    start = max(0, i - 60)
    end = min(len(text), i + len(query) + 120)
    s = " ".join(text[start:end].split())
    return ("…" if start else "") + s + ("…" if end < len(text) else "")


def cmd_search(query: str, path_filter: str | None, n: int) -> None:
    manifest_path = cache_dir() / "manifest.jsonl"
    if not manifest_path.exists():
        print("No index yet. Run: python3 index.py index", file=sys.stderr)
        sys.exit(1)
    q = query.lower()
    hits = []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec.get("pages", 0) <= 0:
            continue
        if path_filter and path_filter.lower() not in rec["path"].lower():
            continue
        page_file = cache_dir() / "pages" / (sha1(rec["path"]) + ".txt")
        if not page_file.exists():
            continue
        body = page_file.read_text(encoding="utf-8", errors="replace")
        current_page = 1
        buf = []
        for raw in body.splitlines():
            m = re.match(r"===== PAGE (\d+) =====", raw)
            if m:
                if buf:
                    text = "\n".join(buf)
                    if q in text.lower():
                        hits.append((rec["path"], current_page, snippet(text, query)))
                current_page = int(m.group(1))
                buf = []
                continue
            buf.append(raw)
        if buf:
            text = "\n".join(buf)
            if q in text.lower():
                hits.append((rec["path"], current_page, snippet(text, query)))
        if len(hits) >= n * 4:
            break
    for path, page, snip in hits[:n]:
        name = Path(path).name
        cite = "[[%s#page=%d|%s, p.%d]]" % (name, page, Path(name).stem, page)
        line = "%s\tp.%d\t%s\t%s" % (path, page, cite, snip)
        print(line.encode("utf-8", errors="replace").decode("utf-8"))
    print("# %d hit(s)" % min(len(hits), n), file=sys.stderr)


def cmd_resolve(target: str) -> None:
    p = Path(target)
    if not p.is_absolute():
        p = VAULT / target
    real, kind = resolve_pdf(p)
    print("kind\t%s" % kind)
    print("vault\t%s" % rel(p))
    print("real\t%s" % (real if real else ""))


def cmd_pages(target: str) -> None:
    p = Path(target)
    if not p.is_absolute():
        p = VAULT / target
    pages, kind, source = extract(p)
    print("# %s kind=%s source=%s pages=%d" % (rel(p), kind, source, len(pages)))
    for i, page in enumerate(pages, 1):
        print("===== PAGE %d =====" % i)
        print(page)
        print()


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    cmd = args[0]
    if cmd == "index":
        root = VAULT
        limit = None
        if "--root" in args:
            root = Path(args[args.index("--root") + 1])
        if "--limit" in args:
            limit = int(args[args.index("--limit") + 1])
        cmd_index(root, limit)
    elif cmd == "search" and len(args) >= 2:
        path_filter = None
        n = 20
        rest = args[1:]
        if "--path" in rest:
            i = rest.index("--path")
            path_filter = rest[i + 1]
            rest = rest[:i] + rest[i + 2 :]
        if "--n" in rest:
            i = rest.index("--n")
            n = int(rest[i + 1])
            rest = rest[:i] + rest[i + 2 :]
        cmd_search(" ".join(rest), path_filter, n)
    elif cmd == "resolve" and len(args) == 2:
        cmd_resolve(args[1])
    elif cmd == "pages" and len(args) == 2:
        cmd_pages(args[1])
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
