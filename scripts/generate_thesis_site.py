from __future__ import annotations

import argparse
import html
import json
import math
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
CARDS_DIR = ROOT / "cartes" / "inbox"
SITE_SOURCE = ROOT / "site"
DEFAULT_OUTPUT = SITE_SOURCE / "dist"
BIBLIOGRAPHY_PATH = ROOT / "bibliographie" / "references.bib"

BIBLIOGRAPHY_TYPE_LABELS = {
    "article": "Article",
    "book": "Livre",
    "incollection": "Chapitre",
    "inproceedings": "Communication",
    "misc": "Ressource en ligne",
    "phdthesis": "Thèse",
    "techreport": "Rapport",
    "unpublished": "Manuscrit",
}

BIBLIOGRAPHY_FIELD_LABELS = {
    "author": "Auteur·rices",
    "editor": "Direction",
    "translator": "Traduction",
    "title": "Titre",
    "journal": "Revue",
    "booktitle": "Ouvrage ou actes",
    "institution": "Institution",
    "school": "Établissement",
    "publisher": "Éditeur",
    "address": "Lieu",
    "series": "Collection",
    "volume": "Volume",
    "number": "Numéro",
    "chapter": "Chapitre",
    "pages": "Pages",
    "year": "Année",
    "month": "Mois",
    "type": "Type",
    "note": "Note",
    "doi": "DOI",
    "isbn": "ISBN",
    "issn": "ISSN",
    "url": "URL",
    "howpublished": "Publication",
    "file": "Document local",
}

MONTH_NAMES = {
    "jan": "janvier",
    "feb": "février",
    "mar": "mars",
    "apr": "avril",
    "may": "mai",
    "jun": "juin",
    "jul": "juillet",
    "aug": "août",
    "sep": "septembre",
    "oct": "octobre",
    "nov": "novembre",
    "dec": "décembre",
}

RELATION_LABELS = {
    "supports": "soutient",
    "motivates": "motive",
    "specifies": "précise",
    "bridges": "relie",
    "operationalizes": "opérationnalise",
    "illustrates": "illustre",
    "limits": "limite",
    "objects_to": "objecte à",
    "contrasts_with": "contraste avec",
}

LEVEL_LABELS = {
    "conceptual": "Conceptuelle",
    "scientific": "Scientifique",
    "articulation": "Articulation",
}

KIND_LABELS = {
    "definition": "Définition",
    "argument": "Argument",
    "objection": "Objection",
    "example": "Exemple",
    "distinction": "Distinction",
    "method": "Méthode",
    "question": "Question",
    "hypothesis": "Hypothèse",
    "bibliographic_note": "Note bibliographique",
}


@dataclass
class Card:
    id: str
    title: str
    kind: str
    level: str
    status: str
    sources: list[str]
    references: list[str]
    source_notes: list[str]
    tags: list[str]
    body: str
    path: Path
    family: str = "Sans famille"
    family_index: int = -1
    argument_role: str = ""
    themes: list[str] = field(default_factory=list)


@dataclass
class Relation:
    source: str
    kind: str
    target: str
    explanation: str


@dataclass
class BibliographyEntry:
    key: str
    entry_type: str
    fields: dict[str, str]
    raw: str

    @property
    def title(self) -> str:
        return self.fields.get("title", self.key)

    @property
    def year(self) -> str:
        return self.fields.get("year", "s. d.")

    @property
    def contributors(self) -> str:
        return self.fields.get("author") or self.fields.get("editor", "Auteur inconnu")

    @property
    def sort_key(self) -> tuple[str, str, str]:
        return (self.contributors.casefold(), self.year, self.title.casefold())


def parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str, path: Path) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise ValueError(f"En-tête YAML absent : {path}")
    try:
        _, raw, body = text.split("---", 2)
    except ValueError as exc:
        raise ValueError(f"En-tête YAML incomplet : {path}") from exc

    metadata: dict[str, object] = {}
    active_list: str | None = None
    for line in raw.strip().splitlines():
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and active_list:
            values = metadata.setdefault(active_list, [])
            assert isinstance(values, list)
            values.append(parse_scalar(item.group(1)))
            continue
        key_value = re.match(r"^([a-z_]+):(?:\s+(.*))?$", line)
        if not key_value:
            continue
        key, value = key_value.groups()
        if value is None or not value.strip():
            metadata[key] = []
            active_list = key
        else:
            metadata[key] = parse_scalar(value)
            active_list = None
    return metadata, body.strip()


def latex_to_text(value: str) -> str:
    accents = {
        ("'", "a"): "á", ("'", "e"): "é", ("'", "i"): "í", ("'", "o"): "ó", ("'", "u"): "ú",
        ("'", "A"): "Á", ("'", "E"): "É", ("'", "I"): "Í", ("'", "O"): "Ó", ("'", "U"): "Ú",
        ("`", "a"): "à", ("`", "e"): "è", ("`", "i"): "ì", ("`", "o"): "ò", ("`", "u"): "ù",
        ("`", "A"): "À", ("`", "E"): "È", ("`", "I"): "Ì", ("`", "O"): "Ò", ("`", "U"): "Ù",
        ("^", "a"): "â", ("^", "e"): "ê", ("^", "i"): "î", ("^", "o"): "ô", ("^", "u"): "û",
        ("^", "A"): "Â", ("^", "E"): "Ê", ("^", "I"): "Î", ("^", "O"): "Ô", ("^", "U"): "Û",
        ('"', "a"): "ä", ('"', "e"): "ë", ('"', "i"): "ï", ('"', "o"): "ö", ('"', "u"): "ü",
        ('"', "A"): "Ä", ('"', "E"): "Ë", ('"', "I"): "Ï", ('"', "O"): "Ö", ('"', "U"): "Ü",
        ("~", "a"): "ã", ("~", "n"): "ñ", ("~", "o"): "õ",
        ("~", "A"): "Ã", ("~", "N"): "Ñ", ("~", "O"): "Õ",
        ("c", "c"): "ç", ("c", "C"): "Ç",
    }

    def replace_accent(match: re.Match[str]) -> str:
        command, letter = match.groups()
        return accents.get((command, letter), letter)

    value = re.sub(r"\{\\([\"'`^~c])\{?([A-Za-z])\}?\}", replace_accent, value)
    value = re.sub(r"\\([\"'`^~c])\{?([A-Za-z])\}?", replace_accent, value)
    value = value.replace(r"\&", "&").replace(r"\%", "%").replace(r"\_", "_")
    value = value.replace("--", "–").replace("~", " ")
    return value.replace("{", "").replace("}", "").strip()


def parse_bibtex_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    position = body.find(",") + 1
    while position > 0 and position < len(body):
        while position < len(body) and (body[position].isspace() or body[position] == ","):
            position += 1
        field_match = re.match(r"([A-Za-z][A-Za-z0-9_-]*)\s*=\s*", body[position:])
        if not field_match:
            break
        name = field_match.group(1).lower()
        position += field_match.end()
        if position >= len(body):
            break

        if body[position] == "{":
            start = position + 1
            depth = 1
            position += 1
            while position < len(body) and depth:
                if body[position] == "{" and (position == 0 or body[position - 1] != "\\"):
                    depth += 1
                elif body[position] == "}" and (position == 0 or body[position - 1] != "\\"):
                    depth -= 1
                position += 1
            raw_value = body[start:position - 1]
        elif body[position] == '"':
            start = position + 1
            position += 1
            while position < len(body):
                if body[position] == '"' and body[position - 1] != "\\":
                    break
                position += 1
            raw_value = body[start:position]
            position += 1
        else:
            start = position
            while position < len(body) and body[position] not in ",\n":
                position += 1
            raw_value = body[start:position].strip()

        fields[name] = MONTH_NAMES.get(raw_value, latex_to_text(raw_value))
    return fields


