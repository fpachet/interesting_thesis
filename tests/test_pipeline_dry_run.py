from __future__ import annotations

import json
import shutil
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
                    "--run-id",
                    "baseline",
                    "--rounds",
                    "2",
                    "--user-note",
                    "Ajouter des exemples concrets.",
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
            self.assertTrue((output_dir / "runs" / "baseline" / "config_snapshot.json").exists())
            self.assertTrue((output_dir / "runs" / "baseline" / "checkpoints" / "digest.json").exists())
            self.assertTrue((output_dir / "runs" / "baseline" / "checkpoints" / "round_01.json").exists())
            self.assertTrue((output_dir / "runs" / "baseline" / "checkpoints" / "round_02.json").exists())
            self.assertTrue((output_dir / "runs" / "baseline" / "checkpoints" / "final.json").exists())
            self.assertTrue((tmp_path / "memory" / "runs" / "baseline.json").exists())

            payload = json.loads(memory_file.read_text(encoding="utf-8"))
            self.assertEqual(payload["theme"], DEFAULT_THEME)
            self.assertEqual(len(payload["rounds"]), 2)
            self.assertEqual(payload["user_notes"], ["Ajouter des exemples concrets."])

            snapshot = json.loads(
                (output_dir / "runs" / "baseline" / "config_snapshot.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(snapshot["run_id"], "baseline")
            self.assertEqual(snapshot["run_mode"], "start")
            self.assertEqual(snapshot["roles"][-1]["kind"], "synthesizer")

    def test_fork_run_creates_a_new_archived_run(self) -> None:
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
                "# Notes\n\nUne contrainte pertinente rend une solution lisible.",
                encoding="utf-8",
            )

            baseline_exit_code = main(
                [
                    "--dry-run",
                    "--run-id",
                    "baseline",
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
            self.assertEqual(baseline_exit_code, 0)

            fork_exit_code = main(
                [
                    "--dry-run",
                    "--run-id",
                    "forked",
                    "--fork-run",
                    "baseline",
                    "--from-checkpoint",
                    "round_01",
                    "--rounds",
                    "2",
                    "--user-note",
                    "Ajouter un exemple musical.",
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
            self.assertEqual(fork_exit_code, 0)

            fork_run_dir = output_dir / "runs" / "forked"
            self.assertTrue(fork_run_dir.exists())
            self.assertTrue((fork_run_dir / "round_01.md").exists())
            self.assertTrue((fork_run_dir / "round_02.md").exists())
            self.assertTrue((fork_run_dir / "final_synthesis.md").exists())
            self.assertTrue((fork_run_dir / "checkpoints" / "round_01.json").exists())

            fork_snapshot = json.loads(
                (fork_run_dir / "config_snapshot.json").read_text(encoding="utf-8")
            )
            self.assertEqual(fork_snapshot["run_mode"], "fork")
            self.assertEqual(fork_snapshot["parent_run_id"], "baseline")
            self.assertEqual(fork_snapshot["resume_checkpoint_name"], "round_01")

            fork_memory = json.loads(
                (tmp_path / "memory" / "runs" / "forked.json").read_text(encoding="utf-8")
            )
            self.assertIn("Ajouter un exemple musical.", fork_memory["user_notes"])

    def test_resume_run_continues_from_latest_checkpoint(self) -> None:
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
                "# Notes\n\nUne bonne these doit distinguer rarete et lisibilite.",
                encoding="utf-8",
            )

            baseline_exit_code = main(
                [
                    "--dry-run",
                    "--run-id",
                    "baseline",
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
            self.assertEqual(baseline_exit_code, 0)

            partial_run_dir = output_dir / "runs" / "partial"
            checkpoints_dir = partial_run_dir / "checkpoints"
            checkpoints_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                output_dir / "runs" / "baseline" / "checkpoints" / "round_01.json",
                checkpoints_dir / "round_01.json",
            )

            resume_exit_code = main(
                [
                    "--dry-run",
                    "--resume-run",
                    "partial",
                    "--rounds",
                    "2",
                    "--user-note",
                    "Poursuivre avec un contre-exemple.",
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
            self.assertEqual(resume_exit_code, 0)

            self.assertTrue((partial_run_dir / "round_01.md").exists())
            self.assertTrue((partial_run_dir / "round_02.md").exists())
            self.assertTrue((partial_run_dir / "final_synthesis.md").exists())

            resume_snapshot = json.loads(
                (partial_run_dir / "config_snapshot.json").read_text(encoding="utf-8")
            )
            self.assertEqual(resume_snapshot["run_mode"], "resume")

            partial_memory = json.loads(
                (tmp_path / "memory" / "runs" / "partial.json").read_text(encoding="utf-8")
            )
            self.assertEqual(len(partial_memory["rounds"]), 2)
            self.assertIn("Poursuivre avec un contre-exemple.", partial_memory["user_notes"])


if __name__ == "__main__":
    unittest.main()
