from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from .config import checkpoint_path, write_config_snapshot
from .debate import (
    build_final_synthesis,
    render_final_synthesis_markdown,
    render_paragraphs_markdown,
    render_round_markdown,
    run_round,
)
from .digest import build_corpus_digest, render_digest_markdown
from .errors import ConfigurationError
from .ingestion import build_corpus_overview, load_documents
from .llm import DryRunClient, LLMClient, OpenAIResponsesClient
from .memory import (
    add_user_note,
    append_round,
    attach_digest,
    attach_final_synthesis,
    initialize_memory,
    load_memory,
    write_memory,
)
from .models import PipelineConfig, RoleConfig, RunMode
from .prompts import PromptLibrary

ProgressCallback = Callable[[str], None]


def run_pipeline(
    config: PipelineConfig,
    roles: list[RoleConfig],
    *,
    progress_callback: ProgressCallback | None = None,
) -> dict[str, Path]:
    report(progress_callback, "Preparing runtime layout.")
    ensure_runtime_layout(config)
    snapshot_path = config.run_output_dir / "config_snapshot.json"
    if not snapshot_path.exists():
        write_config_snapshot(config, roles)

    prompt_library = PromptLibrary(config.prompts_dir)
    client_label = "dry-run client" if config.dry_run else f"OpenAI client ({config.model})"
    report(progress_callback, f"Initializing {client_label}.")
    llm_client = build_llm_client(config)
    documents = None

    if config.resume_checkpoint_path is not None:
        report(
            progress_callback,
            (
                f"Loading checkpoint '{config.resume_checkpoint_name}' "
                f"for run {config.run_id}."
            ),
        )
        memory = load_memory(config.resume_checkpoint_path)
        materialize_outputs_from_memory(config, memory)
    else:
        documents = load_corpus_documents(config, progress_callback)
        corpus = build_corpus_overview(documents)
        report(
            progress_callback,
            (
                f"Loaded {corpus.source_count} source(s), "
                f"{corpus.total_words} words, {corpus.total_characters} characters."
            ),
        )
        memory = initialize_memory(config, corpus)

    add_user_note(memory, config.user_note)
    sync_memory_state(config, memory)
    if config.run_mode == RunMode.FORK and config.resume_checkpoint_name is not None:
        write_checkpoint(config, memory, config.resume_checkpoint_name)

    if len(memory.rounds) > config.rounds:
        raise ConfigurationError(
            "Checkpoint contains more rounds than the current configuration allows."
        )

    if memory.digest is None:
        if documents is None:
            documents = load_corpus_documents(config, progress_callback)
        report(progress_callback, "Building corpus digest.")
        digest = build_corpus_digest(
            documents,
            config=config,
            prompt_library=prompt_library,
            llm_client=llm_client,
            progress_callback=progress_callback,
        )
        attach_digest(memory, digest)
        digest_path = write_artifact(config, "corpus_digest.md", render_digest_markdown(digest))
        report(progress_callback, f"Digest written to {digest_path.name}.")
        sync_memory_state(config, memory)
        write_checkpoint(config, memory, "digest")
    else:
        digest = memory.digest
        digest_path = config.run_output_dir / "corpus_digest.md"
        report(progress_callback, "Digest already available from checkpoint; skipping recompute.")

    round_paths: list[Path] = [
        config.run_output_dir / f"round_{round_record.round_index:02d}.md"
        for round_record in memory.rounds
    ]
    for round_index in range(len(memory.rounds) + 1, config.rounds + 1):
        report(progress_callback, f"Starting round {round_index}/{config.rounds}.")
        round_record = run_round(
            round_index=round_index,
            roles=roles,
            digest=digest,
            memory=memory,
            config=config,
            prompt_library=prompt_library,
            llm_client=llm_client,
            progress_callback=progress_callback,
        )
        append_round(memory, round_record)
        round_path = write_artifact(
            config,
            f"round_{round_index:02d}.md",
            render_round_markdown(round_record),
        )
        round_paths.append(round_path)
        report(progress_callback, f"Round {round_index}/{config.rounds} written to {round_path.name}.")
        sync_memory_state(config, memory)
        write_checkpoint(config, memory, f"round_{round_index:02d}")

    if memory.final_synthesis is None:
        report(progress_callback, "Building final synthesis.")
        final_synthesis = build_final_synthesis(
            digest=digest,
            memory=memory,
            config=config,
            prompt_library=prompt_library,
            llm_client=llm_client,
            progress_callback=progress_callback,
        )
        attach_final_synthesis(memory, final_synthesis)
        final_synthesis_path = write_artifact(
            config,
            "final_synthesis.md",
            render_final_synthesis_markdown(final_synthesis, memory),
        )
        paragraphs_path = write_artifact(
            config,
            "thesis_paragraphs.md",
            render_paragraphs_markdown(memory.reusable_paragraphs),
        )
        report(progress_callback, f"Final synthesis written to {final_synthesis_path.name}.")
        report(progress_callback, f"Reusable paragraphs written to {paragraphs_path.name}.")
        sync_memory_state(config, memory)
        write_checkpoint(config, memory, "final")
    else:
        final_synthesis_path = config.run_output_dir / "final_synthesis.md"
        paragraphs_path = config.run_output_dir / "thesis_paragraphs.md"
        report(progress_callback, "Final synthesis already present in checkpoint; nothing left to compute.")

    report(progress_callback, "Pipeline finished successfully.")

    return {
        "run_dir": config.run_output_dir,
        "run_memory": config.run_memory_file,
        "digest": digest_path,
        "memory": config.memory_file,
        "final_synthesis": final_synthesis_path,
        "paragraphs": paragraphs_path,
        "last_round": round_paths[-1],
    }


