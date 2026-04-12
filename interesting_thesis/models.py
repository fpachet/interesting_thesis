from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class OutputLength(StrEnum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


class RunMode(StrEnum):
    START = "start"
    RESUME = "resume"
    FORK = "fork"


class RoleKind(StrEnum):
    BUILDER = "builder"
    CRITIC = "critic"
    ANALYST = "analyst"
    SYNTHESIZER = "synthesizer"


@dataclass(frozen=True)
class RoleConfig:
    key: str
    name: str
    kind: RoleKind
    prompt_file: str


@dataclass(frozen=True)
class PipelineConfig:
    project_root: Path
    input_dir: Path
    output_dir: Path
    memory_file: Path
    run_output_dir: Path
    run_memory_file: Path
    prompts_dir: Path
    roles_file: Path
    theme: str
    model: str
    rounds: int
    output_length: OutputLength
    dry_run: bool
    run_id: str
    run_mode: RunMode
    resume_checkpoint_path: Path | None = None
    resume_checkpoint_name: str | None = None
    parent_run_id: str | None = None
    user_note: str | None = None
    mirror_latest_outputs: bool = True
    max_chunk_chars: int = 12_000
    max_output_tokens: int = 3_000
    reasoning_effort: str | None = None


@dataclass(frozen=True)
class SourceDocument:
    path: str
    extension: str
    text: str
    char_count: int
    word_count: int


@dataclass(frozen=True)
class TextChunk:
    chunk_id: str
    source_paths: list[str]
    text: str
    char_count: int


@dataclass(frozen=True)
class DocumentMetadata:
    path: str
    extension: str
    char_count: int
    word_count: int


@dataclass(frozen=True)
class CorpusOverview:
    source_count: int
    total_characters: int
    total_words: int
    sources: list[DocumentMetadata]


@dataclass(frozen=True)
class DigestResult:
    markdown: str
    key_ideas: list[str]
    tensions: list[str]
    notable_sources: list[str]


@dataclass(frozen=True)
class AgentOutput:
    role_key: str
    role_name: str
    kind: str
    markdown: str


@dataclass(frozen=True)
class RoundSynthesis:
    summary_markdown: str
    key_advances: list[str]
    open_questions: list[str]
    reusable_paragraphs: list[str]


@dataclass(frozen=True)
class DebateRound:
    round_index: int
    created_at: str
    agent_outputs: list[AgentOutput]
    synthesis: RoundSynthesis


@dataclass(frozen=True)
class FinalSynthesis:
    final_markdown: str
    reusable_paragraphs: list[str]
    remaining_objections: list[str]
    next_angles: list[str]


@dataclass
class MemoryState:
    theme: str
    model: str
    output_length: str
    created_at: str
    updated_at: str
    corpus: CorpusOverview
    digest: DigestResult | None = None
    rounds: list[DebateRound] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    reusable_paragraphs: list[str] = field(default_factory=list)
    final_synthesis: FinalSynthesis | None = None
    user_notes: list[str] = field(default_factory=list)
