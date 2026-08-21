import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.verify import verify_repository


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
PI = VAULT / ".pi"


def run_python(script: Path, *arguments: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command_env = os.environ.copy()
    if env:
        command_env.update(env)
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        cwd=VAULT,
        env=command_env,
        capture_output=True,
        text=True,
        check=False,
    )


class RuntimeScriptTests(unittest.TestCase):
    def test_new_card_schedule_has_valid_initial_state(self) -> None:
        result = run_python(PI / "skills/spaced-repetition/sm2.py", "new")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"due: \d{4}-\d{2}-\d{2}\n")
        self.assertIn("interval: 0\n", result.stdout)
        self.assertIn("ease: 2.5\n", result.stdout)
        self.assertIn("reps: 0\n", result.stdout)
        self.assertIn("lapses: 0\n", result.stdout)

    def test_crosswalk_maps_known_code_and_blocks_unmapped_course(self) -> None:
        script = PI / "skills/past-papers/lookup.py"
        environment = {"VAULT_ROOT": str(VAULT)}

        mapped = run_python(script, "LEGACY102", env=environment)
        blocked = run_python(script, "LEGACY999", env=environment)

        self.assertEqual(mapped.returncode, 0, mapped.stderr)
        self.assertIn("current\tCOURSE102", mapped.stdout)
        self.assertNotIn("BLOCK", mapped.stdout)
        self.assertEqual(blocked.returncode, 0, blocked.stderr)
        self.assertIn("BLOCK\tno current equivalent", blocked.stdout)

    def test_canvas_layout_places_dependencies_left_to_right(self) -> None:
        graph = {
            "nodes": [
                {"id": "proposition", "label": "Proposition", "deps": []},
                {"id": "implication", "label": "Implication", "deps": ["proposition"]},
            ],
            "edges": [{"from": "proposition", "to": "implication"}],
        }
        with tempfile.TemporaryDirectory() as directory:
            graph_path = Path(directory) / "graph.json"
            graph_path.write_text(json.dumps(graph), encoding="utf-8")

            result = run_python(PI / "skills/canvas-gen/layout.py", str(graph_path))

        self.assertEqual(result.returncode, 0, result.stderr)
        placed = json.loads(result.stdout)
        nodes = {node["id"]: node for node in placed["nodes"]}
        self.assertLess(nodes["proposition"]["x"], nodes["implication"]["x"])

    def test_public_runtime_has_no_personal_absolute_paths(self) -> None:
        errors = verify_repository(ROOT)

        personal_path_errors = [
            error for error in errors if error.startswith("Personal or external absolute path:")
        ]
        self.assertEqual(personal_path_errors, [])


class DemoVaultTests(unittest.TestCase):
    def test_demo_course_and_cards_form_a_complete_learning_path(self) -> None:
        course_index = VAULT / "Study Notes/Programme/TERM_01/Foundations of Logic/Foundations of Logic.md"
        lecture_base = VAULT / "Study Notes/Programme/TERM_01/Foundations of Logic/Lecture Notes.base"
        day_note = VAULT / "Study Notes/Programme/TERM_01/W01/D01/Foundations of Logic.md"
        cards = (
            VAULT / "Study Notes/Review/Foundations of Logic/Implication.md",
            VAULT / "Study Notes/Review/Foundations of Logic/Contrapositive.md",
        )

        self.assertTrue(course_index.is_file())
        self.assertTrue(lecture_base.is_file())
        self.assertTrue(day_note.is_file())
        base_text = lecture_base.read_text(encoding="utf-8")
        self.assertIn('file.name == "Foundations of Logic"', base_text)

        for card in cards:
            self.assertTrue(card.is_file(), card)
            text = card.read_text(encoding="utf-8")
            self.assertRegex(text, r"due: \d{4}-\d{2}-\d{2}")
            self.assertRegex(text, r"interval: \d+")
            self.assertRegex(text, r"ease: \d+(?:\.\d+)?")
            self.assertRegex(text, r"reps: \d+")
            self.assertRegex(text, r"lapses: \d+")
            self.assertIn("[[Study Notes/Programme/TERM_01/W01/D01/Foundations of Logic]]", text)

        day_text = day_note.read_text(encoding="utf-8")
        self.assertIn("## Understanding map", day_text)
        self.assertIn("```mermaid", day_text)
        self.assertIn("status: demo", day_text)


if __name__ == "__main__":
    unittest.main()
