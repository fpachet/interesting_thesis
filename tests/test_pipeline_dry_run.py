from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from interesting_thesis.cli import main
from interesting_thesis.config import DEFAULT_THEME


class DryRunPipelineTests(unittest.TestCase):
    def test_pipeline_generates_outputs(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        prompts_dir = project_root / "prompts"
        roles_file = project_root / "config" / "default_roles.json"

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            input_dir = tmp_path / "input"
            output_dir = tmp_path / "output"
            memory_file = tmp_path / "memory" / "state.json"
            input_dir.mkdir(parents=True, exist_ok=True)
            (input_dir / "notes.md").write_text(
                "# Notes\n\n"
                "L'objet interessant n'est pas seulement rare. "
                "Il apparait comme solution stable quand un echantillonnage est contraint "
                "par des budgets d'attention, de temps ou de calcul.\n\n"
                "La these doit distinguer l'interessant du simplement nouveau.",
                encoding="utf-8",
            )

            exit_code = main(
                [
                    "--dry-run",
                    "--rounds",
                    "2",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(output_dir),
                    "--memory-file",
                    str(memory_file),
                    "--prompts-dir",
                    str(prompts_dir),
                    "--roles-file",
                    str(roles_file),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((output_dir / "corpus_digest.md").exists())
            self.assertTrue((output_dir / "round_01.md").exists())
            self.assertTrue((output_dir / "round_02.md").exists())
            self.assertTrue((output_dir / "final_synthesis.md").exists())
            self.assertTrue((output_dir / "thesis_paragraphs.md").exists())
            self.assertTrue(memory_file.exists())

            payload = json.loads(memory_file.read_text(encoding="utf-8"))
            self.assertEqual(payload["theme"], DEFAULT_THEME)
            self.assertEqual(len(payload["rounds"]), 2)


if __name__ == "__main__":
    unittest.main()
