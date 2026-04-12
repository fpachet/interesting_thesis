from __future__ import annotations

import json
import os
import time
from collections.abc import Sequence
from typing import Any, Protocol

from .errors import ConfigurationError, MissingDependencyError, ModelResponseError
from .text_utils import excerpt, sentences, unique_preserve_order

Message = dict[str, str]


class LLMClient(Protocol):
    def generate_text(
        self,
        messages: Sequence[Message],
        *,
        max_output_tokens: int,
        reasoning_effort: str | None = None,
    ) -> str: ...

    def generate_json(
        self,
        messages: Sequence[Message],
        *,
        schema_name: str,
        schema_description: str,
        schema: dict[str, Any],
        max_output_tokens: int,
        reasoning_effort: str | None = None,
    ) -> dict[str, Any]: ...


class OpenAIResponsesClient:
    def __init__(self, model: str) -> None:
        if not os.getenv("OPENAI_API_KEY"):
            raise ConfigurationError("OPENAI_API_KEY is not set.")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise MissingDependencyError(
                "The 'openai' package is required for non-dry runs."
            ) from exc

        self.model = model
        self._client = OpenAI()

    def generate_text(
        self,
        messages: Sequence[Message],
        *,
        max_output_tokens: int,
        reasoning_effort: str | None = None,
    ) -> str:
        response = self._create_response(
            messages=messages,
            max_output_tokens=max_output_tokens,
            reasoning_effort=reasoning_effort,
        )
        return _extract_output_text(response)

    def generate_json(
        self,
        messages: Sequence[Message],
        *,
        schema_name: str,
        schema_description: str,
        schema: dict[str, Any],
        max_output_tokens: int,
        reasoning_effort: str | None = None,
    ) -> dict[str, Any]:
        response = self._create_response(
            messages=messages,
            max_output_tokens=max_output_tokens,
            reasoning_effort=reasoning_effort,
            text_format={
                "type": "json_schema",
                "name": schema_name,
                "description": schema_description,
                "strict": True,
                "schema": schema,
            },
        )
        raw_text = _extract_output_text(response)
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise ModelResponseError(
                f"Model returned invalid JSON for schema '{schema_name}'."
            ) from exc
        if not isinstance(data, dict):
            raise ModelResponseError(
                f"Model returned non-object JSON for schema '{schema_name}'."
            )
        return data

    def _create_response(
        self,
        *,
        messages: Sequence[Message],
        max_output_tokens: int,
        reasoning_effort: str | None,
        text_format: dict[str, Any] | None = None,
    ) -> Any:
        request: dict[str, Any] = {
            "model": self.model,
            "input": list(messages),
            "max_output_tokens": max_output_tokens,
        }
        if reasoning_effort:
            request["reasoning"] = {"effort": reasoning_effort}
        if text_format:
            request["text"] = {"format": text_format}

        for attempt in range(1, 4):
            try:
                response = self._client.responses.create(**request)
                status = getattr(response, "status", None)
                if status in {None, "completed"}:
                    return response
                raise ModelResponseError(f"Response status was '{status}'.")
            except Exception as exc:  # noqa: BLE001
                if attempt == 3:
                    raise ModelResponseError("OpenAI Responses API call failed.") from exc
                time.sleep(0.75 * attempt)
        raise ModelResponseError("OpenAI Responses API call failed.")