def ensure_runtime_layout(config: PipelineConfig) -> None:
    config.input_dir.mkdir(parents=True, exist_ok=True)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    config.memory_file.parent.mkdir(parents=True, exist_ok=True)
    config.run_memory_file.parent.mkdir(parents=True, exist_ok=True)
    if not config.prompts_dir.exists():
        raise ConfigurationError(f"Prompts directory not found: {config.prompts_dir}")
    if not config.roles_file.exists():
        raise ConfigurationError(f"Roles file not found: {config.roles_file}")
    if config.run_mode == RunMode.RESUME:
        if not config.run_output_dir.exists():
            raise ConfigurationError(f"Run directory not found: {config.run_output_dir}")
    else:
        if config.run_output_dir.exists():
            raise ConfigurationError(f"Run directory already exists: {config.run_output_dir}")
        config.run_output_dir.mkdir(parents=True, exist_ok=False)
    (config.run_output_dir / "checkpoints").mkdir(parents=True, exist_ok=True)
    if config.run_mode != RunMode.RESUME and config.run_memory_file.exists():
        raise ConfigurationError(f"Run memory file already exists: {config.run_memory_file}")


def build_llm_client(config: PipelineConfig) -> LLMClient:
    if config.dry_run:
        return DryRunClient(model=config.model)
    return OpenAIResponsesClient(model=config.model)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def load_corpus_documents(
    config: PipelineConfig,
    progress_callback: ProgressCallback | None = None,
):
    report(progress_callback, f"Scanning corpus in {config.input_dir}.")
    documents = load_documents(config.input_dir)
    if not documents:
        raise ConfigurationError(
            f"No supported input documents found in {config.input_dir}."
        )
    return documents


def sync_memory_state(config: PipelineConfig, memory) -> None:
    write_memory(memory, config.run_memory_file)
    if config.mirror_latest_outputs:
        write_memory(memory, config.memory_file)


def write_artifact(config: PipelineConfig, file_name: str, content: str) -> Path:
    run_path = config.run_output_dir / file_name
    write_text(run_path, content)
    if config.mirror_latest_outputs:
        write_text(config.output_dir / file_name, content)
    return run_path


def write_checkpoint(config: PipelineConfig, memory, checkpoint_name: str) -> Path:
    target = checkpoint_path(config.run_output_dir, checkpoint_name)
    write_memory(memory, target)
    return target


def materialize_outputs_from_memory(config: PipelineConfig, memory) -> None:
    if memory.digest is not None:
        write_artifact(config, "corpus_digest.md", render_digest_markdown(memory.digest))
    for round_record in memory.rounds:
        write_artifact(
            config,
            f"round_{round_record.round_index:02d}.md",
            render_round_markdown(round_record),
        )
    if memory.final_synthesis is not None:
        write_artifact(
            config,
            "final_synthesis.md",
            render_final_synthesis_markdown(memory.final_synthesis, memory),
        )
        write_artifact(
            config,
            "thesis_paragraphs.md",
            render_paragraphs_markdown(memory.reusable_paragraphs),
        )


def report(progress_callback: ProgressCallback | None, message: str) -> None:
    if progress_callback is not None:
        progress_callback(message)
