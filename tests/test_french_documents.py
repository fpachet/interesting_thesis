from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


class FrenchDocumentTests(unittest.TestCase):
    def test_french_documents_are_normalized(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "scripts/normalize_french_docs.py", "--check"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("0 document(s) need normalization.", result.stdout)

    def test_prompt_template_variables_remain_ascii_identifiers(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        for path in sorted((project_root / "prompts").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            self.assertIn("$theme", text, path.name)
            self.assertIn("$output_length_instruction", text, path.name)
            self.assertNotIn("$thème", text, path.name)


if __name__ == "__main__":
    unittest.main()