class DryRunClient:
    def __init__(self, model: str) -> None:
        self.model = model

    def generate_text(
        self,
        messages: Sequence[Message],
        *,
        max_output_tokens: int,
        reasoning_effort: str | None = None,
    ) -> str:
        del max_output_tokens, reasoning_effort
        system_text = messages[0]["content"].lower() if messages else ""
        joined = "\n\n".join(message["content"] for message in messages)
        ideas = _ideas_from_text(joined, minimum=4)

        if "constructeur" in system_text:
            return (
                "### Hypothese forte\n"
                f"{ideas[0]}\n\n"
                "### Extension argumentative\n"
                f"{ideas[1]}\n\n"
                "### Formulation reutilisable\n"
                f"{ideas[2]}"
            )
        if "critique" in system_text:
            return (
                "### Point de pression\n"
                f"{ideas[0]}\n\n"
                "### Ambiguite ou contre-exemple\n"
                f"{ideas[1]}\n\n"
                "### Distinction a stabiliser\n"
                f"{ideas[2]}"
            )
        return (
            "### Resume de travail\n"
            f"{ideas[0]}\n\n"
            "### Observations\n"
            f"- {ideas[1]}\n"
            f"- {ideas[2]}\n"
            f"- {ideas[3]}"
        )

    def generate_json(
        self,
        messages: Sequence[Message],
        *,
        schema_name: str,
        schema_description: str,
        schema: dict[str, Any],
        max_output_tokens: int,
        reasoning_effort: str | None = None,
    ) -> dict[str, Any]:
        del schema_description, schema, max_output_tokens, reasoning_effort
        joined = "\n\n".join(message["content"] for message in messages)
        ideas = _ideas_from_text(joined, minimum=8)

        if schema_name == "corpus_digest":
            return {
                "digest_markdown": (
                    "## Digest du corpus\n"
                    f"- {ideas[0]}\n"
                    f"- {ideas[1]}\n"
                    f"- {ideas[2]}"
                ),
                "key_ideas": ideas[:4],
                "tensions": ideas[4:6],
                "notable_sources": [
                    line.strip()
                    for line in joined.splitlines()
                    if line.strip().startswith("- ")
                ][:4]
                or ["Corpus personnel"],
            }

        if schema_name == "round_synthesis":
            return {
                "summary_markdown": (
                    "## Synthese de manche\n"
                    f"- Acquis principal : {ideas[0]}\n"
                    f"- Point restant : {ideas[1]}"
                ),
                "key_advances": ideas[:4],
                "open_questions": ideas[4:6],
                "reusable_paragraphs": [
                    f"{ideas[0]} {ideas[1]}",
                    f"{ideas[2]} {ideas[3]}",
                ],
            }

        if schema_name == "final_synthesis":
            return {
                "final_markdown": (
                    "## Synthese finale\n"
                    f"{ideas[0]}\n\n"
                    f"{ideas[1]}\n\n"
                    f"{ideas[2]}"
                ),
                "reusable_paragraphs": [
                    f"{ideas[0]} {ideas[1]}",
                    f"{ideas[2]} {ideas[3]}",
                    f"{ideas[4]} {ideas[5]}",
                ],
                "remaining_objections": ideas[4:6],
                "next_angles": ideas[6:8],
            }

        raise ModelResponseError(f"Unsupported dry-run schema: {schema_name}")


def _extract_output_text(response: Any) -> str:
    direct_text = getattr(response, "output_text", None)
    if isinstance(direct_text, str) and direct_text.strip():
        return direct_text.strip()

    output_items = getattr(response, "output", None)
    if output_items:
        collected: list[str] = []
        for item in output_items:
            content = getattr(item, "content", None)
            if not content:
                continue
            for part in content:
                part_type = getattr(part, "type", None)
                if part_type not in {"output_text", "text"}:
                    continue
                text = getattr(part, "text", None)
                if isinstance(text, str) and text.strip():
                    collected.append(text.strip())
        if collected:
            return "\n".join(collected).strip()

    if hasattr(response, "model_dump"):
        payload = response.model_dump()
        return _extract_output_text_from_payload(payload)

    raise ModelResponseError("Model response did not contain any text output.")


def _extract_output_text_from_payload(payload: Any) -> str:
    if not isinstance(payload, dict):
        raise ModelResponseError("Unexpected response payload shape.")
    output_items = payload.get("output", [])
    collected: list[str] = []
    for item in output_items:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if not isinstance(content, dict):
                continue
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if isinstance(text, str) and text.strip():
                    collected.append(text.strip())
    if collected:
        return "\n".join(collected).strip()
    raise ModelResponseError("Model response did not contain any text output.")


def _ideas_from_text(text: str, minimum: int) -> list[str]:
    base_sentences = unique_preserve_order(sentences(text))
    ideas = [
        sentence
        for sentence in base_sentences
        if not sentence.lower().startswith(("theme", "memoire", "sources", "sortie"))
    ]

    if len(ideas) < minimum:
        fallback = excerpt(text, max_chars=800) or "Le corpus appelle une reformulation plus stable de la these."
        while len(ideas) < minimum:
            ideas.append(fallback)

    return ideas[: max(minimum, len(ideas))]
