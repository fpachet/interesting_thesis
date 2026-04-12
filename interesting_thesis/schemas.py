from __future__ import annotations


def digest_schema() -> dict[str, object]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "digest_markdown",
            "key_ideas",
            "tensions",
            "notable_sources",
        ],
        "properties": {
            "digest_markdown": {"type": "string"},
            "key_ideas": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 3,
                "maxItems": 8,
            },
            "tensions": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 6,
            },
            "notable_sources": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 12,
            },
        },
    }


def round_synthesis_schema() -> dict[str, object]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "summary_markdown",
            "key_advances",
            "open_questions",
            "reusable_paragraphs",
        ],
        "properties": {
            "summary_markdown": {"type": "string"},
            "key_advances": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
                "maxItems": 8,
            },
            "open_questions": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 8,
            },
            "reusable_paragraphs": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 6,
            },
        },
    }


def final_synthesis_schema() -> dict[str, object]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "final_markdown",
            "reusable_paragraphs",
            "remaining_objections",
            "next_angles",
        ],
        "properties": {
            "final_markdown": {"type": "string"},
            "reusable_paragraphs": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
                "maxItems": 10,
            },
            "remaining_objections": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 8,
            },
            "next_angles": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 8,
            },
        },
    }
