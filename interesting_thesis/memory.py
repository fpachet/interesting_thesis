from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from .models import CorpusOverview
from .models import DebateRound, DigestResult, FinalSynthesis, MemoryState, PipelineConfig
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