def load_bibliography() -> dict[str, BibliographyEntry]:
    text = BIBLIOGRAPHY_PATH.read_text(encoding="utf-8")
    entries: dict[str, BibliographyEntry] = {}
    for match in re.finditer(r"@(\w+)\s*\{", text):
        entry_type = match.group(1).lower()
        start = match.start()
        body_start = match.end()
        position = body_start
        depth = 1
        while position < len(text) and depth:
            if text[position] == "{" and text[position - 1] != "\\":
                depth += 1
            elif text[position] == "}" and text[position - 1] != "\\":
                depth -= 1
            position += 1
        if depth:
            raise ValueError(f"Entrée BibTeX incomplète à partir du caractère {start}")
        body = text[body_start:position - 1]
        key = body.split(",", 1)[0].strip()
        if not key:
            raise ValueError(f"Clé BibTeX absente à partir du caractère {start}")
        if key in entries:
            raise ValueError(f"Clé BibTeX dupliquée : {key}")
        entries[key] = BibliographyEntry(
            key=key,
            entry_type=entry_type,
            fields=parse_bibtex_fields(body),
            raw=text[start:position].strip(),
        )
    return entries


def load_cards() -> dict[str, Card]:
    cards: dict[str, Card] = {}
    for path in sorted(CARDS_DIR.glob("idea_*.md")):
        metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        card = Card(
            id=str(metadata["id"]),
            title=str(metadata["title"]),
            kind=str(metadata["kind"]),
            level=str(metadata["level"]),
            status=str(metadata["status"]),
            sources=list(metadata.get("sources", [])),
            references=list(metadata.get("references", [])),
            source_notes=list(metadata.get("source_notes", [])),
            tags=list(metadata.get("tags", [])),
            body=body,
            path=path,
        )
        if card.id in cards:
            raise ValueError(f"Identifiant dupliqué : {card.id}")
        cards[card.id] = card
    return cards


def load_families(cards: dict[str, Card]) -> list[tuple[str, list[str]]]:
    path = ROOT / "cartes" / "indexes" / "by_argument.md"
    families: list[tuple[str, list[str]]] = []
    current_name = ""
    current_ids: list[str] | None = None
    current_role = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        family = re.match(r"^## \d+\. (.+?) \(\d+\)$", line)
        if family:
            current_name = family.group(1)
            current_ids = []
            families.append((current_name, current_ids))
            current_role = ""
            continue
        role = re.match(r"^### (.+)$", line)
        if role and current_ids is not None:
            current_role = role.group(1)
            continue
        entry = re.match(r"^- `(idea_\d{4})` - ", line)
        if entry and current_ids is not None:
            card_id = entry.group(1)
            if card_id not in cards:
                raise ValueError(f"Carte inconnue dans l'index argumentatif : {card_id}")
            current_ids.append(card_id)
            cards[card_id].family = current_name
            cards[card_id].family_index = len(families) - 1
            cards[card_id].argument_role = current_role
    indexed = [card_id for _, ids in families for card_id in ids]
    if len(indexed) != len(cards) or set(indexed) != set(cards):
        raise ValueError("L'index argumentatif doit contenir chaque carte exactement une fois")
    return families


def load_themes(cards: dict[str, Card]) -> list[str]:
    path = ROOT / "cartes" / "indexes" / "by_theme.md"
    current = ""
    themes: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^## (.+)$", line)
        if heading:
            current = heading.group(1)
            themes.append(current)
            continue
        entry = re.match(r"^- `(idea_\d{4})` - ", line)
        if entry and current and entry.group(1) in cards:
            cards[entry.group(1)].themes.append(current)
    return themes


def load_relations(cards: dict[str, Card]) -> list[Relation]:
    path = ROOT / "cartes" / "relations.tsv"
    relations: list[Relation] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        source, kind, target, explanation = line.split("\t", 3)
        if source not in cards or target not in cards:
            raise ValueError(f"Relation vers une carte inconnue : {line}")
        relations.append(Relation(source, kind, target, explanation))
    return relations


def section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group("body").strip() if match else ""


def first_paragraph(text: str) -> str:
    return re.split(r"\n\s*\n", text.strip(), maxsplit=1)[0].replace("\n", " ")


def extract_bullets(text: str) -> list[str]:
    items: list[str] = []
    current = ""
    for line in text.splitlines():
        if line.startswith("- "):
            if current:
                items.append(current.strip())
            current = line[2:].strip()
        elif current and line.startswith("  "):
            current += " " + line.strip()
        elif current:
            items.append(current.strip())
            current = ""
    if current:
        items.append(current.strip())
    return items


