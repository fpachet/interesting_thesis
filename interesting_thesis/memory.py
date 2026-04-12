from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from .models import (
    AgentOutput,
    CorpusOverview,
    DebateRound,
    DigestResult,
    DocumentMetadata,
    FinalSynthesis,
    MemoryState,
    PipelineConfig,
    RoundSynthesis,
)
from .text_utils import unique_preserve_order


def initialize_memory(config: PipelineConfig, corpus: CorpusOverview) -> MemoryState:
    timestamp = datetime.now(UTC).isoformat()
    return MemoryState(
        theme=config.theme,
        model=config.model,
        output_length=config.output_length.value,
        created_at=timestamp,
        updated_at=timestamp,
        corpus=corpus,
    )


def add_user_note(memory: MemoryState, note: str | None) -> None:
    if not note or not note.strip():
        return
    memory.user_notes = unique_preserve_order([*memory.user_notes, note.strip()])
    memory.updated_at = datetime.now(UTC).isoformat()


def attach_digest(memory: MemoryState, digest: DigestResult) -> None:
    memory.digest = digest
    memory.updated_at = datetime.now(UTC).isoformat()


def append_round(memory: MemoryState, round_record: DebateRound) -> None:
    memory.rounds.append(round_record)
    memory.open_questions = unique_preserve_order(
        [*memory.open_questions, *round_record.synthesis.open_questions]
    )
    memory.reusable_paragraphs = unique_preserve_order(
        [*memory.reusable_paragraphs, *round_record.synthesis.reusable_paragraphs]
    )
    memory.updated_at = datetime.now(UTC).isoformat()


def attach_final_synthesis(memory: MemoryState, final_synthesis: FinalSynthesis) -> None:
    memory.final_synthesis = final_synthesis
    memory.open_questions = unique_preserve_order(
        [*memory.open_questions, *final_synthesis.remaining_objections]
    )
    memory.reusable_paragraphs = unique_preserve_order(
        [*memory.reusable_paragraphs, *final_synthesis.reusable_paragraphs]
    )
    memory.updated_at = datetime.now(UTC).isoformat()


def write_memory(memory: MemoryState, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(memory)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def load_memory(path: Path) -> MemoryState:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return memory_from_dict(payload)


def memory_from_dict(payload: dict[str, object]) -> MemoryState:
    corpus_payload = _require_dict(payload.get("corpus"), "corpus")
    sources_payload = corpus_payload.get("sources")
    if not isinstance(sources_payload, list):
        raise ValueError("Memory payload is missing corpus sources.")

    corpus = CorpusOverview(
        source_count=int(corpus_payload["source_count"]),
        total_characters=int(corpus_payload["total_characters"]),
        total_words=int(corpus_payload["total_words"]),
        sources=[
            DocumentMetadata(
                path=str(source["path"]),
                extension=str(source["extension"]),
                char_count=int(source["char_count"]),
                word_count=int(source["word_count"]),
            )
            for source in (_require_dict(item, "corpus source") for item in sources_payload)
        ],
    )

    digest_payload = payload.get("digest")
    digest = (
        DigestResult(
            markdown=str(_require_dict(digest_payload, "digest")["markdown"]),
            key_ideas=[str(item) for item in _require_dict(digest_payload, "digest")["key_ideas"]],
            tensions=[str(item) for item in _require_dict(digest_payload, "digest")["tensions"]],
            notable_sources=[
                str(item) for item in _require_dict(digest_payload, "digest")["notable_sources"]
            ],
        )
        if digest_payload is not None
        else None
    )

    rounds_payload = payload.get("rounds", [])
    if not isinstance(rounds_payload, list):
        raise ValueError("Memory payload has an invalid 'rounds' field.")
    rounds = [_round_from_dict(_require_dict(item, "round")) for item in rounds_payload]

    final_payload = payload.get("final_synthesis")
    final_synthesis = (
        FinalSynthesis(
            final_markdown=str(_require_dict(final_payload, "final_synthesis")["final_markdown"]),
            reusable_paragraphs=[
                str(item)
                for item in _require_dict(final_payload, "final_synthesis")["reusable_paragraphs"]
            ],
            remaining_objections=[
                str(item)
                for item in _require_dict(final_payload, "final_synthesis")["remaining_objections"]
            ],
            next_angles=[
                str(item) for item in _require_dict(final_payload, "final_synthesis")["next_angles"]
            ],
        )
        if final_payload is not None
        else None
    )

    user_notes_payload = payload.get("user_notes", [])
    if not isinstance(user_notes_payload, list):
        raise ValueError("Memory payload has an invalid 'user_notes' field.")

    return MemoryState(
        theme=str(payload["theme"]),
        model=str(payload["model"]),
        output_length=str(payload["output_length"]),
        created_at=str(payload["created_at"]),
        updated_at=str(payload["updated_at"]),
        corpus=corpus,
        digest=digest,
        rounds=rounds,
        open_questions=[str(item) for item in payload.get("open_questions", [])],
        reusable_paragraphs=[str(item) for item in payload.get("reusable_paragraphs", [])],
        final_synthesis=final_synthesis,
        user_notes=[str(item) for item in user_notes_payload],
    )


def _round_from_dict(payload: dict[str, object]) -> DebateRound:
    agent_outputs_payload = payload.get("agent_outputs", [])
    if not isinstance(agent_outputs_payload, list):
        raise ValueError("Round payload has an invalid 'agent_outputs' field.")
    synthesis_payload = _require_dict(payload.get("synthesis"), "round synthesis")
    return DebateRound(
        round_index=int(payload["round_index"]),
        created_at=str(payload["created_at"]),
        agent_outputs=[
            AgentOutput(
                role_key=str(agent_output["role_key"]),
                role_name=str(agent_output["role_name"]),
                kind=str(agent_output["kind"]),
                markdown=str(agent_output["markdown"]),
            )
            for agent_output in (
                _require_dict(item, "agent_output") for item in agent_outputs_payload
            )
        ],
        synthesis=RoundSynthesis(
            summary_markdown=str(synthesis_payload["summary_markdown"]),
            key_advances=[str(item) for item in synthesis_payload["key_advances"]],
            open_questions=[str(item) for item in synthesis_payload["open_questions"]],
            reusable_paragraphs=[str(item) for item in synthesis_payload["reusable_paragraphs"]],
        ),
    )


def _require_dict(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"Memory payload is missing or invalid: {label}.")
    return value
