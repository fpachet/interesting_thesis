from __future__ import annotations

from collections.abc import Callable
from collections.abc import Sequence

from .config import length_instruction
from .llm import LLMClient
from .models import DigestResult, PipelineConfig, SourceDocument, TextChunk
from .prompts import PromptLibrary
from .schemas import digest_schema
from .text_utils import excerpt, split_text, unique_preserve_order

ProgressCallback = Callable[[str], None]


def build_corpus_digest(
    documents: Sequence[SourceDocument],
    *,
    config: PipelineConfig,
    prompt_library: PromptLibrary,
    llm_client: LLMClient,
    progress_callback: ProgressCallback | None = None,
) -> DigestResult:
    chunks = build_chunks(documents, max_chars=config.max_chunk_chars)
    report(progress_callback, f"Digest will use {len(chunks)} chunk(s).")
    system_prompt = prompt_library.render(
        "digest.md",
        theme=config.theme,
        output_length_instruction=length_instruction(config.output_length),
    )
    document_inventory = render_document_inventory(documents)
    guidance_block = (
        "Consigne utilisateur supplementaire pour cette execution :\n"
        f"{config.user_note}\n\n"
        if config.user_note
        else ""
    )

    if len(chunks) == 1:
        report(progress_callback, "Digest: using a single chunk, no partial summaries needed.")
        digest_input = render_chunk(chunks[0])
    else:
        partial_summaries: list[str] = []
        for index, chunk in enumerate(chunks, start=1):
            report(progress_callback, f"Digest partial summary {index}/{len(chunks)} ({chunk.chunk_id}).")
            summary = llm_client.generate_text(
                [
                    {"role": "developer", "content": system_prompt},
                    {
                        "role": "user",
                        "content": (
                            f"{guidance_block}"
                            "Produis un digest partiel du segment suivant.\n\n"
                            f"{render_chunk(chunk)}"
                        ),
                    },
                ],
                max_output_tokens=config.max_output_tokens,
                reasoning_effort=config.reasoning_effort,
            )
            partial_summaries.append(f"## {chunk.chunk_id}\n{summary}")
        digest_input = "\n\n".join(partial_summaries)

    report(progress_callback, "Digest: building final structured synthesis.")
    data = llm_client.generate_json(
        [
            {"role": "developer", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"{guidance_block}"
                    "Construit un digest de corpus a partir du materiau suivant.\n\n"
                    f"Inventaire des sources:\n{document_inventory}\n\n"
                    f"{digest_input}"
                ),
            },
        ],
        schema_name="corpus_digest",
        schema_description="Structured digest of a philosophical source corpus.",
        schema=digest_schema(),
        max_output_tokens=config.max_output_tokens,
        reasoning_effort=config.reasoning_effort,
    )

    return DigestResult(
        markdown=str(data["digest_markdown"]).strip(),
        key_ideas=unique_preserve_order(data["key_ideas"]),
        tensions=unique_preserve_order(data["tensions"]),
        notable_sources=unique_preserve_order(data["notable_sources"]),
    )


def build_chunks(documents: Sequence[SourceDocument], *, max_chars: int) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    counter = 1
    for document in documents:
        parts = split_text(document.text, max_chars) or [""]
        for index, part in enumerate(parts, start=1):
            rendered = (
                f"## Source: {document.path}\n"
                f"## Segment: {index}/{len(parts)}\n\n"
                f"{part or '[No extractable text]'}"
            )
            chunks.append(
                TextChunk(
                    chunk_id=f"chunk_{counter:02d}",
                    source_paths=[document.path],
                    text=rendered,
                    char_count=len(rendered),
                )
            )
            counter += 1
    return chunks


def render_chunk(chunk: TextChunk) -> str:
    return chunk.text


def render_digest_markdown(digest: DigestResult) -> str:
    notable_sources = "\n".join(f"- {item}" for item in digest.notable_sources)
    tensions = "\n".join(f"- {item}" for item in digest.tensions)
    key_ideas = "\n".join(f"- {item}" for item in digest.key_ideas)
    return (
        "# Corpus Digest\n\n"
        f"{digest.markdown}\n\n"
        "## Key Ideas\n"
        f"{key_ideas or '- None'}\n\n"
        "## Tensions\n"
        f"{tensions or '- None'}\n\n"
        "## Notable Sources\n"
        f"{notable_sources or '- None'}\n"
    )


def render_document_inventory(documents: Sequence[SourceDocument]) -> str:
    lines = []
    for document in documents:
        lines.append(
            f"- {document.path} ({document.extension}, {document.char_count} chars): "
            f"{excerpt(document.text, max_chars=180) or '[No extractable text]'}"
        )
    return "\n".join(lines)


def report(progress_callback: ProgressCallback | None, message: str) -> None:
    if progress_callback is not None:
        progress_callback(message)
