from __future__ import annotations

from pathlib import Path
from string import Template

from .errors import ConfigurationError


class PromptLibrary:
    def __init__(self, prompts_dir: Path) -> None:
        self.prompts_dir = prompts_dir
        self._cache: dict[str, str] = {}

    def load(self, prompt_file: str) -> str:
        path = self.prompts_dir / prompt_file
        if not path.exists():
            raise ConfigurationError(f"Prompt not found: {path}")
        if prompt_file not in self._cache:
            self._cache[prompt_file] = path.read_text(encoding="utf-8").strip()
        return self._cache[prompt_file]

    def render(self, prompt_file: str, **variables: str) -> str:
        template = Template(self.load(prompt_file))
        stringified = {key: str(value) for key, value in variables.items()}
        return template.safe_substitute(stringified)
