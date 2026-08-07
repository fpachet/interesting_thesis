#!/usr/bin/env python3
"""Extract and rank personal publications for a thesis-relevance review.

This is a discovery aid, not an automatic relevance decision.  It creates a
uniform text corpus and surfaces abstracts/conclusions plus lexical signals so
that the subsequent human/LLM reading can be systematic and auditable.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from pathlib import Path


SIGNALS = {
    "interest_attention": (
        r"\binterest(?:ing|ed|s)?\b|\bint[ée]ress\w*|\battention\w*|\bcurios\w*|\bboredom\b|\bboring\b|\bennui\w*",
        5,
    ),
    "expectation_novelty": (
        r"\bexpect\w*|\battente\w*|\bsurpris\w*|\bunexpected\w*|\bnovel\w*|\bnouvea\w*|\bfamiliar\w*",
        3,
    ),
    "creation_generation": (
        r"\bcreati\w*|\bcr[ée]a\w*|\binvent\w*|\bgenerat\w*|\bg[ée]n[ée]r\w*|\bcompos\w*|\bimprovis\w*",
        2,
    ),
    "interaction_reflexivity": (
        r"\binteract\w*|\br[ée]flexi\w*|\bmirror\w*|\bmiroir\w*|\bfeedback\b|\bappren\w*|\blearn\w*",
        2,
    ),
    "subject_preference": (
        r"\bsubject\w*|\bsujet\w*|\bprefer\w*|\bpr[ée]f[ée]r\w*|\btaste\b|\bgo[uû]t\w*|\blisten\w*|\bauditeur\w*|\buser behavio\w*",
        2,
    ),
    "temporality_structure": (
        r"\btemporal\w*|\bsequence\w*|\bcontinu\w*|\bstructure\w*|\bskip\w*|\bduration\w*|\btrajectory\w*|\bparcours\w*",
        1,
    ),
    "constraint_exploration": (
        r"\bconstraint\w*|\bcontrainte\w*|\bexplor\w*|\bpossible\w*|\bcontrol\w*|\bcontr[oô]l\w*",
        1,
    ),
}


@dataclass
class ReviewRow:
    rank: int
    id: str
    year: str
    section: str
    title: str
    local_path: str
    pages: str
    words: int
    score: int
    signals: str
    abstract_excerpt: str
    conclusion_excerpt: str
    review_status: str = "triage lexical seulement"
    relevance: str = ""
    thesis_use: str = ""
    target_cards: str = ""
    notes_pages: str = ""


def normalize_text(value: str) -> str:
    value = value.replace("\x0c", "\n")
    value = re.sub(r"(?<=\w)-\n(?=\w)", "", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def extract_one(pdf: Path, text_path: Path) -> tuple[Path, str]:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        ["pdftotext", "-layout", str(pdf), str(text_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        return pdf, completed.stderr.strip() or "pdftotext failed"
    return pdf, ""


def section_excerpt(text: str, heading: str, limit: int = 1100) -> str:
    patterns = {
        "abstract": r"(?im)^\s*(?:abstract|r[ée]sum[ée])\s*[:.—-]?\s*$",
        "conclusion": r"(?im)^\s*(?:\d+[.)]?\s*)?(?:conclusions?|discussion(?: and conclusion)?|conclusion et perspectives?)\s*[:.—-]?\s*$",
    }
    match = re.search(patterns[heading], text)
    if not match:
        return ""
    tail = text[match.end() :]
    next_heading = re.search(
        r"(?m)^\s*(?:\d+(?:\.\d+)*[.)]?\s+)?[A-ZÀ-ÖØ-Ý][A-ZÀ-ÖØ-Ý0-9 ,:'’\-/]{3,}\s*$",
        tail,
    )
    if next_heading and next_heading.start() < limit:
        tail = tail[: next_heading.start()]
    return re.sub(r"\s+", " ", tail[:limit]).strip()


def signal_counts(text: str, title: str, abstract: str, conclusion: str) -> tuple[int, str]:
    regions = [
        (title, 12),
        (abstract, 5),
        (conclusion, 4),
        (text, 1),
    ]
    score = 0
    evidence: list[str] = []
    for name, (pattern, weight) in SIGNALS.items():
        counts = [len(re.findall(pattern, region, flags=re.IGNORECASE)) for region, _ in regions]
        weighted = sum(min(count, 8) * multiplier for count, (_, multiplier) in zip(counts, regions))
        if counts[0]:
            weighted += 20
        score += weighted * weight
        if sum(counts):
            evidence.append(f"{name}:{'/'.join(map(str, counts))}")
    return score, "; ".join(evidence)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path)
    parser.add_argument("downloads", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--texts", type=Path, default=Path("tmp/personal-publications-text"))
    parser.add_argument("--tsv", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument(
        "--decisions",
        type=Path,
        default=Path("docs/lectures/publications-francois-pachet-decisions.tsv"),
    )
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    with args.inventory.open(encoding="utf-8", newline="") as handle:
        inventory = list(csv.DictReader(handle, delimiter="\t"))
    with args.downloads.open(encoding="utf-8", newline="") as handle:
        downloads = list(csv.DictReader(handle, delimiter="\t"))

    by_url = {row["pdf_url"]: row for row in inventory if row["pdf_url"]}
    by_hash: dict[str, dict[str, str]] = {}
    for row in downloads:
        by_hash.setdefault(row["sha256"], row)
    unique = list(by_hash.values())

    repo = args.repo.resolve()
    text_root = (repo / args.texts).resolve()
    jobs: dict[object, tuple[dict[str, str], Path]] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for row in unique:
            pdf = repo / row["local_path"]
            text_path = text_root / f"{pdf.stem}.txt"
            jobs[executor.submit(extract_one, pdf, text_path)] = (row, text_path)
        for index, future in enumerate(as_completed(jobs), start=1):
            pdf, error = future.result()
            if error:
                print(f"[{index:03d}/{len(jobs):03d}] ERROR {pdf.name}: {error}", flush=True)
            elif index % 25 == 0 or index == len(jobs):
                print(f"[{index:03d}/{len(jobs):03d}] extracted", flush=True)

    review_rows: list[ReviewRow] = []
    failures = 0
    for download in unique:
        source = by_url.get(download["pdf_url"], {})
        if source.get("scientific_scope") != "oui":
            continue
        pdf = repo / download["local_path"]
        text_path = text_root / f"{pdf.stem}.txt"
        if not text_path.exists():
            failures += 1
            continue
        text = normalize_text(text_path.read_text(encoding="utf-8", errors="replace"))
        abstract = section_excerpt(text, "abstract")
        conclusion = section_excerpt(text, "conclusion")
        score, signals = signal_counts(text, source.get("title", pdf.stem), abstract, conclusion)
        review_rows.append(
            ReviewRow(
                rank=0,
                id=source.get("id", ""),
                year=source.get("year", ""),
                section=source.get("section", ""),
                title=source.get("title", pdf.stem),
                local_path=download["local_path"],
                pages=download["pages"],
                words=len(re.findall(r"\b\w+\b", text)),
                score=score,
                signals=signals,
                abstract_excerpt=abstract,
                conclusion_excerpt=conclusion,
            )
        )

    review_rows.sort(key=lambda item: (-item.score, item.year, item.title.casefold()))
    for rank, row in enumerate(review_rows, start=1):
        row.rank = rank

    decisions: dict[str, dict[str, str]] = {}
    if args.decisions.exists():
        with args.decisions.open(encoding="utf-8", newline="") as handle:
            for decision in csv.DictReader(handle, delimiter="\t"):
                decisions[decision["local_path"]] = decision
    for row in review_rows:
        decision = decisions.get(row.local_path)
        if not decision:
            continue
        row.review_status = decision["review_status"]
        row.relevance = decision["relevance"]
        row.thesis_use = decision["thesis_use"]
        row.target_cards = decision["target_cards"]
        row.notes_pages = decision["notes_pages"]

    args.tsv.parent.mkdir(parents=True, exist_ok=True)
    with args.tsv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(review_rows[0])), delimiter="\t")
        writer.writeheader()
        for row in review_rows:
            writer.writerow(asdict(row))

    bands = Counter(
        "priorité haute" if row.score >= 400 else "priorité moyenne" if row.score >= 180 else "priorité basse"
        for row in review_rows
    )
    decided = sum(row.review_status != "triage lexical seulement" for row in review_rows)
    lines = [
        "# Triage des publications personnelles pour la thèse",
        "",
        "Ce document ordonne la lecture ; il ne prononce aucune décision de pertinence.",
        "Le score combine des occurrences dans le titre, l’abstract, la conclusion et le texte",
        "complet. Une décision ne devient valide qu’après lecture et relevé de pages.",
        "",
        "## État du corpus",
        "",
        f"- {len(review_rows)} PDF scientifiques uniques après dédoublonnage ;",
        f"- {sum(int(row.pages) for row in review_rows if row.pages)} pages ;",
        f"- {len(review_rows)} textes extraits ;",
        f"- {failures} échecs d’extraction ;",
        f"- {decided} décisions de lecture validées ;",
        f"- {bands['priorité haute']} texte{'s' if bands['priorité haute'] != 1 else ''} en priorité haute, {bands['priorité moyenne']} en priorité moyenne, {bands['priorité basse']} en priorité basse.",
        "",
        "## Ordre de lecture proposé",
        "",
        "| Rang | ID | Année | Titre | Pages | Score de triage | Décision |",
        "|---:|---|---:|---|---:|---:|---|",
    ]
    for row in review_rows:
        title = row.title.replace("|", "\\|")
        lines.append(
            f"| {row.rank} | {row.id} | {row.year} | {title} | {row.pages} | {row.score} | {row.relevance or 'à examiner'} |"
        )
    lines += [
        "",
        "Les extraits de travail et les colonnes de décision se trouvent dans",
        "`publications-francois-pachet-triage.tsv`. Les textes extraits sont conservés dans",
        "`tmp/personal-publications-text/` et restent hors versionnement.",
        "",
    ]
    args.markdown.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(review_rows)} extracted texts; {failures} failures")


if __name__ == "__main__":
    main()
