from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "vault" / ".pi" / "skills" / "pdf-search" / "index.py"
SPEC = importlib.util.spec_from_file_location("pdf_index_contract", SCRIPT)
assert SPEC and SPEC.loader
index = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(index)


class PdfStatusTests(unittest.TestCase):
    def test_uri_to_path_decodes_windows_file_uri(self) -> None:
        path = index.uri_to_path("file:///C:/Course/My%20Paper.pdf")
        self.assertEqual(str(path).replace("\\", "/"), "C:/Course/My Paper.pdf")

    def test_manifest_paths_are_canonical(self) -> None:
        self.assertEqual(index.canonical_manifest_path(r"Papers\paper.pdf"), "Papers/paper.pdf")

    def test_source_stamp_ignores_relative_path_spelling(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "paper.pdf"
            source.write_bytes(b"%PDF" + b"x" * 256)
            self.assertEqual(index.source_stamp(source, source), index.source_stamp(source.resolve(), source.resolve()))

    def test_missing_shortcut_target_is_not_ocr_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            shortcut = Path(tmp) / "paper.pdf"
            shortcut.write_text("file:///Z:/missing/paper.pdf\n", encoding="utf-8")
            result = index.resolve_source(shortcut)
        self.assertEqual(result.status, index.SourceStatus.MISSING_TARGET)
        self.assertIsNone(result.path)

    def test_non_file_uri_is_unsupported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            shortcut = Path(tmp) / "paper.pdf"
            shortcut.write_text("https://example.test/paper.pdf\n", encoding="utf-8")
            result = index.resolve_source(shortcut)
        self.assertEqual(result.status, index.SourceStatus.UNSUPPORTED_URI)

    def test_empty_extraction_is_no_text_not_failed(self) -> None:
        result = index.classify_extraction([], "pdftotext")
        self.assertEqual(result.status, index.SourceStatus.NO_TEXT_LAYER)
        self.assertIsNone(result.failure_reason)

    def test_backend_error_is_failed(self) -> None:
        result = index.classify_extraction([], "pdftotext", failure_reason="timeout")
        self.assertEqual(result.status, index.SourceStatus.FAILED)

    def test_manifest_record_contains_complete_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "paper.pdf"
            source.write_bytes(b"%PDF" + b"x" * 256)
            record = index.build_manifest_record(
                source,
                index.Resolution(None, source, None),
                index.classify_extraction(["first page", ""], "pdftotext"),
            )
        self.assertEqual(
            set(record),
            {
                "path", "kind", "source", "resolved_path", "status", "pages",
                "text_pages", "chars", "content_hash", "extraction_backend",
                "extracted_at", "source_stamp", "failure_reason",
            },
        )
        self.assertEqual(record["status"], "indexed")

    def test_doctor_rejects_legacy_manifest_without_rewriting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "manifest.jsonl"
            original = json.dumps({"path": "paper.pdf", "pages": 0}) + "\n"
            manifest.write_text(original, encoding="utf-8")
            self.assertNotEqual(index.cmd_doctor(manifest), 0)
            self.assertEqual(manifest.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
