#!/usr/bin/env python3
"""Build a reproducible inventory from francoispachet.fr/publications.

The script deliberately uses only the Python standard library.  It parses a
previously downloaded HTML page, extracts each bibliographic list item and
emits both a machine-readable TSV file and a compact Markdown report.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


SCIENTIFIC_SECTIONS = {
    "Book chapters",
    "Important Journals",
    "Important conferences",
    "Arxiv",
    "Other",
    "Unpublished",
    "Thesis",
    "Technical Reports",
}


def clean_text(value: str) -> str:
    value = html.unescape(value).replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()


def clean_section(value: str) -> str:
    value = clean_text(value)
    return re.sub(r"\s*\(\d+(?::[^)]*)?\)\s*$", "", value).strip()


@dataclass
class Link:
    url: str
    text_parts: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return clean_text("".join(self.text_parts))


@dataclass
class Entry:
    section: str
    text_parts: list[str] = field(default_factory=list)
    links: list[Link] = field(default_factory=list)

    @property
    def citation(self) -> str:
        return clean_text("".join(self.text_parts))


class PublicationsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.article_depth = 0
        self.in_article = False
        self.heading_depth = 0
        self.heading_parts: list[str] = []
        self.current_section = "Front matter"
        self.li_depth = 0
        self.current_entry: Entry | None = None
        self.current_link: Link | None = None
        self.entries: list[Entry] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "article" and attributes.get("id") == "post-33":
            self.in_article = True
            self.article_depth = 1
            return
        if not self.in_article:
            return
        if tag == "article":
            self.article_depth += 1
        if tag == "h1":
            self.heading_depth = 1
            self.heading_parts = []
        elif self.heading_depth:
            self.heading_depth += 1
        if tag == "li":
            self.li_depth = 1
            self.current_entry = Entry(section=self.current_section)
        elif self.li_depth:
            self.li_depth += 1
        if tag == "a" and self.current_entry is not None:
            url = attributes.get("href") or ""
            self.current_link = Link(url=clean_text(url))
            self.current_entry.links.append(self.current_link)

    def handle_endtag(self, tag: str) -> None:
        if not self.in_article:
            return
        if tag == "a":
            self.current_link = None
        if self.heading_depth:
            self.heading_depth -= 1
            if self.heading_depth == 0:
                heading = clean_section("".join(self.heading_parts))
                if heading and heading != "Publications":
                    self.current_section = heading
        if self.li_depth:
            self.li_depth -= 1
            if self.li_depth == 0 and self.current_entry is not None:
                if self.current_entry.citation:
                    self.entries.append(self.current_entry)
                self.current_entry = None
                self.current_link = None
        if tag == "article":
            self.article_depth -= 1
            if self.article_depth == 0:
                self.in_article = False

    def handle_data(self, data: str) -> None:
        if not self.in_article:
            return
        if self.heading_depth:
            self.heading_parts.append(data)
        if self.current_entry is not None:
            self.current_entry.text_parts.append(data)
            if self.current_link is not None:
                self.current_link.text_parts.append(data)


def is_pdf_url(url: str) -> bool:
    return urlparse(url).path.lower().endswith(".pdf")


def candidate_title(entry: Entry, link: Link | None) -> str:
    if link is not None and link.text:
        return link.text.strip(" .")
    if entry.links and entry.links[0].text:
        return entry.links[0].text.strip(" .")
    citation = entry.citation
    match = re.search(r"(?:\. |\) )(.+?)(?:\. (?:In |Proceedings|[A-Z][^.]+, \d{4})|$)", citation)
    return (match.group(1) if match else citation).strip(" .")


def candidate_year(citation: str) -> str:
    years = re.findall(r"(?<!\d)(?:19|20)\d{2}(?!\d)", citation)
    return years[-1] if years else ""


def safe_filename(url: str, sequence: int) -> str:
    name = unquote(Path(urlparse(url).path).name)
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    if not name.lower().endswith(".pdf"):
        name = f"publication_{sequence:03d}.pdf"
    return name


def existing_pdf_names(repo: Path) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for path in repo.rglob("*.pdf"):
        if ".git" in path.parts or "output" in path.parts:
            continue
        found.setdefault(path.name.casefold(), []).append(str(path.relative_to(repo)))
    return found


def build_rows(entries: list[Entry], repo: Path) -> list[dict[str, str]]:
    existing = existing_pdf_names(repo)
    rows: list[dict[str, str]] = []
    record_id = 0
    for page_index, entry in enumerate(entries, start=1):
        if entry.section == "Front matter":
            continue
        pdf_links = [link for link in entry.links if is_pdf_url(link.url)]
        if pdf_links:
            links: list[Link | None] = pdf_links
        else:
            links = [None]
        for link in links:
            record_id += 1
            url = link.url if link is not None else ""
            filename = safe_filename(url, record_id) if url else ""
            existing_paths = existing.get(filename.casefold(), []) if filename else []
            if url and existing_paths:
                status = "déjà présent"
            elif url:
                status = "à télécharger"
            elif entry.links:
                status = "lien indirect à résoudre"
            else:
                status = "aucun lien"
            rows.append(
                {
                    "id": f"FP-{record_id:03d}",
                    "page_index": str(page_index),
                    "section": entry.section,
                    "scientific_scope": "oui" if entry.section in SCIENTIFIC_SECTIONS else "non",
                    "year": candidate_year(entry.citation),
                    "title": candidate_title(entry, link),
                    "citation": entry.citation,
                    "pdf_url": url,
                    "other_urls": " | ".join(item.url for item in entry.links if item is not link),
                    "local_target": f"input/publications-francois-pachet/{filename}" if filename else "",
                    "existing_paths": " | ".join(existing_paths),
                    "download_status": status,
                    "review_status": "à examiner" if entry.section in SCIENTIFIC_SECTIONS else "hors corpus articles",
                    "relevance": "",
                    "thesis_use": "",
                }
            )
    return rows


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], source_url: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sections = Counter(row["section"] for row in rows)
    statuses = Counter(row["download_status"] for row in rows)
    scientific = [row for row in rows if row["scientific_scope"] == "oui"]
    direct_scientific = [row for row in scientific if row["pdf_url"]]
    lines = [
        "# Inventaire des publications de François Pachet",
        "",
        f"Source : [{source_url}]({source_url})",
        "",
        "Cet inventaire est un état de travail reproductible. Une ligne correspond à une publication,",
        "ou à une version PDF distincte lorsque la notice en propose plusieurs. Le TSV associé contient",
        "la citation complète, tous les liens et les colonnes destinées à la revue de pertinence.",
        "",
        "## Synthèse",
        "",
        f"- {len(rows)} notices/versions inventoriées ;",
        f"- {len(scientific)} notices dans le périmètre scientifique à examiner ;",
        f"- {len(direct_scientific)} PDF scientifiques directement téléchargeables ;",
        f"- {statuses['déjà présent']} PDF déjà présents dans le dépôt ;",
        f"- {statuses['à télécharger']} PDF directs restant à télécharger ;",
        f"- {statuses['lien indirect à résoudre']} notices avec lien indirect à résoudre ;",
        f"- {statuses['aucun lien']} notices sans aucun lien.",
        "",
        "## Répartition de la page",
        "",
        "| Section | Notices/versions | Périmètre de revue |",
        "|---|---:|:---:|",
    ]
    for section, count in sections.items():
        scope = "oui" if section in SCIENTIFIC_SECTIONS else "non"
        lines.append(f"| {section} | {count} | {scope} |")
    lines += [
        "",
        "## PDF scientifiques à télécharger",
        "",
        "| ID | Année | Section | Titre | État local |",
        "|---|---:|---|---|---|",
    ]
    for row in direct_scientific:
        title = row["title"].replace("|", "\\|")
        url = row["pdf_url"]
        lines.append(
            f"| {row['id']} | {row['year']} | {row['section']} | "
            f"[{title}]({url}) | {row['download_status']} |"
        )
    lines += [
        "",
        "## Notices scientifiques sans PDF direct",
        "",
        "Ces notices demandent soit de suivre une page d’éditeur ou d’archive, soit une recherche",
        "bibliographique complémentaire. Elles ne sont pas considérées comme absentes tant que cette",
        "résolution n’a pas été tentée.",
        "",
        "| ID | Année | Section | Titre | État |",
        "|---|---:|---|---|---|",
    ]
    for row in scientific:
        if row["pdf_url"]:
            continue
        title = row["title"].replace("|", "\\|")
        lines.append(
            f"| {row['id']} | {row['year']} | {row['section']} | {title} | {row['download_status']} |"
        )
    lines += [
        "",
        "## Méthode de la seconde passe",
        "",
        "Pour chaque texte : contrôle du fichier, extraction du texte, lecture de l’abstract, de",
        "l’argument complet et de la conclusion, relevé des passages/pages utiles, puis classement :",
        "`fort` (carte ou articulation nouvelle), `moyen` (renforce une carte), `contexte`, ou",
        "`non pertinent`. Une publication pertinente reçoit aussi une proposition d’usage précis dans",
        "la thèse et une entrée bibliographique marquée `francois-pachet`.",
        "",
        "Le détail complet et les colonnes de décision se trouvent dans",
        "`publications-francois-pachet-inventaire.tsv`.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--tsv", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument(
        "--source-url",
        default="https://www.francoispachet.fr/publications/",
    )
    args = parser.parse_args()

    page = PublicationsParser()
    page.feed(args.html.read_text(encoding="utf-8"))
    rows = build_rows(page.entries, args.repo.resolve())
    if not rows:
        raise SystemExit("No publication records found")
    write_tsv(args.tsv, rows)
    write_markdown(args.markdown, rows, args.source_url)
    print(f"{len(rows)} rows; {sum(bool(row['pdf_url']) for row in rows)} direct PDFs")


if __name__ == "__main__":
    main()
