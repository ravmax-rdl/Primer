from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "vault" / ".pi" / "skills" / "academic-workflow" / "learning_state.py"
SPEC = importlib.util.spec_from_file_location("learning_state_contract", SCRIPT)
assert SPEC and SPEC.loader
state = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(state)


class LearningStateTests(unittest.TestCase):
    def session(self) -> dict[str, object]:
        return {
            "record_type": "study_session",
            "session_id": "session-1",
            "started_at": "2026-08-20T10:00:00+00:00",
            "course_id": "COURSE101",
            "planned_minutes": 45,
            "target_note": "Courses/COURSE101/Topic.md",
            "concept_ids": ["concept-a"],
            "source_refs": ["[[Source.pdf#page=1]]"],
            "next_action": "Attempt one transfer problem.",
        }

    def attempt(self) -> dict[str, object]:
        return {
            "record_type": "assessment_attempt",
            "attempt_id": "attempt-1",
            "question_id": "COURSE101-2025-P1-Q01",
            "attempted_at": "2026-08-20T10:20:00+00:00",
            "course_id": "COURSE101",
            "concept_ids": ["concept-a"],
            "marks_awarded": 2,
            "marks_available": 5,
            "time_seconds": 480,
            "confidence_before": 0.8,
            "grading_source": "[[Rubric.pdf#page=1]]",
            "grading_confidence": 1.0,
            "error_types": ["concept"],
            "feedback": "The response omitted the required condition.",
            "card_action": "create",
        }

    def test_vocabularies_are_exact(self) -> None:
        self.assertEqual(
            state.ERROR_TYPES,
            frozenset({"recall", "concept", "translation", "procedure", "calculation", "misread", "incomplete-justification", "time-management"}),
        )
        self.assertEqual(state.CARD_ACTIONS, frozenset({"create", "revise", "suspend", "none"}))

    def test_stable_id_ignores_key_order(self) -> None:
        self.assertEqual(state.stable_id("attempt", {"a": 1, "b": 2}), state.stable_id("attempt", {"b": 2, "a": 1}))

    def test_valid_records_pass(self) -> None:
        self.assertEqual(state.validate_record(self.session()), [])
        self.assertEqual(state.validate_record(self.attempt()), [])

    def test_unknown_error_and_missing_feedback_fail(self) -> None:
        record = self.attempt()
        record["error_types"] = ["careless"]
        record["feedback"] = ""
        errors = state.validate_record(record)
        self.assertTrue(any("careless" in error for error in errors))
        self.assertTrue(any("feedback" in error for error in errors))

    def test_append_round_trip_and_invalid_write_safety(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            note = Path(tmp) / "note.md"
            note.write_text("# Topic\n", encoding="utf-8")
            self.assertEqual(state.append_record(note, self.session()), "session-1")
            self.assertEqual(state.load_records(note), [self.session()])
            before = note.read_text(encoding="utf-8")
            invalid = self.attempt()
            invalid["error_types"] = ["careless"]
            with self.assertRaises(ValueError):
                state.append_record(note, invalid)
            self.assertEqual(note.read_text(encoding="utf-8"), before)

    def test_latest_concept_uses_record_time(self) -> None:
        self.assertEqual(state.latest_for_concept([self.attempt(), self.session()], "concept-a"), self.attempt())

    def test_card_action_rules(self) -> None:
        base = dict(error_types={"recall"}, passed=False, has_related_card=False, repeated_failure=False, misleading_card=False)
        self.assertEqual(state.decide_card_action(**base), "create")
        self.assertEqual(state.decide_card_action(**(base | {"has_related_card": True})), "revise")
        self.assertEqual(state.decide_card_action(**(base | {"misleading_card": True})), "suspend")
        self.assertEqual(state.decide_card_action(**(base | {"passed": True})), "none")
        self.assertEqual(state.decide_card_action(**(base | {"error_types": {"procedure"}})), "none")


if __name__ == "__main__":
    unittest.main()
