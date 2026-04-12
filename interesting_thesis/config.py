from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from .errors import ConfigurationError
from .models import OutputLength, PipelineConfig, RoleConfig, RoleKind, RunMode

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
    parser.add_argument(
        "--run-id",
        help="Optional stable identifier for this run.",
    )
    parser.add_argument(
        "--resume-run",
        help="Resume an existing run from its latest checkpoint.",
    )
    parser.add_argument(
        "--fork-run",
        help="Create a new run from a checkpoint of an existing run.",
    )
    parser.add_argument(
        "--from-checkpoint",
        help="Checkpoint name to use when forking, for example 'digest' or 'round_02'.",
    )
    parser.add_argument(
        "--user-note",
        help="Optional user note injected into downstream prompts and checkpoints.",
    )
    parser.add_argument(
        "--no-latest-mirror",
        action="store_true",
        help="Do not mirror the latest run outputs to the legacy top-level files.",
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
    if args.resume_run and args.fork_run:
        raise ConfigurationError("--resume-run and --fork-run cannot be used together.")
    if args.resume_run and args.run_id:
        raise ConfigurationError("--run-id cannot be used with --resume-run.")
    if args.resume_run and args.from_checkpoint:
        raise ConfigurationError("--from-checkpoint can only be used with --fork-run.")
    if args.from_checkpoint and not args.fork_run:
        raise ConfigurationError("--from-checkpoint requires --fork-run.")

    project_root = project_root.resolve()
    output_dir = resolve_path(args.output_dir, project_root)
    memory_file = resolve_path(args.memory_file, project_root)

    run_mode = RunMode.START
    run_id: str
    resume_checkpoint_path: Path | None = None
    resume_checkpoint_name: str | None = None
    parent_run_id: str | None = None

    if args.resume_run:
        run_mode = RunMode.RESUME
        run_id = _normalize_run_id(args.resume_run)
        resume_checkpoint_path = _resolve_existing_checkpoint(
            output_dir=output_dir,
            run_id=run_id,
            checkpoint_name=None,
        )
        resume_checkpoint_name = resume_checkpoint_path.stem
    elif args.fork_run:
        run_mode = RunMode.FORK
        parent_run_id = _normalize_run_id(args.fork_run)
        resume_checkpoint_path = _resolve_existing_checkpoint(
            output_dir=output_dir,
            run_id=parent_run_id,
            checkpoint_name=args.from_checkpoint,
        )
        resume_checkpoint_name = resume_checkpoint_path.stem
        run_id = _normalize_run_id(args.run_id) if args.run_id else _default_fork_run_id(parent_run_id)
    else:
        run_id = _normalize_run_id(args.run_id) if args.run_id else _default_run_id()

    run_output_dir = output_dir / "runs" / run_id
    run_memory_file = memory_file.parent / "runs" / f"{run_id}.json"

    return PipelineConfig(
        project_root=project_root,
        input_dir=resolve_path(args.input_dir, project_root),
        output_dir=output_dir,
        memory_file=memory_file,
        run_output_dir=run_output_dir,
        run_memory_file=run_memory_file,
        prompts_dir=resolve_path(args.prompts_dir, project_root),
        roles_file=resolve_path(args.roles_file, project_root),
        theme=args.theme.strip(),
        model=args.model.strip(),
        rounds=args.rounds,
        output_length=OutputLength(args.output_length),
        dry_run=args.dry_run,
        run_id=run_id,
        run_mode=run_mode,
        resume_checkpoint_path=resume_checkpoint_path,
        resume_checkpoint_name=resume_checkpoint_name,
        parent_run_id=parent_run_id,
        user_note=args.user_note.strip() if args.user_note and args.user_note.strip() else None,
        mirror_latest_outputs=not args.no_latest_mirror,
        max_chunk_chars=args.max_chunk_chars,
        max_output_tokens=args.max_output_tokens,
        reasoning_effort=args.reasoning_effort,
    )


def checkpoint_path(run_output_dir: Path, checkpoint_name: str) -> Path:
    return run_output_dir / "checkpoints" / f"{checkpoint_name}.json"


def write_config_snapshot(config: PipelineConfig, roles: list[RoleConfig]) -> None:
    payload = {
        "run_id": config.run_id,
        "run_mode": config.run_mode.value,
        "parent_run_id": config.parent_run_id,
        "resume_checkpoint_name": config.resume_checkpoint_name,
        "theme": config.theme,
        "model": config.model,
        "rounds": config.rounds,
        "output_length": config.output_length.value,
        "dry_run": config.dry_run,
        "max_chunk_chars": config.max_chunk_chars,
        "max_output_tokens": config.max_output_tokens,
        "reasoning_effort": config.reasoning_effort,
        "user_note": config.user_note,
        "mirror_latest_outputs": config.mirror_latest_outputs,
        "paths": {
            "project_root": str(config.project_root),
            "input_dir": str(config.input_dir),
            "output_dir": str(config.output_dir),
            "run_output_dir": str(config.run_output_dir),
            "memory_file": str(config.memory_file),
            "run_memory_file": str(config.run_memory_file),
            "prompts_dir": str(config.prompts_dir),
            "roles_file": str(config.roles_file),
        },
        "roles": [
            {
                "key": role.key,
                "name": role.name,
                "kind": role.kind.value,
                "prompt_file": role.prompt_file,
            }
            for role in roles
        ],
    }
    snapshot_path = config.run_output_dir / "config_snapshot.json"
    snapshot_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _normalize_run_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    cleaned = cleaned.strip("._-")
    if not cleaned:
        raise ConfigurationError("Run id cannot be empty after normalization.")
    return cleaned


def _default_run_id() -> str:
    return f"run_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"


def _default_fork_run_id(parent_run_id: str) -> str:
    return f"{parent_run_id}_fork_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"


def _resolve_existing_checkpoint(
    *,
    output_dir: Path,
    run_id: str,
    checkpoint_name: str | None,
) -> Path:
    run_output_dir = output_dir / "runs" / run_id
    checkpoints_dir = run_output_dir / "checkpoints"
    if not checkpoints_dir.exists():
        raise ConfigurationError(f"Checkpoint directory not found for run '{run_id}'.")

    if checkpoint_name:
        candidate = checkpoints_dir / f"{checkpoint_name}.json"
        if not candidate.exists():
            raise ConfigurationError(
                f"Checkpoint '{checkpoint_name}' not found for run '{run_id}'."
            )
        return candidate

    checkpoints = sorted(
        checkpoints_dir.glob("*.json"),
        key=lambda path: path.stat().st_mtime_ns,
    )
    if not checkpoints:
        raise ConfigurationError(f"No checkpoints found for run '{run_id}'.")
    return checkpoints[-1]


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
