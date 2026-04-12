from __future__ import annotations

import re
from collections.abc import Iterable


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def count_words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def split_text(text: str, max_chars: int) -> list[str]:
    normalized = normalize_text(text)
    if len(normalized) <= max_chars:
        return [normalized] if normalized else []

    paragraphs = [paragraph.strip() for paragraph in normalized.split("\n\n") if paragraph.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_size = 0

    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if current:
                chunks.append("\n\n".join(current))
                current = []
                current_size = 0
            for start in range(0, len(paragraph), max_chars):
                chunks.append(paragraph[start : start + max_chars].strip())
            continue

        extra = len(paragraph) + (2 if current else 0)
        if current and current_size + extra > max_chars:
            chunks.append("\n\n".join(current))
            current = [paragraph]
            current_size = len(paragraph)
            continue

        current.append(paragraph)
        current_size += extra

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def unique_preserve_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def excerpt(text: str, max_chars: int = 600) -> str:
    normalized = normalize_text(text)
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max_chars - 3].rstrip() + "..."


def sentences(text: str) -> list[str]:
    normalized = normalize_text(text)
    raw_parts = re.split(r"(?<=[.!?])\s+|\n+", normalized)
    cleaned = [part.strip(" -\t") for part in raw_parts if len(part.strip()) > 20]
    return cleaned
