from __future__ import annotations

import json
import runpy
import subprocess
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


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

    assert manifest["cards"] == 161
    assert manifest["families"] == 8
    assert manifest["relations"] == 278
    assert manifest["references"] == 139
    assert manifest["referenced_cards"] == 96
    assert manifest["public_documents"] > 0
    assert len(list((output / "cartes").glob("idea_*/index.html"))) == 161
    assert len(list((output / "bibliographie").glob("*/index.html"))) == 139

    homepage = (output / "index.html").read_text(encoding="utf-8")
    assert "version 12" in homepage
    assert "Thèse centrale actuelle" in homepage
    assert "Est intéressant, pour un sujet, ce qui déclenche" in homepage
    assert "161 propositions" in homepage
    assert (output / "these" / "index.html").is_file()
    assert (output / "lectures" / "index.html").is_file()
    assert (output / "graphe" / "index.html").is_file()
    assert (output / "suivi" / "index.html").is_file()
    assert (output / "bibliographie" / "index.html").is_file()
    assert (output / "cartes" / "idea_0127" / "index.html").is_file()
    assert (output / "cartes" / "idea_0128" / "index.html").is_file()
    assert (output / "cartes" / "idea_0133" / "index.html").is_file()
    assert (output / "cartes" / "idea_0134" / "index.html").is_file()
    assert (output / "cartes" / "idea_0138" / "index.html").is_file()
    assert (output / "cartes" / "idea_0164" / "index.html").is_file()

    thesis_page = (output / "these" / "index.html").read_text(encoding="utf-8")
    assert "Test pédagogique" in thesis_page
    assert "../cartes/idea_0164/index.html" in thesis_page
    assert (output / "cartes" / "idea_0139" / "index.html").is_file()
    assert (output / "cartes" / "idea_0162" / "index.html").is_file()
    assert (output / "cartes" / "idea_0163" / "index.html").is_file()
    assert (output / "bibliographie" / "russell1995awardlecture" / "index.html").is_file()

    thesis_page = (output / "these" / "index.html").read_text(encoding="utf-8")
    assert "Trois mouvements provisoires" in thesis_page
    assert "Constituer l&#x27;angle mort" in thesis_page
    assert "discussion avec Olivia Chevallier" in thesis_page
    assert "Le terme décisif est <em>construction</em>" in thesis_page
    assert "<em>L'intérescence</em> est le nom proposé" in thesis_page
    assert "Christian Berner" in thesis_page
    assert "éditions Vrin" in thesis_page
    assert "motivation morale et affective extrêmement forte" in thesis_page
    assert "sans intérescence interne identifiable" in thesis_page

    status_page = (output / "suivi" / "index.html").read_text(encoding="utf-8")
    assert "Version 12" in status_page
    assert "8 familles de travail" in status_page

    job_card = (output / "cartes" / "idea_0162" / "index.html").read_text(
        encoding="utf-8"
    )
    assert "motivation sans intérescence interne identifiable" in job_card
    assert "L'intense intérescence du lecteur" in job_card

    reading_page = (output / "lectures" / "index.html").read_text(encoding="utf-8")
    assert "Parcours exécutable en dix séances" in reading_page
    assert "Christian Garve" in reading_page
    assert "Friedrich Schlegel" in reading_page
    assert "Bibliothèque numérique prioritaire" in reading_page
    assert "<table>" in reading_page
    assert "../docs/lectures/passages-interessant-etat-art.md" in reading_page
    assert "https://textgridrep.de/browse/v35f.0?lang=de" in reading_page
    assert "https://play.google.com/store/books/details?id=7nMQky4ClX8C" in reading_page

    card_catalog = (output / "cartes" / "index.html").read_text(encoding="utf-8")
    assert "koestler, arthur (1989). the act of creation" in card_catalog
    search_script = (output / "assets" / "app.js").read_text(encoding="utf-8")
    assert "hasAtMostOneEdit" in search_script


def test_bibliography_links_cards_references_and_documents(tmp_path: Path) -> None:
    output = generate_site(tmp_path)

    card = (output / "cartes" / "idea_0084" / "index.html").read_text(encoding="utf-8")
    reference = (
        output / "bibliographie" / "pachet2018oreille" / "index.html"
    ).read_text(encoding="utf-8")

    assert "../../bibliographie/pachet2018oreille/index.html" in card
    assert "../../documents/input/PACHET_HISTOIRE_OREILLE_BAT.pdf" in card
    accented_source = unicodedata.normalize("NFC", "input/projet thèse philo.pdf")
    assert f"../../documents/{quote(accented_source, safe='/')}" in card
    assert "../../cartes/idea_0084/index.html" in reference
    assert "Histoire d&#x27;une oreille" in reference
    assert (output / "documents" / "input" / "PACHET_HISTOIRE_OREILLE_BAT.pdf").is_file()
    assert (output / "documents" / accented_source).is_file()


def test_missing_local_document_uses_bibliography_url(tmp_path: Path) -> None:
    generator = runpy.run_path(ROOT / "scripts" / "generate_thesis_site.py")
    entry_class = generator["BibliographyEntry"]
    source = "input/publications-francois-pachet/example.pdf"
    public_url = "https://www.francoispachet.fr/publications/example.pdf"
    bibliography = {
        "example": entry_class(
            key="example",
            entry_type="article",
            fields={"title": "Example", "file": source, "url": public_url},
            raw="",
        )
    }
    generator["document_access"].__globals__["ROOT"] = tmp_path

    access_url, external = generator["document_access"](
        source, "../../", bibliography
    )
    rendered_link = generator["source_link"](source, "../../", bibliography)

    assert access_url == public_url
    assert external is True
    assert f'href="{public_url}"' in rendered_link
    assert "Consulter en ligne" in rendered_link


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
