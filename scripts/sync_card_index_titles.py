from __future__ import annotations

import re
from pathlib import Path


def load_titles(card_dir: Path) -> dict[str, str]:
    titles: dict[str, str] = {}
    for card in card_dir.glob("idea_*.md"):
        frontmatter = card.read_text(encoding="utf-8").split("---", 2)[1]
        card_id = re.search(r"^id:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
        title = re.search(r'^title:\s*"(.+)"\s*$', frontmatter, re.MULTILINE)
        if card_id is None or title is None:
            raise ValueError(f"Missing id or title: {card}")
        titles[card_id.group(1)] = title.group(1)
    return titles


def sync_index(path: Path, titles: dict[str, str]) -> bool:
    original = path.read_text(encoding="utf-8")

    def replacement(match: re.Match[str]) -> str:
        card_id = match.group("id")
        return f"- `{card_id}` - {titles[card_id]}."

    updated = re.sub(
        r"^- `(?P<id>idea_\d{4})` - .+$",
        replacement,
        original,
        flags=re.MULTILINE,
    )
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    titles = load_titles(project_root / "cartes" / "inbox")
    changed = [
        path
        for path in sorted((project_root / "cartes" / "indexes").glob("*.md"))
        if sync_index(path, titles)
    ]
    print(f"Synchronized {len(changed)} index file(s).")


if __name__ == "__main__":
    main()
