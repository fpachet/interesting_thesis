from __future__ import annotations

import json
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"a", "link"} and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "script" and values.get("src"):
            self.links.append(values["src"] or "")


def generate_site(tmp_path: Path) -> Path:
    output = tmp_path / "site"
    subprocess.run(
        [sys.executable, "scripts/generate_thesis_site.py", "--output", str(output)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return output


def test_site_contains_all_cards_and_core_views(tmp_path: Path) -> None:
    output = generate_site(tmp_path)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["cards"] == 121
    assert manifest["families"] == 7
    assert manifest["relations"] == 112
    assert len(list((output / "cartes").glob("idea_*/index.html"))) == 121

    homepage = (output / "index.html").read_text(encoding="utf-8")
    assert "Thèse centrale actuelle" in homepage
    assert "L&#x27;intéressant est ce qui déclenche et soutient une construction" in homepage
    assert (output / "these" / "index.html").is_file()
    assert (output / "graphe" / "index.html").is_file()
    assert (output / "suivi" / "index.html").is_file()


def test_generated_internal_links_resolve(tmp_path: Path) -> None:
    output = generate_site(tmp_path)
    broken: list[tuple[Path, str]] = []

    for page in output.rglob("*.html"):
        collector = LinkCollector()
        collector.feed(page.read_text(encoding="utf-8"))
        for link in collector.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (page.parent / unquote(parsed.path)).resolve()
            if not target.is_file():
                broken.append((page.relative_to(output), link))

    assert broken == []
