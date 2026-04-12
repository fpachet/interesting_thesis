from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .config import build_parser, load_roles, resolve_config
from .errors import InterestingThesisError
from .pipeline import run_pipeline


def main(argv: Sequence[str] | None = None) -> int:
    project_root = Path.cwd()
    parser = build_parser(project_root)
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        config = resolve_config(args, project_root)
        roles = load_roles(config.roles_file)
        outputs = run_pipeline(config, roles)
    except InterestingThesisError as exc:
        parser.exit(status=2, message=f"Error: {exc}\n")
    except KeyboardInterrupt:
        parser.exit(status=130, message="Interrupted.\n")

    print("Run completed.")
    for label, path in outputs.items():
        print(f"- {label}: {path}")
    return 0
