#!/usr/bin/env python3
"""Portable sidecar text index for vault PDFs.

Usage:
  python index.py index [--root DIR] [--limit N]
  python index.py search <query> [--path SUBSTR] [--n 20]
  python index.py resolve <vault-relative-or-abs.pdf>
  python index.py pages <vault-relative-or-abs.pdf>
  python index.py ocr-pages <vault-relative-or-abs.pdf> [--dpi 200]
  python index.py doctor [--manifest PATH]
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
from collections import Counter
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple

PI_DIR = Path(__file__).resolve().parents[2]
if str(PI_DIR) not in sys.path:
    sys.path.insert(0, str(PI_DIR))

from lib.vault import find_vault

VAULT = find_vault()
CACHE = VAULT / ".pi" / "cache" / "pdf-index"
OCR_CACHE = VAULT / ".obsidian" / "plugins" / "text-extractor" / "cache"
PAGE_RE = re.compile(r"# Page (\d+)\^page=\d+")
URI_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
MANIFEST_FIELDS = {
    "path",
    "kind",
    "source",
    "resolved_path",
    "status",
    "pages",
    "text_pages",
    "chars",
    "content_hash",
    "extraction_backend",
    "extracted_at",
    "source_stamp",
    "failure_reason",
}


class SourceStatus(StrEnum):
    INDEXED = "indexed"
    MISSING_TARGET = "missing_target"
    UNSUPPORTED_URI = "unsupported_uri"
    UNREADABLE = "unreadable"
    NO_TEXT_LAYER = "no_text_layer"
    OCR_PENDING = "ocr_pending"
    FAILED = "failed"


class Resolution(NamedTuple):
    status: SourceStatus | None
    path: Path | None
    failure_reason: str | None
    kind: str = "pdf"


class ExtractionResult(NamedTuple):
    status: SourceStatus
    pages: int
    text_pages: int
    chars: int
    backend: str | None
    failure_reason: str | None
    page_text: tuple[str, ...] = ()


def cache_dir() -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "pages").mkdir(exist_ok=True)
    return CACHE


def canonical_manifest_path(value: str) -> str:
    return value.replace("\\", "/")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(VAULT.resolve()).as_posix()
    except ValueError:
        return canonical_manifest_path(str(path))


def read_shortcut_uri(path: Path) -> str | None:
    data = path.read_bytes()[:400]
    if data.startswith(b"%PDF"):
        return None
    first_line = data.decode("utf-8", errors="replace").strip().splitlines()
    if not first_line:
        return None
    candidate = first_line[0].strip()
    return candidate if URI_RE.match(candidate) else None


def is_uri_shortcut(path: Path) -> str | None:
    try:
        return read_shortcut_uri(path)
    except OSError:
        return None


def uri_to_path(uri: str) -> Path:
    parsed = urllib.parse.urlparse(uri)
    if parsed.scheme.lower() != "file":
        raise ValueError("unsupported URI scheme: %s" % (parsed.scheme or "none"))
    raw = urllib.parse.unquote(parsed.path)
    if parsed.netloc and parsed.netloc not in {"", "localhost"}:
        raw = "//%s%s" % (parsed.netloc, raw)
    if re.match(r"^/[A-Za-z]:", raw):
        raw = raw[1:]
    return Path(raw)


def resolve_source(path: Path) -> Resolution:
    try:
        if not path.exists() or not path.is_file():
            return Resolution(SourceStatus.MISSING_TARGET, None, "source does not exist")
        uri = read_shortcut_uri(path)
    except OSError as error:
        return Resolution(SourceStatus.UNREADABLE, None, str(error))

    if uri:
        parsed = urllib.parse.urlparse(uri)
        if parsed.scheme.lower() != "file":
            return Resolution(
                SourceStatus.UNSUPPORTED_URI,
                None,
                "unsupported URI scheme: %s" % (parsed.scheme or "none"),
                "shortcut",
            )
        try:
            target = uri_to_path(uri)
        except ValueError as error:
            return Resolution(SourceStatus.UNSUPPORTED_URI, None, str(error), "shortcut")
        if not target.exists() or not target.is_file():
            return Resolution(SourceStatus.MISSING_TARGET, None, "shortcut target does not exist", "shortcut")
        try:
            if target.read_bytes()[:4] != b"%PDF":
                return Resolution(SourceStatus.UNREADABLE, None, "shortcut target is not a PDF", "shortcut")
        except OSError as error:
            return Resolution(SourceStatus.UNREADABLE, None, str(error), "shortcut")
        return Resolution(None, target, None, "shortcut")

    try:
        if path.read_bytes()[:4] != b"%PDF":
            return Resolution(SourceStatus.UNREADABLE, None, "source is not a PDF")
    except OSError as error:
        return Resolution(SourceStatus.UNREADABLE, None, str(error))
    return Resolution(None, path, None)


def resolve_pdf(path: Path) -> tuple[Path | None, str]:
    resolution = resolve_source(path)
    if resolution.path is not None:
        return resolution.path, resolution.kind
    return None, resolution.status.value if resolution.status else "unreadable"


def sha1(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_stamp(source: Path, resolved: Path | None) -> str | None:
    stamps: list[str] = []
    seen: set[Path] = set()
    for path in (source, resolved):
        if path is None:
            continue
        canonical = path.resolve()
        if canonical in seen:
            continue
        seen.add(canonical)
        try:
            stat = canonical.stat()
        except OSError:
            return None
        stamps.append("%d:%d" % (stat.st_mtime_ns, stat.st_size))
    return "|".join(stamps)


def pdftotext_pages(pdf: Path) -> tuple[list[str], str | None]:
    out = cache_dir() / "pages" / (sha1(str(pdf)) + ".extract.txt")
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), str(out)],
            capture_output=True,
            text=True,
            timeout=90,
        )
    except FileNotFoundError:
        return [], "pdftotext executable not found"
    except subprocess.TimeoutExpired:
        return [], "pdftotext timed out"
    if result.returncode not in (0, 1) or not out.exists():
        reason = result.stderr.strip() or "pdftotext exited %d" % result.returncode
        return [], reason
    text = out.read_text(encoding="utf-8", errors="replace")
    pages = [page.strip() for page in text.split("\f")]
    while pages and not pages[-1]:
        pages.pop()
    if len(pages) == 1 and len(pages[0]) <= 1:
        pages = []
    return pages, None


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
        pages: dict[int, str] = {}
        index = 1
        while index + 1 < len(chunks):
            try:
                page_number = int(chunks[index])
            except ValueError:
                index += 2
                continue
            pages[page_number] = chunks[index + 1].strip()
            index += 2
        if pages:
            return [pages.get(number, "") for number in range(1, max(pages) + 1)]
    return []


def classify_extraction(
    pages: list[str],
    backend: str | None,
    failure_reason: str | None = None,
    *,
    ocr_pending: bool = False,
) -> ExtractionResult:
    text_pages = sum(bool(page.strip()) for page in pages)
    chars = sum(len(page) for page in pages)
    if failure_reason:
        status = SourceStatus.FAILED
    elif text_pages:
        status = SourceStatus.INDEXED
    elif ocr_pending:
        status = SourceStatus.OCR_PENDING
    else:
        status = SourceStatus.NO_TEXT_LAYER
    return ExtractionResult(status, len(pages), text_pages, chars, backend, failure_reason, tuple(pages))


def extract(vault_pdf: Path, resolution: Resolution | None = None) -> ExtractionResult:
    resolution = resolution or resolve_source(vault_pdf)
    if resolution.status is not None or resolution.path is None:
        status = resolution.status or SourceStatus.UNREADABLE
        return ExtractionResult(status, 0, 0, 0, None, resolution.failure_reason)

    pages, failure = pdftotext_pages(resolution.path)
    if pages:
        return classify_extraction(pages, "pdftotext")
    ocr = ocr_pages_for(rel(vault_pdf))
    if ocr:
        return classify_extraction(ocr, "ocr-cache")
    return classify_extraction([], "pdftotext", failure_reason=failure)


def render_for_ocr(
    vault_pdf: Path,
    *,
    dpi: int = 200,
    run=subprocess.run,
) -> tuple[Path, ...]:
    resolution = resolve_source(vault_pdf)
    stamp = source_stamp(vault_pdf, resolution.path) or str(resolution.path)
    destination = cache_dir() / "ocr" / sha1("%s|dpi=%d" % (stamp, dpi))
    destination.mkdir(parents=True, exist_ok=True)

    def rendered_pages() -> tuple[Path, ...]:
        return tuple(
            sorted(
                destination.glob("page-*.png"),
                key=lambda path: int(path.stem.rsplit("-", 1)[1]),
            )
        )

    pages = rendered_pages()
    if pages:
        return pages

    extraction = extract(vault_pdf, resolution)
    if extraction.status is not SourceStatus.NO_TEXT_LAYER:
        raise ValueError("OCR rendering requires no_text_layer source, got %s" % extraction.status.value)

    prefix = destination / "page"
    try:
        result = run(
            ["pdftoppm", "-png", "-r", str(dpi), str(resolution.path), str(prefix)],
            capture_output=True,
            text=True,
            timeout=180,
        )
    except FileNotFoundError as error:
        raise RuntimeError("pdftoppm executable not found") from error
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "pdftoppm exited %d" % result.returncode)
    pages = rendered_pages()
    if not pages:
        raise RuntimeError("pdftoppm produced no page images")
    return pages


def build_manifest_record(
    source: Path,
    resolution: Resolution,
    extraction: ExtractionResult | None,
) -> dict[str, object]:
    extraction = extraction or ExtractionResult(
        resolution.status or SourceStatus.UNREADABLE,
        0,
        0,
        0,
        None,
        resolution.failure_reason,
    )
    resolved = resolution.path
    try:
        content_hash = file_hash(resolved) if resolved is not None else None
    except OSError:
        content_hash = None
    return {
        "path": rel(source),
        "kind": resolution.kind,
        "source": extraction.backend or resolution.kind,
        "resolved_path": str(resolved) if resolved is not None else None,
        "status": extraction.status.value,
        "pages": extraction.pages,
        "text_pages": extraction.text_pages,
        "chars": extraction.chars,
        "content_hash": content_hash,
        "extraction_backend": extraction.backend,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "source_stamp": source_stamp(source, resolved),
        "failure_reason": extraction.failure_reason,
    }


def store_pages(vault_rel: str, pages: tuple[str, ...] | list[str]) -> Path:
    destination = cache_dir() / "pages" / (sha1(vault_rel) + ".txt")
    parts = ["===== PAGE %d =====\n%s" % (number, page) for number, page in enumerate(pages, 1)]
    destination.write_text("\n\n".join(parts), encoding="utf-8")
    return destination


def iter_pdfs(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in {".git", ".obsidian", ".pi", ".trash", "Bin"}]
        for name in filenames:
            if name.lower().endswith(".pdf"):
                yield Path(dirpath) / name


def cmd_index(root: Path, limit: int | None) -> None:
    root = root.resolve()
    manifest_path = cache_dir() / "manifest.jsonl"
    seen: dict[str, dict[str, object]] = {}
    if manifest_path.exists():
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            key = canonical_manifest_path(str(record["path"]))
            record["path"] = key
            seen[key] = record

    indexed = 0
    updated = 0
    for pdf in iter_pdfs(root):
        vault_rel = rel(pdf)
        resolution = resolve_source(pdf)
        stamp = source_stamp(pdf, resolution.path)
        previous = seen.get(vault_rel)
        if previous and MANIFEST_FIELDS <= set(previous) and previous.get("source_stamp") == stamp:
            indexed += 1
            if limit and indexed >= limit:
                break
            continue
        extraction = extract(pdf, resolution)
        if extraction.status == SourceStatus.INDEXED:
            store_pages(vault_rel, extraction.page_text)
        record = build_manifest_record(pdf, resolution, extraction)
        seen[vault_rel] = record
        updated += 1
        indexed += 1
        print("%s\t%s\t%d pages\t%s" % (record["status"], vault_rel, extraction.pages, resolution.kind))
        if limit and indexed >= limit:
            break

    with manifest_path.open("w", encoding="utf-8") as output:
        for record in sorted(seen.values(), key=lambda value: str(value["path"])):
            output.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    print("# indexed %d files, wrote %d, manifest %d" % (indexed, updated, len(seen)), file=sys.stderr)


def snippet(text: str, query: str, width: int = 180) -> str:
    lower = text.lower()
    query_lower = query.lower()
    position = lower.find(query_lower)
    if position < 0:
        return " ".join(text.split())[:width]
    start = max(0, position - 60)
    end = min(len(text), position + len(query) + 120)
    value = " ".join(text[start:end].split())
    return ("…" if start else "") + value + ("…" if end < len(text) else "")


def cmd_search(query: str, path_filter: str | None, limit: int) -> None:
    manifest_path = cache_dir() / "manifest.jsonl"
    if not manifest_path.exists():
        print("No index yet. Run: python index.py index", file=sys.stderr)
        raise SystemExit(1)
    query_lower = query.lower()
    hits = []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record.get("status") != SourceStatus.INDEXED.value:
            continue
        if path_filter and path_filter.lower() not in str(record["path"]).lower():
            continue
        page_file = cache_dir() / "pages" / (sha1(str(record["path"])) + ".txt")
        if not page_file.exists():
            continue
        body = page_file.read_text(encoding="utf-8", errors="replace")
        current_page = 1
        buffer = []
        for raw in body.splitlines():
            match = re.match(r"===== PAGE (\d+) =====", raw)
            if match:
                if buffer:
                    text = "\n".join(buffer)
                    if query_lower in text.lower():
                        hits.append((record["path"], current_page, snippet(text, query)))
                current_page = int(match.group(1))
                buffer = []
                continue
            buffer.append(raw)
        if buffer:
            text = "\n".join(buffer)
            if query_lower in text.lower():
                hits.append((record["path"], current_page, snippet(text, query)))
        if len(hits) >= limit * 4:
            break
    for path, page, text in hits[:limit]:
        name = Path(str(path)).name
        citation = "[[%s#page=%d|%s, p.%d]]" % (name, page, Path(name).stem, page)
        print("%s\tp.%d\t%s\t%s" % (path, page, citation, text))
    print("# %d hit(s)" % min(len(hits), limit), file=sys.stderr)


def cmd_resolve(target: str) -> None:
    path = Path(target)
    if not path.is_absolute():
        path = VAULT / target
    resolution = resolve_source(path)
    print("kind\t%s" % resolution.kind)
    print("status\t%s" % (resolution.status.value if resolution.status else "resolved"))
    print("vault\t%s" % rel(path))
    print("real\t%s" % (resolution.path or ""))


def cmd_pages(target: str) -> None:
    path = Path(target)
    if not path.is_absolute():
        path = VAULT / target
    result = extract(path)
    print("# %s status=%s source=%s pages=%d" % (rel(path), result.status.value, result.backend, result.pages))
    for number, page in enumerate(result.page_text, 1):
        print("===== PAGE %d =====" % number)
        print(page)
        print()


def cmd_ocr_pages(target: str, dpi: int) -> None:
    path = Path(target)
    if not path.is_absolute():
        path = VAULT / target
    pages = render_for_ocr(path, dpi=dpi)
    result = {
        "source": rel(path),
        "dpi": dpi,
        "page_images": [str(page) for page in pages],
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


def cmd_doctor(manifest_path: Path | None = None) -> int:
    manifest_path = manifest_path or (cache_dir() / "manifest.jsonl")
    if not manifest_path.exists():
        print(json.dumps({"blocking": 1, "error": "manifest_missing", "path": str(manifest_path)}, sort_keys=True))
        return 1

    counts: Counter[str] = Counter()
    blockers = []
    legacy = []
    for line_number, line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            legacy.append({"line": line_number, "reason": str(error)})
            continue
        missing = sorted(MANIFEST_FIELDS - set(record))
        if missing:
            legacy.append({"path": record.get("path"), "missing": missing})
            continue
        status = str(record["status"])
        counts[status] += 1
        if status in {
            SourceStatus.MISSING_TARGET.value,
            SourceStatus.UNSUPPORTED_URI.value,
            SourceStatus.UNREADABLE.value,
            SourceStatus.FAILED.value,
        }:
            blockers.append({"path": record["path"], "status": status, "reason": record.get("failure_reason")})

    result = {
        "blocking": len(blockers) + len(legacy),
        "blockers": blockers,
        "counts": dict(sorted(counts.items())),
        "legacy": legacy,
        "manifest": str(manifest_path),
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 1 if result["blocking"] else 0


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        raise SystemExit(2)
    command = args[0]
    if command == "index":
        root = VAULT
        limit = None
        if "--root" in args:
            root = Path(args[args.index("--root") + 1])
        if "--limit" in args:
            limit = int(args[args.index("--limit") + 1])
        cmd_index(root, limit)
    elif command == "search" and len(args) >= 2:
        path_filter = None
        limit = 20
        rest = args[1:]
        if "--path" in rest:
            position = rest.index("--path")
            path_filter = rest[position + 1]
            rest = rest[:position] + rest[position + 2 :]
        if "--n" in rest:
            position = rest.index("--n")
            limit = int(rest[position + 1])
            rest = rest[:position] + rest[position + 2 :]
        cmd_search(" ".join(rest), path_filter, limit)
    elif command == "resolve" and len(args) == 2:
        cmd_resolve(args[1])
    elif command == "pages" and len(args) == 2:
        cmd_pages(args[1])
    elif command == "ocr-pages" and len(args) >= 2:
        dpi = 200
        if "--dpi" in args:
            dpi = int(args[args.index("--dpi") + 1])
        cmd_ocr_pages(args[1], dpi)
    elif command == "doctor":
        manifest = None
        if "--manifest" in args:
            manifest = Path(args[args.index("--manifest") + 1])
        raise SystemExit(cmd_doctor(manifest))
    else:
        print(__doc__)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