def inline_markdown(value: str) -> str:
    escaped = html.escape(value, quote=False)
    code_values: list[str] = []

    def save_code(match: re.Match[str]) -> str:
        code_values.append(f"<code>{match.group(1)}</code>")
        return f"\x00CODE{len(code_values) - 1}\x00"

    escaped = re.sub(r"`([^`]+)`", save_code, escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: f'<a href="{html.escape(match.group(2), quote=True)}">{match.group(1)}</a>',
        escaped,
    )
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    for index, code in enumerate(code_values):
        escaped = escaped.replace(f"\x00CODE{index}\x00", code)
    return escaped


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(part.strip() for part in paragraph))}</p>")
            paragraph.clear()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            index += 1
            continue
        if stripped.startswith("```"):
            flush_paragraph()
            language = stripped[3:].strip()
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            output.append(
                f'<pre data-language="{html.escape(language)}"><code>{html.escape(chr(10).join(code_lines))}</code></pre>'
            )
            index += 1
            continue
        heading = re.match(r"^(#{2,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            index += 1
            continue
        if stripped.startswith("> "):
            flush_paragraph()
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip().lstrip("> "))
                index += 1
            output.append(f"<blockquote>{inline_markdown(' '.join(quote_lines))}</blockquote>")
            continue
        if re.match(r"^- ", stripped):
            flush_paragraph()
            items: list[str] = []
            while index < len(lines) and re.match(r"^\s*- ", lines[index]):
                item = re.sub(r"^\s*- ", "", lines[index]).strip()
                index += 1
                while index < len(lines) and lines[index].startswith("  ") and lines[index].strip():
                    item += " " + lines[index].strip()
                    index += 1
                items.append(item)
            output.append("<ul>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in items) + "</ul>")
            continue
        if re.match(r"^\d+\. ", stripped):
            flush_paragraph()
            items = []
            while index < len(lines) and re.match(r"^\s*\d+\. ", lines[index]):
                item = re.sub(r"^\s*\d+\. ", "", lines[index]).strip()
                index += 1
                while index < len(lines) and lines[index].startswith("  ") and lines[index].strip():
                    item += " " + lines[index].strip()
                    index += 1
                items.append(item)
            output.append("<ol>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in items) + "</ol>")
            continue
        paragraph.append(line)
        index += 1
    flush_paragraph()
    return "\n".join(output)


def card_href(card_id: str, prefix: str) -> str:
    return f"{prefix}cartes/{card_id}/index.html"


def bibliography_href(reference_key: str, prefix: str) -> str:
    return f"{prefix}bibliographie/{quote(reference_key)}/index.html"


def document_href(source: str, prefix: str) -> str:
    return f"{prefix}documents/{quote(source, safe='/')}"


def format_people(value: str, *, shortened: bool = False) -> str:
    people = [person.strip() for person in re.split(r"\s+and\s+", value) if person.strip()]
    if shortened and len(people) > 2:
        return f"{people[0]} et al."
    if len(people) < 2:
        return people[0] if people else "Auteur inconnu"
    return ", ".join(people[:-1]) + " et " + people[-1]


def short_reference(entry: BibliographyEntry) -> str:
    people = format_people(entry.contributors, shortened=True)
    return f"{people} ({entry.year}). {entry.title}"


def format_reference(entry: BibliographyEntry) -> str:
    fields = entry.fields
    contributors = format_people(entry.contributors).rstrip(".")
    if "author" not in fields and "editor" in fields:
        contributors += " (dir.)"
    parts = [f"<span class=\"reference-authors\">{html.escape(contributors)}</span>"]
    parts.append(f"<span class=\"reference-year\">({html.escape(entry.year)})</span>")

    if entry.entry_type == "book":
        parts.append(f"<em>{html.escape(entry.title)}</em>")
    else:
        parts.append(f"« {html.escape(entry.title)} »")

    container = fields.get("journal") or fields.get("booktitle")
    if container:
        parts.append(f"<em>{html.escape(container)}</em>")
    if fields.get("editor") and fields.get("author") and fields.get("booktitle"):
        parts.append(f"dir. {html.escape(format_people(fields['editor']))}")

    publication = []
    if fields.get("address"):
        publication.append(fields["address"])
    if fields.get("publisher"):
        publication.append(fields["publisher"])
    if fields.get("institution"):
        publication.append(fields["institution"])
    if fields.get("school"):
        publication.append(fields["school"])
    if publication:
        parts.append(" : ".join(html.escape(item) for item in publication))

    issue = ""
    if fields.get("volume"):
        issue = f"vol. {html.escape(fields['volume'])}"
    if fields.get("number"):
        issue += f"{', ' if issue else ''}nº {html.escape(fields['number'])}"
    if issue:
        parts.append(issue)
    if fields.get("chapter"):
        parts.append(f"chap. {html.escape(fields['chapter'])}")
    if fields.get("pages"):
        parts.append(f"p. {html.escape(fields['pages'])}")
    if fields.get("series"):
        parts.append(f"coll. {html.escape(fields['series'])}")
    if fields.get("note"):
        parts.append(html.escape(fields["note"]))
    return ". ".join(part.rstrip(".") for part in parts if part) + "."


def source_link(source: str, prefix: str) -> str:
    name = Path(source).name
    return f"""<a class="source-link" href="{document_href(source, prefix)}">
      <strong>{html.escape(name)}</strong><small>{html.escape(source)}</small><span>Consulter le document →</span>
    </a>"""


def badge(value: str, variant: str = "") -> str:
    class_name = "badge" + (f" badge--{variant}" if variant else "")
    return f'<span class="{class_name}">{html.escape(value)}</span>'


def base_page(
    *,
    title: str,
    description: str,
    content: str,
    prefix: str,
    active: str,
    extra_script: str = "",
) -> str:
    nav_items = [
        ("accueil", "Vue d'ensemble", "index.html"),
        ("these", "La thèse", "these/index.html"),
        ("cartes", "Les cartes", "cartes/index.html"),
        ("bibliographie", "Bibliographie", "bibliographie/index.html"),
        ("graphe", "Le graphe", "graphe/index.html"),
        ("suivi", "Suivi", "suivi/index.html"),
    ]
    nav = "".join(
        f'<a class="site-nav__link{" is-active" if key == active else ""}" href="{prefix}{href}">{label}</a>'
        for key, label, href in nav_items
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(description, quote=True)}">
  <title>{html.escape(title)} · L'émergence de l'intéressant</title>
  <link rel="stylesheet" href="{prefix}assets/styles.css">
  <script defer src="{prefix}assets/app.js"></script>
  {extra_script}
</head>
<body>
  <a class="skip-link" href="#contenu">Aller au contenu</a>
  <header class="site-header">
    <div class="shell site-header__inner">
      <a class="brand" href="{prefix}index.html" aria-label="Accueil">
        <span class="brand__mark" aria-hidden="true">I</span>
        <span><strong>L'émergence</strong><small>de l'intéressant</small></span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav class="site-nav" id="site-nav" aria-label="Navigation principale">{nav}</nav>
    </div>
  </header>
  <main id="contenu">{content}</main>
  <footer class="site-footer">
    <div class="shell site-footer__inner">
      <p><strong>L'émergence de l'intéressant</strong><br>Atelier documentaire d'un projet de thèse en philosophie.</p>
      <p class="site-footer__links"><a href="{prefix}suivi/index.html">État du projet</a><a href="{prefix}cartes/index.html">121 propositions</a></p>
    </div>
  </footer>
</body>
</html>
"""


def thesis_statement() -> str:
    text = (ROOT / "projet-these" / "BUT_DE_LA_THESE.md").read_text(encoding="utf-8")
    central = section(text, "Hypothèse centrale : l'intéressant comme déclencheur de construction")
    match = re.search(r"\*\*([^*]+)\*\*", central, re.DOTALL)
    if not match:
        raise ValueError("Impossible d'extraire la thèse centrale")
    statement = re.sub(r"\s+", " ", match.group(1)).strip()
    return statement[:1].upper() + statement[1:]


def direct_question() -> str:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    match = re.search(r"La question directrice est : \*\*(.+?)\*\*", text, re.DOTALL)
    if not match:
        raise ValueError("Impossible d'extraire la question directrice")
    return re.sub(r"\s+", " ", match.group(1))


def open_questions() -> list[str]:
    text = (ROOT / "cartes" / "ORGANISATION.md").read_text(encoding="utf-8")
    return extract_bullets(section(text, "Questions ouvertes"))


def git_metadata() -> tuple[str, list[tuple[str, str, str]]]:
    try:
        last_date = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs"], cwd=ROOT, text=True
        ).strip()
        raw = subprocess.check_output(
            ["git", "log", "-6", "--format=%h%x09%cs%x09%s"], cwd=ROOT, text=True
        )
        changes = [tuple(line.split("\t", 2)) for line in raw.splitlines()]
        return last_date, changes
    except (OSError, subprocess.CalledProcessError):
        return "", []


def registry_stats() -> tuple[int, Counter[str]]:
    path = ROOT / "cartes" / "REGISTRE_TRAITEMENT.md"
    statuses: Counter[str] = Counter()
    total = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `input/"):
            continue
        columns = [column.strip().strip("`") for column in line.strip("|").split("|")]
        if len(columns) < 2:
            continue
        total += 1
        statuses[columns[1]] += 1
    return total, statuses


def home_page(
    cards: dict[str, Card],
    families: list[tuple[str, list[str]]],
    relations: list[Relation],
    statement: str,
    question: str,
    questions: list[str],
    last_date: str,
) -> str:
    central_steps = [
        ("01", "La rencontre", "Une forme rencontre un sujet façonné par sa mémoire et son histoire.", "idea_0084"),
        ("02", "La zone féconde", "La difficulté reste assez accessible pour permettre une construction.", "idea_0121"),
        ("03", "Le travail", "Le sujet compare, anticipe, catégorise ou reconstruit un problème.", "idea_0123"),
        ("04", "La prise nouvelle", "Une distinction, un modèle ou une capacité nouvelle devient contrôlable.", "idea_0071"),
    ]
    steps_html = "".join(
        f"""<a class="thesis-step" href="{card_href(card_id, '')}">
          <span class="thesis-step__number">{number}</span>
          <strong>{title}</strong><span>{description}</span>
        </a>"""
        for number, title, description, card_id in central_steps
    )
    family_html = "".join(
        f"""<a class="family-row family-{index}" href="cartes/index.html?famille={html.escape(name, quote=True)}">
          <span class="family-row__mark" aria-hidden="true"></span>
          <span class="family-row__body"><strong>{html.escape(name)}</strong><small>{len(ids)} propositions</small></span>
          <span class="family-row__arrow" aria-hidden="true">↗</span>
        </a>"""
        for index, (name, ids) in enumerate(families)
    )
    questions_html = "".join(
        f'<li><span>{index:02d}</span><p>{inline_markdown(item)}</p></li>'
        for index, item in enumerate(questions[:4], 1)
    )
    level_counts = Counter(card.level for card in cards.values())
    formatted_date = ""
    if last_date:
        formatted_date = datetime.strptime(last_date, "%Y-%m-%d").strftime("%d.%m.%Y")

    content = f"""
<section class="hero hero--home">
  <div class="shell hero__grid">
    <div class="hero__copy">
      <p class="eyebrow">Projet de thèse en philosophie · version 2</p>
      <h1>L'émergence<br><em>de l'intéressant</em></h1>
      <p class="hero__lead">Naissance des idées, compréhension et singularité des formes.</p>
      <p class="hero__question"><span>Question directrice</span>{html.escape(question)}</p>
      <div class="button-row"><a class="button button--primary" href="these/index.html">Comprendre la thèse</a><a class="button" href="suivi/index.html">Voir son avancement</a></div>
    </div>
    <aside class="hero__aside" aria-label="État du corpus">
      <p class="hero__aside-label">Atelier vivant</p>
      <div class="hero__metrics">
        <div><strong>{len(cards)}</strong><span>propositions</span></div>
        <div><strong>{len(relations)}</strong><span>relations fortes</span></div>
        <div><strong>{len(families)}</strong><span>familles</span></div>
      </div>
      <div class="level-bar" aria-label="Répartition par niveau">
        <span class="level-bar__conceptual" style="--size:{level_counts['conceptual']}"></span>
        <span class="level-bar__scientific" style="--size:{level_counts['scientific']}"></span>
        <span class="level-bar__articulation" style="--size:{level_counts['articulation']}"></span>
      </div>
      <p class="hero__updated">Dernière évolution du dépôt · {formatted_date or 'date indisponible'}</p>
    </aside>
  </div>
</section>

<section class="section thesis-feature">
  <div class="shell">
    <div class="section-heading section-heading--split">
      <div><p class="eyebrow">Thèse centrale actuelle</p><h2>Une proposition à défendre,<br>pas un résultat déjà acquis.</h2></div>
      <p>Le site organise les arguments autour de cette formulation tout en gardant visibles ses limites, objections et transformations possibles.</p>
    </div>
    <blockquote class="central-statement">{html.escape(statement)}</blockquote>
    <div class="thesis-steps">{steps_html}</div>
    <div class="thesis-limits"><span>Deux issues à surveiller</span><a href="{card_href('idea_0122', '')}">L'épuisement vers l'ennui ou l'anxiété</a><a href="{card_href('idea_0124', '')}">La fascination sans compréhension vérifiable</a></div>
  </div>
</section>

<section class="section section--ink">
  <div class="shell two-column">
    <div>
      <p class="eyebrow eyebrow--light">Architecture argumentative</p>
      <h2>Sept familles, aucune boîte définitive.</h2>
      <p class="section-intro">Les familles donnent une orientation au lecteur. Elles restent réversibles et ne constituent pas encore le plan de la thèse.</p>
      <a class="text-link text-link--light" href="graphe/index.html">Explorer les relations entre les cartes <span>→</span></a>
    </div>
    <div class="family-list">{family_html}</div>
  </div>
</section>

<section class="section">
  <div class="shell two-column two-column--questions">
    <div>
      <p class="eyebrow">Travail en cours</p>
      <h2>Les questions restent visibles.</h2>
      <p class="section-intro">Un suivi de thèse utile ne montre pas seulement ce qui est écrit. Il rend également lisibles les tensions qui orientent la prochaine étape.</p>
      <a class="button" href="suivi/index.html">Consulter le tableau de suivi</a>
    </div>
    <ol class="open-questions">{questions_html}</ol>
  </div>
</section>

<section class="section section--compact">
  <div class="shell invitation">
    <div><p class="eyebrow">Entrer dans l'atelier</p><h2>Une carte = une proposition contestable.</h2></div>
    <p>Rechercher un concept, suivre une relation ou parcourir une famille argumentative.</p>
    <a class="button button--primary" href="cartes/index.html">Parcourir les {len(cards)} cartes</a>
  </div>
</section>
"""
    return base_page(
        title="Vue d'ensemble",
        description="Suivre l'avancement et l'architecture argumentative d'une thèse sur l'émergence de l'intéressant.",
        content=content,
        prefix="",
        active="accueil",
    )


def thesis_page(cards: dict[str, Card], statement: str, question: str) -> str:
    roles = [
        ("Cadre relationnel", "idea_0084", "Une forme, un sujet, une mémoire et un horizon historique."),
        ("Condition", "idea_0121", "Une zone de difficulté où une construction demeure possible."),
        ("Mécanisme", "idea_0123", "Un travail perceptif, explicatif ou opératoire qui donne prise."),
        ("Dynamique", "idea_0122", "Une relation métastable qui dérive vers l'ennui ou l'anxiété."),
        ("Mesure candidate", "idea_0071", "Le progrès local plutôt que la surprise ou l'erreur brute."),
        ("Cas limite", "idea_0124", "Une promesse de compréhension sans transformation vérifiable."),
    ]
    roles_html = "".join(
        f"""<a class="argument-card" href="{card_href(card_id, '../')}">
          <span>{label}</span><h3>{html.escape(cards[card_id].title)}</h3><p>{description}</p><small>Lire {card_id} →</small>
        </a>"""
        for label, card_id, description in roles
    )
    content = f"""
<section class="page-hero">
  <div class="shell page-hero__inner">
    <div><p class="eyebrow">La thèse</p><h1>Ce que le projet<br>cherche à établir.</h1></div>
    <p class="page-hero__lead">L'intéressant comme relation dynamique entre une forme et un sujet, capable de transformer ce que celui-ci perçoit, comprend ou peut faire.</p>
  </div>
</section>
<section class="section">
  <div class="shell thesis-page-grid">
    <aside class="thesis-index"><p>Sur cette page</p><a href="#objet">Objet</a><a href="#hypothese">Hypothèse centrale</a><a href="#architecture">Architecture</a><a href="#methode">Mise à l'épreuve</a></aside>
    <article class="prose prose--large">
      <section id="objet"><p class="eyebrow">Objet</p><h2>Constituer l'intéressant comme objet philosophique.</h2><p>Le projet ne traite pas l'intéressant comme un synonyme vague de préférence, de nouveauté ou de beauté. Il cherche à décrire un type de relation entre une forme et un sujet doté d'une mémoire, d'attentes et de capacités acquises.</p><div class="question-callout"><span>Question directrice</span><strong>{html.escape(question)}</strong></div></section>
      <section id="hypothese"><p class="eyebrow">Hypothèse centrale actuelle</p><blockquote>{html.escape(statement)}</blockquote><p>Le terme décisif est <em>construction</em>. L'objet intéressant ne se contente pas de capter l'attention : il engage un travail qui modifie les distinctions, les anticipations ou les capacités du sujet.</p><p>Cette hypothèse reste un candidat. Sa force dépendra de sa capacité à distinguer une construction réelle d'une simple impression de profondeur et à résister aux cas limites.</p></section>
      <section id="architecture"><p class="eyebrow">Architecture</p><h2>Le dossier argumentatif.</h2><div class="argument-grid">{roles_html}</div></section>
      <section id="methode"><p class="eyebrow">Mise à l'épreuve</p><h2>Construire sans naturaliser.</h2><p>La musique, les pratiques de création et les systèmes d'intelligence artificielle servent de terrains de variation. Ils rendent certaines hypothèses observables ou manipulables, sans transformer automatiquement un résultat scientifique en preuve ontologique.</p><div class="method-list"><div><strong>Musique</strong><span>Attente, mémoire et micro-transformations de l'attention.</span></div><div><strong>Intelligence artificielle</strong><span>Systèmes construits comme instruments philosophiques réflexifs.</span></div><div><strong>Création</strong><span>Contraintes, problèmes implicites et nécessité rétrospective.</span></div></div></section>
    </article>
  </div>
</section>
"""
    return base_page(
        title="La thèse",
        description="Objet, hypothèse centrale et méthode du projet de thèse.",
        content=content,
        prefix="../",
        active="these",
    )


def cards_page(cards: dict[str, Card], families: list[tuple[str, list[str]]]) -> str:
    family_options = "".join(
        f'<option value="{html.escape(name, quote=True)}">{html.escape(name)}</option>' for name, _ in families
    )
    kind_values = sorted({card.kind for card in cards.values()})
    kind_options = "".join(
        f'<option value="{kind}">{html.escape(KIND_LABELS.get(kind, kind))}</option>' for kind in kind_values
    )
    cards_html = "".join(
        f"""<article class="catalog-card family-{card.family_index}" data-card data-title="{html.escape(card.title.lower(), quote=True)}" data-text="{html.escape((card.body + ' ' + ' '.join(card.tags)).lower(), quote=True)}" data-family="{html.escape(card.family, quote=True)}" data-level="{card.level}" data-kind="{card.kind}">
          <a href="{card.id}/index.html" aria-label="Lire {html.escape(card.title, quote=True)}"></a>
          <div class="catalog-card__top"><span class="catalog-card__id">{card.id.replace('idea_', '')}</span><span class="catalog-card__family">{html.escape(card.family)}</span></div>
          <h2>{html.escape(card.title)}</h2>
          <div class="catalog-card__meta">{badge(LEVEL_LABELS.get(card.level, card.level), card.level)}{badge(KIND_LABELS.get(card.kind, card.kind))}</div>
        </article>"""
        for card in cards.values()
    )
    content = f"""
<section class="page-hero page-hero--catalog">
  <div class="shell page-hero__inner">
    <div><p class="eyebrow">Corpus argumentatif</p><h1>Les cartes<br>d'idées.</h1></div>
    <p class="page-hero__lead">Chaque carte formule une proposition indépendante, sourcée et susceptible d'être soutenue, précisée, contestée ou mise à l'épreuve.</p>
  </div>
</section>
<section class="catalog-section">
  <div class="shell">
    <form class="catalog-controls" data-catalog-form>
      <label class="search-field"><span class="sr-only">Rechercher</span><svg aria-hidden="true" viewBox="0 0 24 24"><path d="m21 21-4.4-4.4m2.4-5.1a7.5 7.5 0 1 1-15 0 7.5 7.5 0 0 1 15 0Z"/></svg><input type="search" name="recherche" placeholder="Rechercher une idée, un auteur, un concept…" autocomplete="off"></label>
      <label><span>Famille</span><select name="famille"><option value="">Toutes</option>{family_options}</select></label>
      <label><span>Niveau</span><select name="niveau"><option value="">Tous</option><option value="conceptual">Conceptuel</option><option value="scientific">Scientifique</option><option value="articulation">Articulation</option></select></label>
      <label><span>Forme</span><select name="forme"><option value="">Toutes</option>{kind_options}</select></label>
    </form>
    <div class="catalog-status"><p><strong data-result-count>{len(cards)}</strong> propositions affichées</p><button type="button" class="text-button" data-reset-filters>Effacer les filtres</button></div>
    <div class="catalog-grid" data-catalog-grid>{cards_html}</div>
    <p class="empty-state" data-empty-state hidden>Aucune carte ne correspond à cette recherche.</p>
  </div>
</section>
"""
    return base_page(
        title="Les cartes",
        description="Rechercher et parcourir les propositions du projet de thèse.",
        content=content,
        prefix="../",
        active="cartes",
    )


def card_page(
    card: Card,
    cards: dict[str, Card],
    bibliography: dict[str, BibliographyEntry],
    relations: list[Relation],
    family_ids: list[str],
) -> str:
    outgoing = [relation for relation in relations if relation.source == card.id]
    incoming = [relation for relation in relations if relation.target == card.id]

    def relation_item(relation: Relation, direction: str) -> str:
        other_id = relation.target if direction == "out" else relation.source
        other = cards[other_id]
        if direction == "out":
            label = RELATION_LABELS.get(relation.kind, relation.kind)
        else:
            label = f"est {RELATION_LABELS.get(relation.kind, relation.kind)} par"
        return f"""<li><span class="relation-kind relation-kind--{relation.kind}">{html.escape(label)}</span><a href="../{other_id}/index.html"><strong>{html.escape(other.title)}</strong><small>{html.escape(relation.explanation)}</small></a></li>"""

    relation_html = ""
    if outgoing or incoming:
        outgoing_html = "".join(relation_item(relation, "out") for relation in outgoing)
        incoming_html = "".join(relation_item(relation, "in") for relation in incoming)
        relation_html = f"""<section class="card-relations"><div class="section-heading"><p class="eyebrow">Graphe argumentatif</p><h2>Relations fortes</h2></div><div class="relation-columns">{f'<div><h3>Cette carte…</h3><ul>{outgoing_html}</ul></div>' if outgoing else ''}{f'<div><h3>D’autres cartes…</h3><ul>{incoming_html}</ul></div>' if incoming else ''}</div></section>"""

    sources_html = "".join(f"<li>{source_link(source, '../../')}</li>" for source in card.sources)
    refs_html = "".join(
        f'<li><a class="card-reference-link" href="{bibliography_href(reference, "../../")}"><span>{html.escape(reference)}</span><strong>{html.escape(short_reference(bibliography[reference]))}</strong></a></li>'
        for reference in card.references
    )
    notes_html = "".join(f"<li>{html.escape(note)}</li>" for note in card.source_notes)
    tags_html = "".join(badge(tag) for tag in card.tags)
    current_index = family_ids.index(card.id)
    previous_id = family_ids[current_index - 1] if current_index else family_ids[-1]
    next_id = family_ids[(current_index + 1) % len(family_ids)]
    content = f"""
<section class="card-hero family-{card.family_index}">
  <div class="shell">
    <nav class="breadcrumbs" aria-label="Fil d'Ariane"><a href="../../cartes/index.html">Cartes</a><span>→</span><a href="../../cartes/index.html?famille={html.escape(card.family, quote=True)}">{html.escape(card.family)}</a></nav>
    <div class="card-hero__grid">
      <div><p class="card-id">{card.id}</p><h1>{html.escape(card.title)}</h1></div>
      <aside><span>Rôle actuel</span><strong>{html.escape(card.argument_role or KIND_LABELS.get(card.kind, card.kind))}</strong><small>Organisation réversible</small></aside>
    </div>
    <div class="card-hero__meta">{badge(LEVEL_LABELS.get(card.level, card.level), card.level)}{badge(KIND_LABELS.get(card.kind, card.kind))}</div>
  </div>
</section>
<section class="section card-body-section">
  <div class="shell card-layout">
    <article class="prose card-prose">{markdown_to_html(card.body)}</article>
    <aside class="card-sidebar">
      <div><h2>Provenance</h2><ul class="source-list">{sources_html or '<li>Non renseignée</li>'}</ul></div>
      {f'<div><h2>Références</h2><ul>{refs_html}</ul></div>' if refs_html else ''}
      {f'<div><h2>Notes de source</h2><ul>{notes_html}</ul></div>' if notes_html else ''}
      <div><h2>Thèmes</h2><div class="tag-list">{tags_html}</div></div>
    </aside>
  </div>
</section>
<div class="shell">{relation_html}</div>
<nav class="card-pagination shell" aria-label="Cartes de la même famille"><a href="../{previous_id}/index.html"><span>← Carte précédente</span><strong>{html.escape(cards[previous_id].title)}</strong></a><a href="../{next_id}/index.html"><span>Carte suivante →</span><strong>{html.escape(cards[next_id].title)}</strong></a></nav>
"""
    return base_page(
        title=card.title,
        description=first_paragraph(section(card.body, "Idée"))[:155],
        content=content,
        prefix="../../",
        active="cartes",
    )


def bibliography_page(
    bibliography: dict[str, BibliographyEntry],
    cards_by_reference: dict[str, list[Card]],
    total_cards: int,
) -> str:
    entries = sorted(bibliography.values(), key=lambda entry: entry.sort_key)
    types = sorted({entry.entry_type for entry in entries})
    linked_card_ids = {
        card.id for linked_cards in cards_by_reference.values() for card in linked_cards
    }
    local_documents = {
        entry.fields["file"] for entry in entries if entry.fields.get("file")
    }
    type_options = "".join(
        f'<option value="{html.escape(entry_type, quote=True)}">{html.escape(BIBLIOGRAPHY_TYPE_LABELS.get(entry_type, entry_type))}</option>'
        for entry_type in types
    )
    items = []
    for entry in entries:
        linked_cards = cards_by_reference.get(entry.key, [])
        search_text = " ".join(entry.fields.values()) + " " + entry.key
        access = []
        if entry.fields.get("file"):
            access.append("document")
        if entry.fields.get("doi"):
            access.append("DOI")
        elif entry.fields.get("url"):
            access.append("lien externe")
        access_html = "".join(f"<span>{html.escape(item)}</span>" for item in access)
        items.append(
            f"""<article class="bibliography-item" data-reference data-search="{html.escape(search_text, quote=True)}" data-type="{html.escape(entry.entry_type, quote=True)}">
              <a href="{bibliography_href(entry.key, '../')}">
                <div class="bibliography-item__meta"><span>{html.escape(BIBLIOGRAPHY_TYPE_LABELS.get(entry.entry_type, entry.entry_type))}</span><code>{html.escape(entry.key)}</code></div>
                <p class="formatted-reference">{format_reference(entry)}</p>
                <div class="bibliography-item__footer"><span>{len(linked_cards)} idée{'s' if len(linked_cards) != 1 else ''} liée{'s' if len(linked_cards) != 1 else ''}</span><span class="bibliography-access">{access_html}</span></div>
              </a>
            </article>"""
        )
    content = f"""
<section class="page-hero page-hero--bibliography">
  <div class="shell page-hero__inner">
    <div><p class="eyebrow">Corpus bibliographique</p><h1>Les références<br>et leurs usages.</h1></div>
    <p class="page-hero__lead">Partir d'une idée pour retrouver ses appuis documentaires, ou d'une publication pour voir exactement comment elle intervient dans la thèse.</p>
  </div>
</section>
<section class="section section--compact">
  <div class="shell bibliography-metrics">
    <div><strong>{len(entries)}</strong><span>références canoniques</span></div>
    <div><strong>{len(linked_card_ids)}/{total_cards}</strong><span>cartes reliées explicitement</span></div>
    <div><strong>{len(local_documents)}</strong><span>documents rattachés aux notices</span></div>
  </div>
</section>
<section class="section bibliography-section">
  <div class="shell">
    <form class="bibliography-controls" data-bibliography-form>
      <label><span>Rechercher</span><input type="search" name="recherche" placeholder="Auteur, titre, année, revue ou clé…" autocomplete="off"></label>
      <label><span>Type</span><select name="type"><option value="">Tous les types</option>{type_options}</select></label>
    </form>
    <div class="catalog-status"><p><strong data-reference-count>{len(entries)}</strong> références affichées</p><button type="button" class="text-button" data-reset-bibliography>Effacer les filtres</button></div>
    <div class="bibliography-list">{''.join(items)}</div>
    <p class="empty-state" data-bibliography-empty hidden>Aucune référence ne correspond à cette recherche.</p>
  </div>
</section>
"""
    return base_page(
        title="Bibliographie",
        description="Bibliographie du projet de thèse et liens vers les propositions qui mobilisent chaque référence.",
        content=content,
        prefix="../",
        active="bibliographie",
    )


def reference_page(entry: BibliographyEntry, linked_cards: list[Card]) -> str:
    fields = entry.fields
    metadata_parts = []
    for name, value in fields.items():
        rendered_value = html.escape(value)
        if name == "doi":
            rendered_value = f'<a href="https://doi.org/{html.escape(value, quote=True)}">{html.escape(value)}</a>'
        elif name == "url":
            rendered_value = f'<a href="{html.escape(value, quote=True)}">{html.escape(value)}</a>'
        elif name == "file":
            rendered_value = f'<a href="{document_href(value, "../../")}">{html.escape(value)}</a>'
        metadata_parts.append(
            f"<dt>{html.escape(BIBLIOGRAPHY_FIELD_LABELS.get(name, name.title()))}</dt><dd>{rendered_value}</dd>"
        )
    metadata_rows = "".join(metadata_parts)
    actions = []
    if fields.get("file"):
        actions.append(
            f'<a class="button button--primary" href="{document_href(fields["file"], "../../")}">Ouvrir le document</a>'
        )
    if fields.get("doi"):
        actions.append(
            f'<a class="button" href="https://doi.org/{html.escape(fields["doi"], quote=True)}">Consulter via le DOI</a>'
        )
    if fields.get("url"):
        actions.append(
            f'<a class="button" href="{html.escape(fields["url"], quote=True)}">Consulter la page officielle</a>'
        )

    cards_html = []
    for card in sorted(linked_cards, key=lambda item: item.id):
        notes = "".join(f"<li>{html.escape(note)}</li>" for note in card.source_notes)
        cards_html.append(
            f"""<article class="reference-card-link">
              <div><code>{card.id}</code><span>{html.escape(card.family)}</span></div>
              <h2><a href="{card_href(card.id, '../../')}">{html.escape(card.title)}</a></h2>
              {f'<details><summary>Repérages indiqués sur la carte</summary><ul>{notes}</ul></details>' if notes else ''}
            </article>"""
        )
    content = f"""
<section class="reference-hero">
  <div class="shell">
    <nav class="breadcrumbs" aria-label="Fil d'Ariane"><a href="../index.html">Bibliographie</a><span>→</span><code>{html.escape(entry.key)}</code></nav>
    <p class="eyebrow">{html.escape(BIBLIOGRAPHY_TYPE_LABELS.get(entry.entry_type, entry.entry_type))}</p>
    <h1>{html.escape(entry.title)}</h1>
    <p class="reference-hero__contributors">{html.escape(format_people(entry.contributors))} · {html.escape(entry.year)}</p>
  </div>
</section>
<section class="section section--compact">
  <div class="shell reference-layout">
    <article>
      <p class="eyebrow">Notice recommandée</p>
      <p class="formatted-reference formatted-reference--large">{format_reference(entry)}</p>
      <div class="button-row">{''.join(actions) or '<span class="caption">Aucun accès externe ou document local renseigné.</span>'}</div>
    </article>
    <aside class="reference-metadata"><h2>Métadonnées</h2><dl>{metadata_rows}</dl></aside>
  </div>
</section>
<section class="section section--warm">
  <div class="shell">
    <div class="section-heading section-heading--split"><div><p class="eyebrow">Navigation inverse</p><h2>Idées qui mobilisent cette référence.</h2></div><p>{len(linked_cards)} proposition{'s' if len(linked_cards) != 1 else ''} possède{'nt' if len(linked_cards) != 1 else ''} actuellement un lien bibliographique explicite vers cette notice.</p></div>
    <div class="reference-card-grid">{''.join(cards_html) or '<p class="empty-reference-links">Cette référence appartient au corpus canonique mais n’est pas encore reliée explicitement à une carte.</p>'}</div>
  </div>
</section>
<section class="section section--compact">
  <div class="shell bibtex-block"><details><summary>Voir l'entrée BibTeX complète</summary><pre><code>{html.escape(entry.raw)}</code></pre></details></div>
</section>
"""
    return base_page(
        title=entry.title,
        description=f"Notice bibliographique de {entry.title} et idées du projet de thèse associées.",
        content=content,
        prefix="../../",
        active="bibliographie",
    )


def graph_svg(cards: dict[str, Card], families: list[tuple[str, list[str]]], relations: list[Relation]) -> str:
    center = 500
    radius = 355
    gap = math.radians(3)
    usable = math.tau - len(families) * gap
    angles: dict[str, float] = {}
    ranges: list[tuple[float, float, int]] = []
    cursor = math.radians(-88)
    for family_index, (_, ids) in enumerate(families):
        span = usable * len(ids) / len(cards)
        start = cursor
        step = span / len(ids)
        for offset, card_id in enumerate(ids):
            angles[card_id] = cursor + step * (offset + 0.5)
        cursor += span
        ranges.append((start, cursor, family_index))
        cursor += gap
    positions = {
        card_id: (center + radius * math.cos(angle), center + radius * math.sin(angle))
        for card_id, angle in angles.items()
    }

    arcs: list[str] = []
    for start, end, family_index in ranges:
        r = radius + 30
        x1, y1 = center + r * math.cos(start), center + r * math.sin(start)
        x2, y2 = center + r * math.cos(end), center + r * math.sin(end)
        large = 1 if end - start > math.pi else 0
        arcs.append(
            f'<path class="graph-family-arc family-{family_index}" d="M {x1:.2f} {y1:.2f} A {r} {r} 0 {large} 1 {x2:.2f} {y2:.2f}"/>'
        )

    edges = []
    for index, relation in enumerate(relations):
        sx, sy = positions[relation.source]
        tx, ty = positions[relation.target]
        pull = 0.56 if cards[relation.source].family == cards[relation.target].family else 0.32
        c1x = center + (sx - center) * pull
        c1y = center + (sy - center) * pull
        c2x = center + (tx - center) * pull
        c2y = center + (ty - center) * pull
        edges.append(
            f'<path class="graph-edge relation-{relation.kind}" data-source="{relation.source}" data-target="{relation.target}" data-relation="{relation.kind}" d="M {sx:.2f} {sy:.2f} C {c1x:.2f} {c1y:.2f}, {c2x:.2f} {c2y:.2f}, {tx:.2f} {ty:.2f}" marker-end="url(#arrow-{relation.kind})"/>'
        )

    nodes = []
    for card in cards.values():
        x, y = positions[card.id]
        radius_value = 9 if card.id == "idea_0123" else 5.5
        nodes.append(
            f'<g class="graph-node family-{card.family_index}" data-id="{card.id}" data-family="{html.escape(card.family, quote=True)}" data-level="{card.level}" data-title="{html.escape(card.title, quote=True)}" transform="translate({x:.2f} {y:.2f})" role="button" tabindex="0" aria-label="{html.escape(card.title, quote=True)}"><circle r="{radius_value}"/><title>{html.escape(card.id + " — " + card.title)}</title></g>'
        )

    marker_defs = "".join(
        f'<marker id="arrow-{kind}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z"/></marker>'
        for kind in RELATION_LABELS
    )
    return f"""<svg class="idea-graph" data-idea-graph viewBox="0 0 1000 1000" role="img" aria-label="Graphe interactif des propositions">
      <defs>{marker_defs}</defs>
      <g class="graph-arcs">{''.join(arcs)}</g>
      <g class="graph-edges">{''.join(edges)}</g>
      <g class="graph-center"><circle cx="500" cy="500" r="92"/><text x="500" y="484">{len(cards)} idées</text><text x="500" y="514">{len(relations)} relations fortes</text></g>
      <g class="graph-nodes">{''.join(nodes)}</g>
    </svg>"""


def graph_page(cards: dict[str, Card], families: list[tuple[str, list[str]]], relations: list[Relation]) -> str:
    family_options = "".join(
        f'<option value="{html.escape(name, quote=True)}">{html.escape(name)}</option>' for name, _ in families
    )
    relation_options = "".join(
        f'<option value="{kind}">{html.escape(label.capitalize())}</option>' for kind, label in RELATION_LABELS.items()
    )
    family_legend = "".join(
        f'<li class="family-{index}"><span></span>{html.escape(name)} <small>{len(ids)}</small></li>'
        for index, (name, ids) in enumerate(families)
    )
    graph_data = {
        "cards": {
            card.id: {
                "title": card.title,
                "family": card.family,
                "level": LEVEL_LABELS.get(card.level, card.level),
                "href": f"../cartes/{card.id}/index.html",
            }
            for card in cards.values()
        },
        "relations": [relation.__dict__ for relation in relations],
        "labels": RELATION_LABELS,
    }
    graph_json = json.dumps(graph_data, ensure_ascii=False).replace("</", "<\\/")
    content = f"""
<section class="page-hero page-hero--graph">
  <div class="shell page-hero__inner">
    <div><p class="eyebrow">Carte argumentative</p><h1>Voir les<br>relations.</h1></div>
    <p class="page-hero__lead">Sélectionnez une proposition pour isoler ce qui la soutient, la précise, l'opérationnalise ou en limite la portée.</p>
  </div>
</section>
<section class="graph-section">
  <div class="shell">
    <div class="graph-toolbar">
      <label><span>Aller à une carte</span><input type="search" list="graph-cards" placeholder="Titre ou identifiant" data-graph-search><datalist id="graph-cards">{''.join(f'<option value="{card.id}">{html.escape(card.title)}</option>' for card in cards.values())}</datalist></label>
      <label><span>Famille</span><select data-graph-family><option value="">Toutes</option>{family_options}</select></label>
      <label><span>Relation</span><select data-graph-relation><option value="">Toutes</option>{relation_options}</select></label>
      <button type="button" class="button button--small" data-graph-reset>Vue générale</button>
    </div>
    <div class="graph-layout">
      <div class="graph-canvas">{graph_svg(cards, families, relations)}</div>
      <aside class="graph-detail" data-graph-detail>
        <p class="eyebrow">Mode d'emploi</p><h2>Choisissez une proposition.</h2><p>Le graphe affichera son voisinage argumentatif immédiat. Les flèches indiquent le sens des relations fortes.</p>
        <div class="graph-detail__legend"><h3>Familles</h3><ul>{family_legend}</ul></div>
      </aside>
    </div>
    <div class="relation-legend">{''.join(f'<span class="relation-{kind}"><i></i>{html.escape(label)}</span>' for kind, label in RELATION_LABELS.items())}</div>
  </div>
</section>
<script id="graph-data" type="application/json">{graph_json}</script>
"""
    return base_page(
        title="Le graphe",
        description="Explorer les relations fortes entre les propositions du projet de thèse.",
        content=content,
        prefix="../",
        active="graphe",
    )


def suivi_page(
    cards: dict[str, Card],
    bibliography: dict[str, BibliographyEntry],
    families: list[tuple[str, list[str]]],
    relations: list[Relation],
    questions: list[str],
    last_date: str,
    git_changes: list[tuple[str, str, str]],
) -> str:
    levels = Counter(card.level for card in cards.values())
    source_total, source_statuses = registry_stats()
    covered = sum(
        count for status, count in source_statuses.items() if "complete" in status or "intégr" in status
    )
    questions_html = "".join(f"<li>{inline_markdown(item)}</li>" for item in questions)
    changes_html = "".join(
        f'<li><time datetime="{date}">{datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y")}</time><span>{html.escape(message)}</span><code>{commit}</code></li>'
        for commit, date, message in git_changes
    )
    family_progress = "".join(
        f"""<div class="progress-row family-{index}"><div><strong>{html.escape(name)}</strong><span>{len(ids)} cartes</span></div><span class="progress-row__line"><i style="width:{len(ids) / max(len(group) for _, group in families) * 100:.1f}%"></i></span></div>"""
        for index, (name, ids) in enumerate(families)
    )
    referenced_cards = {card.id for card in cards.values() if card.references}
    public_documents = {source for card in cards.values() for source in card.sources}
    bibliography_coverage = "".join(
        f"""<div class="coverage-row family-{index}"><div><strong>{html.escape(name)}</strong><span>{sum(1 for card_id in ids if card_id in referenced_cards)}/{len(ids)} cartes référencées</span></div><span class="coverage-row__bar"><i style="width:{sum(1 for card_id in ids if card_id in referenced_cards) / len(ids) * 100:.1f}%"></i></span></div>"""
        for index, (name, ids) in enumerate(families)
    )
    content = f"""
<section class="page-hero page-hero--suivi">
  <div class="shell page-hero__inner">
    <div><p class="eyebrow">Tableau de suivi</p><h1>Un projet<br>en mouvement.</h1></div>
    <p class="page-hero__lead">Cette page distingue ce qui est structuré, ce qui reste provisoire et les questions qui orientent le prochain travail.</p>
  </div>
</section>
<section class="section section--compact">
  <div class="shell status-strip">
    <div><span>Version du projet</span><strong>Version 2</strong><small>Texte français et anglais synchronisé</small></div>
    <div><span>Dernière évolution</span><strong>{datetime.strptime(last_date, '%Y-%m-%d').strftime('%d.%m.%Y') if last_date else '—'}</strong><small>D'après l'historique Git</small></div>
    <div><span>Corpus traité</span><strong>{covered}/{source_total}</strong><small>Documents à couverture complète ou intégrée</small></div>
    <div><span>Couverture bibliographique</span><strong>{len(referenced_cards)}/{len(cards)}</strong><small>Cartes reliées à une notice canonique</small></div>
  </div>
</section>
<section class="section">
  <div class="shell follow-grid">
    <article>
      <p class="eyebrow">Ce qui est en place</p><h2>Une architecture vérifiable.</h2>
      <ul class="check-list"><li><strong>{len(cards)} propositions</strong><span>Chaque carte possède un niveau, une famille principale et une provenance lorsque celle-ci est connue.</span></li><li><strong>{len(relations)} relations fortes</strong><span>Neuf types directionnels distinguent soutien, précision, objection, limite et opérationnalisation.</span></li><li><strong>Une thèse centrale explicite</strong><span><code>idea_0123</code> sert de proposition canonique et relie le cadre relationnel aux terrains scientifiques.</span></li><li><strong>Trois niveaux épistémiques</strong><span>{levels['conceptual']} cartes conceptuelles, {levels['scientific']} scientifiques et {levels['articulation']} articulations.</span></li></ul>
    </article>
    <article>
      <p class="eyebrow">Répartition actuelle</p><h2>Sept familles de travail.</h2><div class="progress-list">{family_progress}</div><p class="caption">La longueur indique le nombre de propositions, pas leur importance ni leur degré d'achèvement.</p>
    </article>
  </div>
</section>
<section class="section section--ink">
  <div class="shell follow-grid bibliography-follow">
    <div><p class="eyebrow eyebrow--light">Assise documentaire</p><h2>Une couverture mesurable,<br>encore inégale.</h2><p class="section-intro">Le corpus comprend {len(bibliography)} notices canoniques et {len(public_documents)} documents publics effectivement mobilisés par les cartes. L'indicateur mesure les liens bibliographiques explicites, sans confondre une publication avec le fichier précis qui a été lu.</p><a class="button button--light" href="../bibliographie/index.html">Explorer la bibliographie</a></div>
    <div class="coverage-list">{bibliography_coverage}</div>
  </div>
</section>
<section class="section section--warm">
  <div class="shell follow-grid follow-grid--questions">
    <div><p class="eyebrow">À discuter</p><h2>Questions ouvertes.</h2><p>Ces questions ne sont pas des défauts masqués : elles indiquent les points où une objection, une source ou une reformulation peut changer l'architecture.</p></div>
    <ol class="question-list">{questions_html}</ol>
  </div>
</section>
<section class="section">
  <div class="shell follow-grid">
    <div><p class="eyebrow">Journal de recherche</p><h2>Dernières transformations.</h2><p class="section-intro">L'historique Git rend visibles les changements intellectuels et documentaires, au-delà des seules versions stabilisées.</p></div>
    <ol class="change-list">{changes_html}</ol>
  </div>
</section>
"""
    return base_page(
        title="Suivi",
        description="État du corpus, questions ouvertes et dernières évolutions du projet de thèse.",
        content=content,
        prefix="../",
        active="suivi",
    )


def write_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build(output: Path) -> None:
    cards = load_cards()
    bibliography = load_bibliography()
    missing_references = sorted(
        {reference for card in cards.values() for reference in card.references}
        - set(bibliography)
    )
    if missing_references:
        raise ValueError(
            "Références absentes de la bibliographie : " + ", ".join(missing_references)
        )
    cards_by_reference: dict[str, list[Card]] = defaultdict(list)
    for card in cards.values():
        for reference in card.references:
            cards_by_reference[reference].append(card)
    families = load_families(cards)
    load_themes(cards)
    relations = load_relations(cards)
    statement = thesis_statement()
    question = direct_question()
    questions = open_questions()
    last_date, git_changes = git_metadata()

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree(SITE_SOURCE / "assets", output / "assets")
    shutil.copytree(ROOT / "input", output / "documents" / "input")
    source_paths = {source for card in cards.values() for source in card.sources}
    source_paths.update(
        entry.fields["file"]
        for entry in bibliography.values()
        if entry.fields.get("file")
    )
    for source in source_paths:
        origin = ROOT / source
        if not origin.is_file():
            raise ValueError(f"Document public introuvable : {source}")
        destination = output / "documents" / source
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            shutil.copy2(origin, destination)
    write_page(
        output / "index.html",
        home_page(cards, families, relations, statement, question, questions, last_date),
    )
    write_page(output / "these" / "index.html", thesis_page(cards, statement, question))
    write_page(output / "cartes" / "index.html", cards_page(cards, families))
    write_page(
        output / "bibliographie" / "index.html",
        bibliography_page(bibliography, cards_by_reference, len(cards)),
    )
    write_page(output / "graphe" / "index.html", graph_page(cards, families, relations))
    write_page(
        output / "suivi" / "index.html",
        suivi_page(
            cards,
            bibliography,
            families,
            relations,
            questions,
            last_date,
            git_changes,
        ),
    )
    family_ids = {name: ids for name, ids in families}
    for card in cards.values():
        write_page(
            output / "cartes" / card.id / "index.html",
            card_page(card, cards, bibliography, relations, family_ids[card.family]),
        )
    for entry in bibliography.values():
        write_page(
            output / "bibliographie" / entry.key / "index.html",
            reference_page(entry, cards_by_reference.get(entry.key, [])),
        )

    public_documents = {source for card in cards.values() for source in card.sources}
    referenced_cards = sum(1 for card in cards.values() if card.references)
    manifest = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "cards": len(cards),
        "families": len(families),
        "relations": len(relations),
        "references": len(bibliography),
        "referenced_cards": referenced_cards,
        "public_documents": len(public_documents),
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Site généré dans {output} : {len(cards)} cartes, "
        f"{len(families)} familles, {len(relations)} relations, "
        f"{len(bibliography)} références."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Génère le site statique de suivi de la thèse.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    build(output)


if __name__ == "__main__":
    main()
