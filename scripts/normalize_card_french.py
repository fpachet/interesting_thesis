from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path

from generate_card_catalog import restore_text_accents, restore_title_accents


HEADING_REPLACEMENTS = {
    "Idee": "Idée",
    "Interet pour la these": "Intérêt pour la thèse",
}


def normalize_frontmatter(frontmatter: str) -> str:
    lines = frontmatter.splitlines()
    in_source_notes = False
    normalized: list[str] = []

    for line in lines:
        if line.startswith("title: "):
            prefix, value = line.split(": ", 1)
            quote = '"' if value.startswith('"') and value.endswith('"') else ""
            title = value[1:-1] if quote else value
            normalized.append(f"{prefix}: {quote}{restore_title_accents(title)}{quote}")
            in_source_notes = False
            continue

        if line == "source_notes:":
            in_source_notes = True
            normalized.append(line)
            continue

        if in_source_notes and re.match(r"^[A-Za-z_]+:", line):
            in_source_notes = False

        if in_source_notes and line.startswith('  - "') and line.endswith('"'):
            normalized.append('  - "' + restore_text_accents(line[5:-1]) + '"')
        else:
            normalized.append(line)

    return "\n".join(normalized)


def wrap_paragraph(text: str) -> str:
    return textwrap.fill(
        restore_text_accents(" ".join(text.splitlines())),
        width=88,
        break_long_words=False,
        break_on_hyphens=False,
    )


def normalize_body(body: str) -> str:
    blocks = re.split(r"\n\s*\n", body.strip())
    normalized: list[str] = []

    for block in blocks:
        if block.startswith("## ") and "\n" not in block:
            heading = block[3:]
            normalized.append("## " + HEADING_REPLACEMENTS.get(heading, heading))
            continue

        if all(not line or line.startswith("- ") for line in block.splitlines()):
            normalized.append(
                "\n".join(
                    "- " + restore_text_accents(line[2:]) if line.startswith("- ") else line
                    for line in block.splitlines()
                )
            )
            continue

        normalized.append(wrap_paragraph(block))

    return "\n\n".join(normalized) + "\n"


def normalize_card(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    parts = original.split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Invalid frontmatter: {path}")
    updated = (
        "---\n"
        + normalize_frontmatter(parts[1]).strip()
        + "\n---\n"
        + normalize_body(parts[2])
    )
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Restore French accents in card sources")
    parser.add_argument("--check", action="store_true", help="Report cards that need changes")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    card_dir = project_root / "cartes" / "inbox"
    changed: list[Path] = []

    for path in sorted(card_dir.glob("idea_*.md")):
        if args.check:
            original = path.read_text(encoding="utf-8")
            parts = original.split("---", 2)
            updated = (
                "---\n"
                + normalize_frontmatter(parts[1]).strip()
                + "\n---\n"
                + normalize_body(parts[2])
            )
            if updated != original:
                changed.append(path)
        elif normalize_card(path):
            changed.append(path)

    action = "need normalization" if args.check else "normalized"
    print(f"{len(changed)} card(s) {action}.")
    if args.check:
        for path in changed:
            print(path.relative_to(project_root))


if __name__ == "__main__":
    main()
