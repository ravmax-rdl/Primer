from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
VAULT = ROOT / "vault"
PROMPTS = VAULT / ".pi" / "prompts"
REFERENCES = VAULT / ".pi" / "skills" / "academic-workflow" / "references"
VISIBLE = {"study.md", "capture.md", "research.md", "exam.md", "doctor.md"}
SPECIALIST = {
    "lecture-video.md", "lecture.md", "probe.md", "teach.md", "classify.md",
    "overview.md", "mock.md", "postmortem.md", "weakspots.md", "review.md",
    "cards.md", "cram.md", "cite.md", "gap.md", "exercises.md", "feynman.md",
    "paper.md", "worked.md", "source.md", "find.md", "synth.md", "summary.md",
    "predict.md", "paper-review.md", "crosswalk.md",
}


def body(name: str) -> str:
    return (PROMPTS / name).read_text(encoding="utf-8")


class WorkflowPromptTests(unittest.TestCase):
    def test_only_five_prompts_are_discoverable(self) -> None:
        self.assertEqual({path.name for path in PROMPTS.glob("*.md")}, VISIBLE)

    def test_all_specialist_references_are_internal(self) -> None:
        self.assertEqual({path.name for path in REFERENCES.glob("*.md")}, SPECIALIST)

    def test_visible_prompts_have_front_matter(self) -> None:
        for name in VISIBLE:
            text = body(name)
            self.assertTrue(text.startswith("---\n"), name)
            front_matter = text.split("---", 2)[1]
            self.assertRegex(front_matter, r"(?m)^description:\s*\S")
            self.assertRegex(front_matter, r"(?m)^argument-hint:\s*.*$")

    def test_study_uses_evidence_closed_loop(self) -> None:
        text = body("study.md")
        for token in ("probe.md", "teach.md", "exercises.md", "postmortem.md", "cards.md"):
            self.assertIn(token, text)
        self.assertIn("learning_state.py validate", text)
        self.assertIn("learning_state.py append", text)
        self.assertLess(text.index("learning_state.py validate"), text.index("learning_state.py append"))

    def test_exam_uses_exact_taxonomy_and_card_decision(self) -> None:
        text = body("exam.md")
        self.assertIn("learning_state.py decide-card", text)
        for label in ("recall", "concept", "translation", "procedure", "calculation", "misread", "incomplete-justification", "time-management"):
            self.assertIn(label, text)

    def test_doctor_is_read_only(self) -> None:
        text = body("doctor.md")
        self.assertIn("pdf-search/index.py doctor", text)
        self.assertRegex(text.lower(), r"do not (write|modify|repair)")

    def test_past_paper_ocr_writes_year_scoped_answer_script_notes(self) -> None:
        pdf_search = (VAULT / ".pi" / "skills" / "pdf-search" / "SKILL.md").read_text(encoding="utf-8")
        past_papers = (VAULT / ".pi" / "skills" / "past-papers" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("ocr-pages", pdf_search)
        self.assertIn("resolved target", pdf_search.lower())
        self.assertIn("Papers & Reviews/Programme/Y01_S01/Answer Scripts/<year>/", past_papers)
        self.assertIn("question-paper", past_papers)
        self.assertIn("resolved-pdf-raster", past_papers)
        self.assertTrue(
            (VAULT / "Papers & Reviews" / "Programme" / "Y01_S01" / "Answer Scripts").is_dir()
        )

    def test_visible_prompts_do_not_call_removed_commands(self) -> None:
        stems = (re.escape(Path(name).stem) for name in SPECIALIST)
        removed = re.compile(r"(?<![\w.-])/(?:" + "|".join(stems) + r")(?![\w.-])")
        for name in VISIBLE:
            self.assertIsNone(removed.search(body(name)), name)


if __name__ == "__main__":
    unittest.main()
