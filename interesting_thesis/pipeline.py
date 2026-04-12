from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

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
from .memory import append_round, attach_digest, attach_final_synthesis, initialize_memory, write_memory
from .models import PipelineConfig, RoleConfig
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

    report(progress_callback, f"Scanning corpus in {config.input_dir}.")
    documents = load_documents(config.input_dir)
    if not documents:
        raise ConfigurationError(
            f"No supported input documents found in {config.input_dir}."
        )

    corpus = build_corpus_overview(documents)
    report(
        progress_callback,
        (
            f"Loaded {corpus.source_count} source(s), "
            f"{corpus.total_words} words, {corpus.total_characters} characters."
        ),
    )
    memory = initialize_memory(config, corpus)
    prompt_library = PromptLibrary(config.prompts_dir)
    client_label = "dry-run client" if config.dry_run else f"OpenAI client ({config.model})"
    report(progress_callback, f"Initializing {client_label}.")
    llm_client = build_llm_client(config)

    write_memory(memory, config.memory_file)

    report(progress_callback, "Building corpus digest.")
    digest = build_corpus_digest(
        documents,
        config=config,
        prompt_library=prompt_library,
        llm_client=llm_client,
        progress_callback=progress_callback,
    )
    attach_digest(memory, digest)
    digest_path = config.output_dir / "corpus_digest.md"
    write_text(digest_path, render_digest_markdown(digest))
    report(progress_callback, f"Digest written to {digest_path.name}.")
    write_memory(memory, config.memory_file)

    round_paths: list[Path] = []
    for round_index in range(1, config.rounds + 1):
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
        round_path = config.output_dir / f"round_{round_index:02d}.md"
        write_text(round_path, render_round_markdown(round_record))
        round_paths.append(round_path)
        report(progress_callback, f"Round {round_index}/{config.rounds} written to {round_path.name}.")
        write_memory(memory, config.memory_file)

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
    final_synthesis_path = config.output_dir / "final_synthesis.md"
    paragraphs_path = config.output_dir / "thesis_paragraphs.md"
    write_text(final_synthesis_path, render_final_synthesis_markdown(final_synthesis, memory))
    write_text(paragraphs_path, render_paragraphs_markdown(memory.reusable_paragraphs))
    report(progress_callback, f"Final synthesis written to {final_synthesis_path.name}.")
    report(progress_callback, f"Reusable paragraphs written to {paragraphs_path.name}.")
    write_memory(memory, config.memory_file)
    report(progress_callback, "Pipeline finished successfully.")

    return {
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
    if not config.prompts_dir.exists():
        raise ConfigurationError(f"Prompts directory not found: {config.prompts_dir}")
    if not config.roles_file.exists():
        raise ConfigurationError(f"Roles file not found: {config.roles_file}")


def build_llm_client(config: PipelineConfig) -> LLMClient:
    if config.dry_run:
        return DryRunClient(model=config.model)
    return OpenAIResponsesClient(model=config.model)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def report(progress_callback: ProgressCallback | None, message: str) -> None:
    if progress_callback is not None:
        progress_callback(message)
