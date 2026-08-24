from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from collections.abc import Iterator
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "vault" / ".pi" / "skills" / "pdf-search" / "index.py"
SPEC = importlib.util.spec_from_file_location("pdf_index_contract", SCRIPT)
assert SPEC and SPEC.loader
index = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(index)


@contextlib.contextmanager
def ocr_fixture(pages: list[str] | None = None) -> Iterator[tuple[Path, Path, Path]]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        real_pdf = root / "real paper.pdf"
        real_pdf.write_bytes(b"%PDF" + b"x" * 256)
        shortcut = root / "paper.pdf"
        shortcut.write_text(real_pdf.as_uri(), encoding="utf-8")
        original_cache = index.CACHE
        original_extract = index.extract
        try:
            index.CACHE = root / "cache"
            index.extract = lambda *_args, **_kwargs: index.classify_extraction(
                pages or [],
                "pdftotext",
            )
            yield root, real_pdf, shortcut
        finally:
            index.CACHE = original_cache
            index.extract = original_extract


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

    def test_render_for_ocr_uses_resolved_pdf_and_orders_page_images(self) -> None:
        commands: list[list[str]] = []

        def fake_run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            commands.append(command)
            Path(command[-1] + "-10.png").write_bytes(b"page 10")
            Path(command[-1] + "-2.png").write_bytes(b"page 2")
            return subprocess.CompletedProcess(command, 0, "", "")

        with ocr_fixture() as (_root, real_pdf, shortcut):
            result = index.render_for_ocr(shortcut, run=fake_run)

        self.assertEqual([path.name for path in result], ["page-2.png", "page-10.png"])
        self.assertEqual(Path(commands[0][-2]), real_pdf)

    def test_render_for_ocr_rejects_searchable_sources(self) -> None:
        def unexpected_run(*_args: object, **_kwargs: object) -> None:
            raise AssertionError("renderer must not run")

        with ocr_fixture(["searchable text"]) as (_root, _real_pdf, shortcut):
            with self.assertRaisesRegex(ValueError, "requires no_text_layer"):
                index.render_for_ocr(shortcut, run=unexpected_run)

    def test_render_for_ocr_reuses_cached_images(self) -> None:
        calls = 0

        def fake_run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            nonlocal calls
            calls += 1
            Path(command[-1] + "-1.png").write_bytes(b"page")
            return subprocess.CompletedProcess(command, 0, "", "")

        with ocr_fixture() as (_root, _real_pdf, shortcut):
            first = index.render_for_ocr(shortcut, run=fake_run)
            second = index.render_for_ocr(shortcut, run=fake_run)

        self.assertEqual(first, second)
        self.assertEqual(calls, 1)

    def test_render_for_ocr_caches_each_dpi_separately(self) -> None:
        calls: list[str] = []

        def fake_run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            calls.append(command[3])
            Path(command[-1] + "-1.png").write_bytes(b"page")
            return subprocess.CompletedProcess(command, 0, "", "")

        with ocr_fixture() as (_root, _real_pdf, shortcut):
            first = index.render_for_ocr(shortcut, dpi=180, run=fake_run)
            second = index.render_for_ocr(shortcut, dpi=300, run=fake_run)

        self.assertNotEqual(first, second)
        self.assertEqual(calls, ["180", "300"])

    def test_render_for_ocr_does_not_reuse_partial_cache(self) -> None:
        calls = 0

        def flaky_run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            nonlocal calls
            calls += 1
            Path(command[-1] + "-1.png").write_bytes(b"page 1")
            if calls == 1:
                return subprocess.CompletedProcess(command, 2, "", "interrupted")
            Path(command[-1] + "-2.png").write_bytes(b"page 2")
            return subprocess.CompletedProcess(command, 0, "", "")

        with ocr_fixture() as (_root, _real_pdf, shortcut):
            with self.assertRaisesRegex(RuntimeError, "interrupted"):
                index.render_for_ocr(shortcut, run=flaky_run)
            pages = index.render_for_ocr(shortcut, run=flaky_run)

        self.assertEqual(calls, 2)
        self.assertEqual([path.name for path in pages], ["page-1.png", "page-2.png"])

    def test_render_for_ocr_reports_timeout_and_removes_partial_pages(self) -> None:
        def timed_out_run(command: list[str], **_kwargs: object) -> None:
            Path(command[-1] + "-1.png").write_bytes(b"partial")
            raise subprocess.TimeoutExpired(command, 180)

        with ocr_fixture() as (root, _real_pdf, shortcut):
            with self.assertRaisesRegex(RuntimeError, "pdftoppm timed out"):
                index.render_for_ocr(shortcut, run=timed_out_run)
            self.assertEqual(list((root / "cache" / "ocr").rglob("page-*.png")), [])

    def test_render_for_ocr_includes_extraction_failure_reason(self) -> None:
        with ocr_fixture() as (_root, _real_pdf, shortcut):
            index.extract = lambda *_args, **_kwargs: index.classify_extraction(
                [],
                "pdftotext",
                failure_reason="pdftotext executable not found",
            )
            with self.assertRaisesRegex(ValueError, "pdftotext executable not found"):
                index.render_for_ocr(shortcut)

    def test_render_for_ocr_prunes_superseded_source_stamp(self) -> None:
        def fake_run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            Path(command[-1] + "-1.png").write_bytes(b"page")
            return subprocess.CompletedProcess(command, 0, "", "")

        with ocr_fixture() as (_root, real_pdf, shortcut):
            first = index.render_for_ocr(shortcut, run=fake_run)
            real_pdf.write_bytes(b"%PDF" + b"updated" * 128)
            second = index.render_for_ocr(shortcut, run=fake_run)
            self.assertNotEqual(first, second)
            self.assertFalse(first[0].parent.exists())

    def test_render_for_ocr_reports_renderer_failure(self) -> None:
        def failed_run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(command, 2, "", "renderer failed")

        with ocr_fixture() as (_root, _real_pdf, shortcut):
            with self.assertRaisesRegex(RuntimeError, "renderer failed"):
                index.render_for_ocr(shortcut, run=failed_run)

    def test_render_for_ocr_rejects_empty_renderer_output(self) -> None:
        def empty_run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(command, 0, "", "")

        with ocr_fixture() as (_root, _real_pdf, shortcut):
            with self.assertRaisesRegex(RuntimeError, "no page images"):
                index.render_for_ocr(shortcut, run=empty_run)

    def test_render_for_ocr_reports_missing_renderer(self) -> None:
        def missing_run(*_args: object, **_kwargs: object) -> None:
            raise FileNotFoundError

        with ocr_fixture() as (_root, _real_pdf, shortcut):
            with self.assertRaisesRegex(RuntimeError, "pdftoppm executable not found"):
                index.render_for_ocr(shortcut, run=missing_run)

    def test_cmd_ocr_pages_emits_machine_readable_page_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "paper.pdf"
            source.write_bytes(b"%PDF" + b"x" * 256)
            page = root / "page-1.png"
            page.write_bytes(b"page")
            output = io.StringIO()
            original_vault = index.VAULT
            original_render = index.render_for_ocr
            try:
                index.VAULT = root
                index.render_for_ocr = lambda *_args, **_kwargs: (page,)
                with contextlib.redirect_stdout(output):
                    index.cmd_ocr_pages("paper.pdf", 240)
            finally:
                index.VAULT = original_vault
                index.render_for_ocr = original_render

        result = json.loads(output.getvalue())
        self.assertEqual(result["source"], "paper.pdf")
        self.assertEqual(result["dpi"], 240)
        self.assertEqual(result["page_images"], [str(page)])

    def test_main_routes_ocr_pages_with_flag_before_target(self) -> None:
        calls: list[tuple[str, int]] = []
        original_argv = index.sys.argv
        original_command = index.cmd_ocr_pages
        try:
            index.sys.argv = ["index.py", "ocr-pages", "--dpi", "240", "paper.pdf"]
            index.cmd_ocr_pages = lambda target, dpi: calls.append((target, dpi))
            index.main()
        finally:
            index.sys.argv = original_argv
            index.cmd_ocr_pages = original_command

        self.assertEqual(calls, [("paper.pdf", 240)])

    def test_doctor_rejects_legacy_manifest_without_rewriting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "manifest.jsonl"
            original = json.dumps({"path": "paper.pdf", "pages": 0}) + "\n"
            manifest.write_text(original, encoding="utf-8")
            self.assertNotEqual(index.cmd_doctor(manifest), 0)
            self.assertEqual(manifest.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
