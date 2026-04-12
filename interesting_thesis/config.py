from __future__ import annotations

import argparse
import json
from pathlib import Path

from .errors import ConfigurationError
from .models import OutputLength, PipelineConfig, RoleConfig, RoleKind

DEFAULT_THEME = (
    "L'objet interessant comme solution relativement rare d'un probleme "
    "d'echantillonnage sous contrainte."
)
DEFAULT_MODEL = "gpt-5.4-mini"

_OUTPUT_LENGTH_INSTRUCTIONS = {
    OutputLength.SHORT: "reponse concise, dense, sans digression inutile",
    OutputLength.MEDIUM: "reponse developpee mais resserree, exploitable telle quelle",
    OutputLength.LONG: "reponse ample, argumentative, avec nuances et reformulations reutilisables",
}


def build_parser(project_root: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="interesting-thesis",
        description="Generate a multi-agent philosophical debate from a personal corpus.",
    )
    parser.add_argument("--theme", default=DEFAULT_THEME, help="Central thesis theme.")
    parser.add_argument("--rounds", type=int, default=3, help="Number of debate rounds.")
    parser.add_argument(
        "--output-length",
        choices=[item.value for item in OutputLength],
        default=OutputLength.MEDIUM.value,
        help="Target output length.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=project_root / "input",
        help="Directory containing source documents.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=project_root / "output",
        help="Directory where Markdown outputs are written.",
    )
    parser.add_argument(
        "--memory-file",
        type=Path,
        default=project_root / "memory" / "state.json",
        help="JSON state file.",
    )
    parser.add_argument(
        "--prompts-dir",
        type=Path,
        default=project_root / "prompts",
        help="Directory containing external prompts.",
    )
    parser.add_argument(
        "--roles-file",
        type=Path,
        default=project_root / "config" / "default_roles.json",
        help="JSON file describing debate roles.",
    )
    parser.add_argument(
        "--max-chunk-chars",
        type=int,
        default=12_000,
        help="Approximate maximum character count per corpus chunk.",
    )
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        default=3_000,
        help="Upper bound for generated tokens per call.",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "medium", "high", "xhigh"],
        default=None,
        help="Optional reasoning effort for compatible reasoning models.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run locally without calling the OpenAI API.",
    )
    return parser


def length_instruction(output_length: OutputLength) -> str:
    return _OUTPUT_LENGTH_INSTRUCTIONS[output_length]


def resolve_path(path: Path, project_root: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    return (project_root / path).resolve()


def resolve_config(args: argparse.Namespace, project_root: Path) -> PipelineConfig:
    if args.rounds < 1:
        raise ConfigurationError("--rounds must be >= 1.")
    if args.max_chunk_chars < 2_000:
        raise ConfigurationError("--max-chunk-chars must be >= 2000.")
    if args.max_output_tokens < 256:
        raise ConfigurationError("--max-output-tokens must be >= 256.")
    if not str(args.theme).strip():
        raise ConfigurationError("--theme must not be empty.")
    if not str(args.model).strip():
        raise ConfigurationError("--model must not be empty.")

    return PipelineConfig(
        project_root=project_root.resolve(),
        input_dir=resolve_path(args.input_dir, project_root),
        output_dir=resolve_path(args.output_dir, project_root),
        memory_file=resolve_path(args.memory_file, project_root),
        prompts_dir=resolve_path(args.prompts_dir, project_root),
        roles_file=resolve_path(args.roles_file, project_root),
        theme=args.theme.strip(),
        model=args.model.strip(),
        rounds=args.rounds,
        output_length=OutputLength(args.output_length),
        dry_run=args.dry_run,
        max_chunk_chars=args.max_chunk_chars,
        max_output_tokens=args.max_output_tokens,
        reasoning_effort=args.reasoning_effort,
    )


def load_roles(roles_file: Path) -> list[RoleConfig]:
    if not roles_file.exists():
        raise ConfigurationError(f"Roles file not found: {roles_file}")

    try:
        raw_roles = json.loads(roles_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigurationError(f"Invalid JSON in roles file: {roles_file}") from exc

    if not isinstance(raw_roles, list) or not raw_roles:
        raise ConfigurationError("Roles file must contain a non-empty list.")

    roles: list[RoleConfig] = []
    for item in raw_roles:
        try:
            role = RoleConfig(
                key=str(item["key"]).strip(),
                name=str(item["name"]).strip(),
                kind=RoleKind(str(item["kind"]).strip()),
                prompt_file=str(item["prompt_file"]).strip(),
            )
        except KeyError as exc:
            raise ConfigurationError(f"Missing role field in {roles_file}: {exc}") from exc
        except ValueError as exc:
            raise ConfigurationError(f"Invalid role kind in {roles_file}: {exc}") from exc

        if not role.key or not role.name or not role.prompt_file:
            raise ConfigurationError(f"Invalid empty role field in {roles_file}.")
        roles.append(role)

    synthesizers = [role for role in roles if role.kind == RoleKind.SYNTHESIZER]
    if len(synthesizers) != 1:
        raise ConfigurationError("Exactly one role must be of kind 'synthesizer'.")
    if roles[-1].kind != RoleKind.SYNTHESIZER:
        raise ConfigurationError("The final role must be the synthesizer.")

    return roles
