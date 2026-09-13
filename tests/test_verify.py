import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify import verify_repository


REQUIRED_FILES = ("README.md", "LICENSE", "LICENSE-CODE",
"LICENSE-CONTENT",
"CONTRIBUTING.md",
"CHANGELOG.md",
"docs/setup.md",
"docs/workflows.md",
"docs/customization.md",
"docs/troubleshooting.md",
"vault/START HERE.md",
"vault/.pi/settings.json",
"vault/.pi/APPEND_SYSTEM.md",
"vault/.pi/LEARNER.md",
"vault/.obsidian/app.json",)

VISIBLE_PROMPTS = {"study.md", "capture.md", "research.md", "exam.md", "doctor.md"}
SPECIALIST_REFERENCES = {
    "lecture-video.md", "lecture.md", "probe.md", "teach.md", "classify.md",
    "overview.md", "mock.md", "postmortem.md", "weakspots.md", "review.md",
    "cards.md", "cram.md", "cite.md", "gap.md", "exercises.md", "feynman.md",
    "paper.md", "worked.md", "source.md", "find.md", "synth.md", "summary.md",
    "predict.md", "paper-review.md", "crosswalk.md",
}


class VerifyRepositoryTests(unittest.TestCase):
    def make_repository(self, root: Path) -> None:
        for relative_path in REQUIRED_FILES:
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".json":
                path.write_text(json.dumps({"safe": True}), encoding="utf-8")
            elif path.suffix == ".svg":
                path.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")
            else:
                path.write_text("# Safe fixture\n", encoding="utf-8")
        prompts = root / "vault/.pi/prompts"
        references = root / "vault/.pi/skills/academic-workflow/references"
        prompts.mkdir(parents=True, exist_ok=True)
        references.mkdir(parents=True, exist_ok=True)
        for name in VISIBLE_PROMPTS:
            (prompts / name).write_text("---\ndescription: safe\nargument-hint: ''\n---\n", encoding="utf-8")
        for name in SPECIALIST_REFERENCES:
            (references / name).write_text("# Internal reference\n", encoding="utf-8")
        for relative_path in (
            "vault/.pi/skills/academic-workflow/learning_state.py",
            "vault/.pi/skills/pdf-search/index.py",
        ):
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# safe runtime\n", encoding="utf-8")

    def test_accepts_complete_safe_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            self.assertEqual(verify_repository(root), [])

    def test_reports_missing_required_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            (root / "vault/START HERE.md").unlink()
            self.assertIn("Missing required file: vault/START HERE.md", verify_repository(root))

    def test_rejects_generated_runtime_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            cache = root / "vault/.pi/cache/index.json"
            cache.parent.mkdir(parents=True)
            cache.write_text("{}", encoding="utf-8")
            workspace = root / "vault/.obsidian/workspace.json"
            workspace.write_text("{}", encoding="utf-8")
            errors = verify_repository(root)
            self.assertIn("Forbidden generated file: vault/.pi/cache/index.json", errors)
            self.assertIn("Forbidden generated file: vault/.obsidian/workspace.json", errors)

    def test_rejects_secret_like_filename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            secret = root / "vault/notes/github-recovery-codes.txt"
            secret.parent.mkdir(parents=True)
            secret.write_text("fixture", encoding="utf-8")
            self.assertIn(
                "Sensitive filename: vault/notes/github-recovery-codes.txt",
                verify_repository(root),
            )

    def test_rejects_personal_absolute_paths_and_file_uris(self) -> None:
        examples = (
            "C:/Users/alex/Documents/Vault",
            r"C:\Users\alex\Documents\Vault",
            "/Users/alex/Documents/Vault",
            "/home/alex/Vault",
            "file:///F:/Text Books/course.pdf",
        )
        for value in examples:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.make_repository(root)
                (root / "vault/README.md").write_text(value, encoding="utf-8")
                errors = verify_repository(root)
                self.assertTrue(
                    any(error.startswith("Personal or external absolute path:") for error in errors),
                    errors,
                )

    def test_does_not_treat_detector_source_as_a_leaked_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            detector = root / "scripts/detector.py"
            detector.parent.mkdir(parents=True)
            detector.write_text('PATTERN = r"file:///|/Users/[^/]+/"\n', encoding="utf-8")
            self.assertEqual(verify_repository(root), [])

    def test_reports_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            (root / "vault/.obsidian/app.json").write_text("{", encoding="utf-8")
            errors = verify_repository(root)
            self.assertTrue(any(error.startswith("Invalid JSON: vault/.obsidian/app.json") for error in errors))

    def test_reports_broken_relative_markdown_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            (root / "README.md").write_text("[Setup](docs/missing.md)\n", encoding="utf-8")
            self.assertIn("Broken link in README.md: docs/missing.md", verify_repository(root))


    def test_rejects_extra_visible_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            (root / "vault/.pi/prompts/teach.md").write_text("# stale command\n", encoding="utf-8")
            self.assertIn("Unexpected visible prompt: teach.md", verify_repository(root))

    def test_rejects_missing_internal_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            (root / "vault/.pi/skills/academic-workflow/references/probe.md").unlink()
            self.assertIn("Missing academic workflow reference: probe.md", verify_repository(root))

    def test_rejects_private_template_values_in_vault(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repository(root)
            (root / "vault/START HERE.md").write_text("UCSC BSc Discrete Mathematics\n", encoding="utf-8")
            errors = verify_repository(root)
            self.assertTrue(any(error.startswith("Private template value:") for error in errors))


if __name__ == "__main__":
    unittest.main()
