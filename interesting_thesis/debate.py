from __future__ import annotations

from datetime import UTC, datetime

from .config import length_instruction
from .llm import LLMClient
from .models import (
    AgentOutput,
    DebateRound,
    DigestResult,
    FinalSynthesis,
    MemoryState,
    PipelineConfig,
    RoleConfig,
    RoleKind,
    RoundSynthesis,
)
from .prompts import PromptLibrary
from .schemas import final_synthesis_schema, round_synthesis_schema
from .text_utils import unique_preserve_order


def run_round(
    *,
    round_index: int,
    roles: list[RoleConfig],
    digest: DigestResult,
    memory: MemoryState,
    config: PipelineConfig,
    prompt_library: PromptLibrary,
    llm_client: LLMClient,
) -> DebateRound:
    agent_outputs: list[AgentOutput] = []
    synthesis: RoundSynthesis | None = None
    shared_context = build_shared_context(
        round_index=round_index,
        digest=digest,
        memory=memory,
    )

    for role in roles:
        system_prompt = prompt_library.render(
            role.prompt_file,
            theme=config.theme,
            output_length_instruction=length_instruction(config.output_length),
        )
        current_round_context = render_current_round_context(agent_outputs)
        user_content = (
            f"{shared_context}\n\n"
            "Sorties deja produites dans cette manche :\n"
            f"{current_round_context}"
        )

        if role.kind == RoleKind.SYNTHESIZER:
            data = llm_client.generate_json(
                [
                    {"role": "developer", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                schema_name="round_synthesis",
                schema_description="Structured synthesis for a debate round.",
                schema=round_synthesis_schema(),
                max_output_tokens=config.max_output_tokens,
                reasoning_effort=config.reasoning_effort,
            )
            synthesis = RoundSynthesis(
                summary_markdown=str(data["summary_markdown"]).strip(),
                key_advances=unique_preserve_order(data["key_advances"]),
                open_questions=unique_preserve_order(data["open_questions"]),
                reusable_paragraphs=unique_preserve_order(data["reusable_paragraphs"]),
            )
            agent_outputs.append(
                AgentOutput(
                    role_key=role.key,
                    role_name=role.name,
                    kind=role.kind.value,
                    markdown=synthesis.summary_markdown,
                )
            )
            continue

        output = llm_client.generate_text(
            [
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            max_output_tokens=config.max_output_tokens,
            reasoning_effort=config.reasoning_effort,
        )
        agent_outputs.append(
            AgentOutput(
                role_key=role.key,
                role_name=role.name,
                kind=role.kind.value,
                markdown=output.strip(),
            )
        )

    if synthesis is None:
        raise RuntimeError("No synthesizer output was produced.")

    return DebateRound(
        round_index=round_index,
        created_at=datetime.now(UTC).isoformat(),
        agent_outputs=agent_outputs,
        synthesis=synthesis,
    )


def build_final_synthesis(
    *,
    digest: DigestResult,
    memory: MemoryState,
    config: PipelineConfig,
    prompt_library: PromptLibrary,
    llm_client: LLMClient,
) -> FinalSynthesis:
    system_prompt = prompt_library.render(
        "final_synthesis.md",
        theme=config.theme,
        output_length_instruction=length_instruction(config.output_length),
    )
    data = llm_client.generate_json(
        [
            {"role": "developer", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "Digest du corpus :\n"
                    f"{digest.markdown}\n\n"
                    "Memoire des manches :\n"
                    f"{render_memory_for_prompt(memory)}"
                ),
            },
        ],
        schema_name="final_synthesis",
        schema_description="Structured final synthesis for a philosophical debate.",
        schema=final_synthesis_schema(),
        max_output_tokens=config.max_output_tokens,
        reasoning_effort=config.reasoning_effort,
    )

    return FinalSynthesis(
        final_markdown=str(data["final_markdown"]).strip(),
        reusable_paragraphs=unique_preserve_order(data["reusable_paragraphs"]),
        remaining_objections=unique_preserve_order(data["remaining_objections"]),
        next_angles=unique_preserve_order(data["next_angles"]),
    )


def build_shared_context(*, round_index: int, digest: DigestResult, memory: MemoryState) -> str:
    return (
        f"Manche en cours: {round_index}\n\n"
        "Digest du corpus:\n"
        f"{digest.markdown}\n\n"
        "Memoire utile:\n"
        f"{render_memory_for_prompt(memory)}"
    )


def render_memory_for_prompt(memory: MemoryState) -> str:
    previous_rounds = memory.rounds[-2:]
    if previous_rounds:
        round_blocks = []
        for round_record in previous_rounds:
            round_blocks.append(
                f"### Manche {round_record.round_index}\n"
                f"{round_record.synthesis.summary_markdown}"
            )
        rounds_text = "\n\n".join(round_blocks)
    else:
        rounds_text = "Aucune manche precedente."

    open_questions = "\n".join(f"- {item}" for item in memory.open_questions[:8]) or "- None"
    reusable_paragraphs = "\n".join(
        f"- {item}" for item in memory.reusable_paragraphs[:6]
    ) or "- None"

    return (
        f"{rounds_text}\n\n"
        "Questions ouvertes:\n"
        f"{open_questions}\n\n"
        "Paragraphes reutilisables deja identifies:\n"
        f"{reusable_paragraphs}"
    )


def render_current_round_context(agent_outputs: list[AgentOutput]) -> str:
    if not agent_outputs:
        return "- Aucune sortie precedente dans cette manche."
    return "\n\n".join(
        f"## {output.role_name}\n{output.markdown}" for output in agent_outputs
    )


def render_round_markdown(round_record: DebateRound) -> str:
    sections = [f"# Manche {round_record.round_index}", ""]
    for output in round_record.agent_outputs:
        sections.append(f"## {output.role_name}")
        sections.append(output.markdown)
        sections.append("")

    sections.append("## Acquis")
    sections.extend(f"- {item}" for item in round_record.synthesis.key_advances)
    sections.append("")
    sections.append("## Objections Restantes")
    sections.extend(f"- {item}" for item in round_record.synthesis.open_questions)
    sections.append("")
    sections.append("## Paragraphes Reutilisables")
    sections.extend(f"- {item}" for item in round_record.synthesis.reusable_paragraphs)
    sections.append("")
    return "\n".join(sections).strip() + "\n"


def render_final_synthesis_markdown(final_synthesis, memory: MemoryState) -> str:
    objections = "\n".join(f"- {item}" for item in final_synthesis.remaining_objections)
    next_angles = "\n".join(f"- {item}" for item in final_synthesis.next_angles)
    reusable = "\n".join(f"- {item}" for item in final_synthesis.reusable_paragraphs)

    return (
        "# Synthese Finale\n\n"
        f"{final_synthesis.final_markdown}\n\n"
        "## Objections Restantes\n"
        f"{objections or '- None'}\n\n"
        "## Pistes de Prolongement\n"
        f"{next_angles or '- None'}\n\n"
        "## Paragraphes Reutilisables\n"
        f"{reusable or '- None'}\n\n"
        f"## Nombre de Manches\n{len(memory.rounds)}\n"
    )


def render_paragraphs_markdown(paragraphs: list[str]) -> str:
    blocks = ["# Paragraphes Bons Pour La These", ""]
    for index, paragraph in enumerate(paragraphs, start=1):
        blocks.append(f"## Paragraphe {index}")
        blocks.append(paragraph)
        blocks.append("")
    return "\n".join(blocks).strip() + "\n"
