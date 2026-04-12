from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from interesting_thesis.env import load_env_file


class EnvLoadingTests(unittest.TestCase):
    def test_load_env_file_sets_missing_values(self) -> None:
        key = "INTERESTING_THESIS_TEST_KEY"
        original = os.environ.get(key)
        os.environ.pop(key, None)

        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                env_path = Path(tmp_dir) / ".env"
                env_path.write_text(f"{key}=hello\n", encoding="utf-8")
                load_env_file(env_path)
                self.assertEqual(os.environ.get(key), "hello")
        finally:
            if original is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original

    def test_load_env_file_does_not_override_existing_env(self) -> None:
        key = "INTERESTING_THESIS_TEST_KEY"
        original = os.environ.get(key)
        os.environ[key] = "existing"

        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                env_path = Path(tmp_dir) / ".env"
                env_path.write_text(f"{key}=new-value\n", encoding="utf-8")
                load_env_file(env_path)
                self.assertEqual(os.environ.get(key), "existing")
        finally:
            if original is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original


if __name__ == "__main__":
    unittest.main()
