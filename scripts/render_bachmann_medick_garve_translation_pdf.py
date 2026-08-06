#!/usr/bin/env python3
"""Translate and typeset Bachmann-Medick's essay on Garve.

The translation is intentionally labelled as a working document. Translation
and PDF rendering are separate so the local Argos environment and the bundled
ReportLab runtime can be used independently.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "Garve-Interessierendes2.pdf"
DEFAULT_TEXT = ROOT / "tmp/pdfs/garve_interessierendes_article/source.txt"
DEFAULT_JSON = ROOT / "tmp/pdfs/garve_interessierendes_article/translation.json"
DEFAULT_PDF = ROOT / "output/pdf/bachmann-medick-garve-interessant-traduction-de-travail.pdf"
SOURCE_URL = "https://bachmann-medick.de/wp-content/uploads/2006/07/Garve-Interessierendes2.pdf"

POLISHED_TRANSLATIONS = {
    "Anziehungskraft statt Selbstinteresse.\nChristian Garves nicht-utilitarische Konzeption des „Interessierenden“\nInteresse im Kontext ästhetischer Erfahrung": (
        "Force d’attraction plutôt qu’intérêt personnel.<br/>"
        "La conception non utilitariste de « l’intéressant » chez Christian Garve<br/>"
        "L’intérêt dans le contexte de l’expérience esthétique"
    ),
    "Interesse und Moral: das Vorurteil vom typisch neuzeitlichen Interessebegriff": (
        "Intérêt et morale : le préjugé d’une conception typiquement moderne de l’intérêt"
    ),
    "Interesse und Aufmerksamkeit": "Intérêt et attention",
    "Das „Interessirende“ als Teilnahme am „Gegenstand“": (
        "L’« intéressant » comme participation à l’« objet »"
    ),
    "Die „Energie“ des „Interessirenden“: Vorstellungsentwicklung, Erfahrungsbildung und\nHandlungskraft": (
        "L’« énergie » de l’intéressant : développement des représentations, formation de l’expérience et puissance d’agir"
    ),
}


def normalize_text(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = re.sub(r"-\s*\n\s*(?=[a-zäöüß])", "", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_heading(block: str) -> bool:
    flat = normalize_text(block)
    if block in POLISHED_TRANSLATIONS:
        return True
    return len(flat) < 135 and not re.search(r"[.!?;:]$", flat)


def extract(source_pdf: Path, text_path: Path) -> dict[str, object]:
    text_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdftotext", str(source_pdf), str(text_path)], check=True)
    pages = text_path.read_text(encoding="utf-8").split("\f")
    page_payloads: list[dict[str, object]] = []
    for page_number, page in enumerate(pages, 1):
        if not page.strip():
            continue
        raw_blocks = [block.strip() for block in page.split("\n\n") if block.strip()]
        if raw_blocks and raw_blocks[0].strip() == str(page_number):
            raw_blocks.pop(0)
        blocks: list[dict[str, object]] = []
        for index, raw in enumerate(raw_blocks):
            if page_number == 1 and index == 0 and raw == "Doris Bachmann-Medick":
                kind = "author"
            elif page_number == 1 and index == 1:
                kind = "title"
            elif re.match(r"^\d+[.]?\s", raw):
                kind = "notes"
            elif is_heading(raw):
                kind = "heading"
            else:
                kind = "body"
            blocks.append(
                {
                    "kind": kind,
                    "source": raw if kind == "title" else normalize_text(raw),
                    "translation": POLISHED_TRANSLATIONS.get(raw),
                }
            )
        page_payloads.append({"source_page": page_number, "blocks": blocks})
    return {
        "author": "Doris Bachmann-Medick",
        "title_fr": "Force d’attraction plutôt qu’intérêt personnel",
        "subtitle_fr": "La conception non utilitariste de « l’intéressant » chez Christian Garve",
        "title_de": "Anziehungskraft statt Selbstinteresse. Christian Garves nicht-utilitarische Konzeption des „Interessierenden“",
        "year": 2008,
        "source_url": SOURCE_URL,
        "pages": page_payloads,
    }


def save_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def split_for_translation(text: str, limit: int = 1450) -> list[str]:
    if len(text) <= limit:
        return [text]
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ0-9])", text)
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if not current:
            current = sentence
        elif len(current) + len(sentence) + 1 <= limit:
            current += " " + sentence
        else:
            chunks.append(current)
            current = sentence
    if current:
        chunks.append(current)
    return chunks


def split_for_marian(text: str, limit: int = 620) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ0-9„\"])", text)
    pieces: list[str] = []
    for sentence in sentences:
        if len(sentence) <= limit:
            pieces.append(sentence)
            continue
        clauses = re.split(r"(?<=[;:])\s+|\s+(?=[—–-])", sentence)
        current = ""
        for clause in clauses:
            if len(clause) > limit:
                words = clause.split()
                for word in words:
                    if current and len(current) + len(word) + 1 > limit:
                        pieces.append(current)
                        current = word
                    else:
                        current = f"{current} {word}".strip()
            elif current and len(current) + len(clause) + 1 > limit:
                pieces.append(current)
                current = clause
            else:
                current = f"{current} {clause}".strip()
        if current:
            pieces.append(current)

    chunks: list[str] = []
    current = ""
    for piece in pieces:
        if current and len(current) + len(piece) + 1 > limit:
            chunks.append(current)
            current = piece
        else:
            current = f"{current} {piece}".strip()
    if current:
        chunks.append(current)
    return chunks


def prepare_for_translation(text: str) -> str:
    """Modernize recurrent historical forms that confuse the local models."""
    replacements = {
        "des „Interessirenden“": "des Phänomens des Interessantmachenden",
        "dem „Interessirenden“": "dem Phänomen des Interessantmachenden",
        "das „Interessirende“": "das Phänomen des Interessantmachenden",
        "Das „Interessirende“": "Das Phänomen des Interessantmachenden",
        "vom „Interessirenden“": "vom Phänomen des Interessantmachenden",
        "zum „Interessirenden“": "zum Phänomen des Interessantmachenden",
        "„Interessirendes“": "Phänomen des Interessantmachenden",
        "„Interessirenden“": "Phänomen des Interessantmachenden",
        "„Interessirende“": "Phänomen des Interessantmachenden",
        "Interessirenden": "Phänomen des Interessantmachenden",
        "Interessirende": "Phänomen des Interessantmachenden",
        "interessirenden": "interessierenden",
        "interessirende": "interessierende",
        "interessirt": "interessiert",
        "Interessiren": "Interessieren",
        "beym": "beim",
        "Beym": "Beim",
        "bey": "bei",
        "Bey": "Bei",
        "seyn": "sein",
        "thun": "tun",
        "frey": "frei",
        "muß": "muss",
        "läßt": "lässt",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def translate_payload(payload: dict[str, object], json_path: Path) -> None:
    from argostranslate import translate

    blocks = [block for page in payload["pages"] for block in page["blocks"]]
    total = len(blocks)
    for index, block in enumerate(blocks, 1):
        if block.get("translation"):
            continue
        source = str(block["source"])
        if block["kind"] == "author":
            block["translation"] = source
        else:
            prepared = prepare_for_translation(source)
            translated = [translate.translate(chunk, "de", "fr") for chunk in split_for_translation(prepared)]
            block["translation"] = " ".join(piece.strip() for piece in translated if piece.strip())
        save_json(json_path, payload)
        print(f"[{index:03d}/{total:03d}] {block['kind']} - {len(source)} caractères", flush=True)


def translate_payload_marian(payload: dict[str, object], json_path: Path) -> None:
    import torch
    from transformers import MarianMTModel, MarianTokenizer

    model_name = "Helsinki-NLP/opus-mt-de-fr"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model.to(device)
    model.eval()

    blocks = [block for page in payload["pages"] for block in page["blocks"]]
    total = len(blocks)
    for index, block in enumerate(blocks, 1):
        if block.get("translation"):
            continue
        source = str(block["source"])
        if block["kind"] == "author":
            block["translation"] = source
        else:
            chunks = split_for_marian(prepare_for_translation(source))
            translated_chunks: list[str] = []
            for start in range(0, len(chunks), 6):
                batch = chunks[start : start + 6]
                encoded = tokenizer(batch, return_tensors="pt", padding=True).to(device)
                with torch.inference_mode():
                    generated = model.generate(**encoded, num_beams=3, max_length=512)
                translated_chunks.extend(tokenizer.batch_decode(generated, skip_special_tokens=True))
            block["translation"] = " ".join(piece.strip() for piece in translated_chunks if piece.strip())
        save_json(json_path, payload)
        print(
            f"[{index:03d}/{total:03d}] {block['kind']} - {len(source)} caractères - {device}",
            flush=True,
        )


def french_cleanup(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"(?:\.\s*){4,}", "", text)
    text = text.replace(" ,", ",").replace(" .", ".")
    text = re.sub(r"\s*([;:!?])", "\u00a0" + r"\1", text)
    replacements = {
        '"Some Thoughts on the Interesting"': "« Quelques pensées sur l’intéressant »",
        "Some Thoughts on the Interesting": "Quelques pensées sur l’intéressant",
        "Thoughts on the Interesting": "Quelques pensées sur l’intéressant",
        "l'Intérêté": "l’« intéressant »",
        "L'Intérêté": "L’« intéressant »",
        "moral-philosophique": "de philosophie morale",
        "auto-compulsion": "contrainte exercée sur soi",
        "un travail de choses": "une œuvre des choses",
        "le phénomène de l'intéressant": "l’« intéressant »",
        "Le phénomène de l'intéressant": "L’« intéressant »",
        "du phénomène de l'intéressant": "de l’« intéressant »",
        "au phénomène de l'intéressant": "à l’« intéressant »",
        "des phénomènes de l'intéressant": "des formes de l’« intéressant »",
        "non utilitarienne": "non utilitaire",
        "auto-obligation": "contrainte exercée sur soi",
        "18ème siècle": "XVIIIe siècle",
        "Garves ♥Les pensées sur le phénomène du sujet qui l'intrigue": "Les « Pensées sur l’intéressant » de Garve",
        "budget de l'expérience": "fonds d’expérience",
        "fumabilité": "utilisabilité",
        "♥": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"([.])(?=[A-ZÀÂÉÈÊÎÔÙÛÇ])", r"\1 ", text)
    return text


def render(payload: dict[str, object], pdf_path: Path) -> None:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer

    unfinished = [
        block
        for page in payload["pages"]
        for block in page["blocks"]
        if not block.get("translation")
    ]
    if unfinished:
        raise RuntimeError(f"{len(unfinished)} blocs ne sont pas traduits")

    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("ArticleSerif", str(font_dir / "Times New Roman.ttf")))
    pdfmetrics.registerFont(TTFont("ArticleSerif-Bold", str(font_dir / "Times New Roman Bold.ttf")))
    pdfmetrics.registerFont(TTFont("ArticleSerif-Italic", str(font_dir / "Times New Roman Italic.ttf")))
    pdfmetrics.registerFontFamily(
        "ArticleSerif",
        normal="ArticleSerif",
        bold="ArticleSerif-Bold",
        italic="ArticleSerif-Italic",
        boldItalic="ArticleSerif-Bold",
    )

    width, height = A4
    left, right, top, bottom = 23 * mm, 21 * mm, 21 * mm, 20 * mm
    frame = Frame(left, bottom, width - left - right, height - top - bottom, id="main")

    def page_decor(canvas, document) -> None:
        if document.page == 1:
            return
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#B9B3AA"))
        canvas.setLineWidth(0.35)
        canvas.line(left, 14.5 * mm, width - right, 14.5 * mm)
        canvas.setFont("ArticleSerif", 8.1)
        canvas.setFillColor(colors.HexColor("#6A655F"))
        canvas.drawString(left, 10.2 * mm, "Doris Bachmann-Medick - Garve et l’intéressant")
        canvas.drawRightString(width - right, 10.2 * mm, str(document.page - 1))
        canvas.restoreState()

    doc = BaseDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=left,
        rightMargin=right,
        topMargin=top,
        bottomMargin=bottom,
        title="Force d’attraction plutôt qu’intérêt personnel - traduction française de travail",
        author="Doris Bachmann-Medick",
        subject="Traduction française de travail de l’étude consacrée à Garve et à l’intéressant",
    )
    doc.addPageTemplates([PageTemplate(id="article", frames=[frame], onPage=page_decor)])

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "ArticleTitle",
        parent=styles["Title"],
        fontName="ArticleSerif-Bold",
        fontSize=23,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2A2825"),
        spaceAfter=7 * mm,
    )
    subtitle = ParagraphStyle(
        "ArticleSubtitle",
        parent=styles["Normal"],
        fontName="ArticleSerif",
        fontSize=13.5,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#514B45"),
    )
    meta = ParagraphStyle(
        "ArticleMeta",
        parent=styles["Normal"],
        fontName="ArticleSerif",
        fontSize=9.3,
        leading=13,
        textColor=colors.HexColor("#4C4842"),
        spaceAfter=3 * mm,
    )
    warning = ParagraphStyle(
        "ArticleWarning",
        parent=meta,
        borderColor=colors.HexColor("#B39463"),
        borderWidth=0.6,
        borderPadding=8,
        backColor=colors.HexColor("#F7F2E8"),
        leading=13.5,
    )
    body = ParagraphStyle(
        "ArticleBody",
        parent=styles["BodyText"],
        fontName="ArticleSerif",
        fontSize=10.25,
        leading=14.35,
        alignment=TA_JUSTIFY,
        firstLineIndent=5 * mm,
        textColor=colors.HexColor("#252321"),
        spaceAfter=3.2 * mm,
        allowWidows=0,
        allowOrphans=0,
    )
    heading = ParagraphStyle(
        "ArticleHeading",
        parent=styles["Heading1"],
        fontName="ArticleSerif-Bold",
        fontSize=15.3,
        leading=19,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#302C27"),
        spaceBefore=7 * mm,
        spaceAfter=4 * mm,
        keepWithNext=True,
    )
    notes = ParagraphStyle(
        "ArticleNotes",
        parent=body,
        fontSize=8.55,
        leading=11.35,
        firstLineIndent=0,
        leftIndent=6 * mm,
        textColor=colors.HexColor("#514D47"),
        borderColor=colors.HexColor("#D2CDC5"),
        borderWidth=0,
        borderPadding=0,
    )
    page_marker = ParagraphStyle(
        "ArticlePageMarker",
        parent=styles["Normal"],
        fontName="ArticleSerif-Italic",
        fontSize=7.8,
        leading=9,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#8A837A"),
        spaceBefore=1.5 * mm,
        spaceAfter=2 * mm,
    )

    story = [
        Spacer(1, 24 * mm),
        Paragraph("Doris Bachmann-Medick", subtitle),
        Spacer(1, 12 * mm),
        Paragraph("Force d’attraction<br/>plutôt qu’intérêt personnel", title),
        Paragraph("La conception non utilitariste de « l’intéressant »<br/>chez Christian Garve", subtitle),
        Spacer(1, 8 * mm),
        Paragraph("L’intérêt dans le contexte de l’expérience esthétique", subtitle),
        Spacer(1, 24 * mm),
        Paragraph(
            "<b>Traduction française de travail.</b> Traduction automatique locale allemand-français, "
            "non révisée par l’autrice. Elle convient au repérage conceptuel, mais les citations et nuances "
            "philologiques doivent être contrôlées sur le texte allemand.",
            warning,
        ),
        Spacer(1, 7 * mm),
        Paragraph(
            "Source : Doris Bachmann-Medick, <i>Anziehungskraft statt Selbstinteresse. Christian Garves "
            "nicht-utilitarische Konzeption des « Interessierenden »</i>, version en ligne, 2008, 29 p.",
            meta,
        ),
        Paragraph(f'<link href="{SOURCE_URL}" color="#68523A">{SOURCE_URL}</link>', meta),
        Paragraph("Document préparé le 6 août 2026.", meta),
        PageBreak(),
    ]

    for page in payload["pages"]:
        story.append(Paragraph(f"[original allemand, p.&nbsp;{page['source_page']}]", page_marker))
        for block in page["blocks"]:
            if block["kind"] in {"author", "title"}:
                continue
            translated = french_cleanup(str(block["translation"]))
            safe = html.escape(translated).replace("&lt;br/&gt;", "<br/>")
            if block["kind"] == "heading":
                story.append(Paragraph(safe, heading))
            elif block["kind"] == "notes":
                story.append(Spacer(1, 1.5 * mm))
                story.append(Paragraph(safe, notes))
            else:
                story.append(Paragraph(safe, body))

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("extract", "translate", "translate-marian", "render"))
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--text", type=Path, default=DEFAULT_TEXT)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()

    if args.mode == "extract":
        payload = extract(args.source, args.text)
        save_json(args.json, payload)
        count = sum(len(page["blocks"]) for page in payload["pages"])
        print(f"{count} blocs extraits dans {args.json}")
    elif args.mode in {"translate", "translate-marian"}:
        payload = json.loads(args.json.read_text(encoding="utf-8")) if args.json.exists() else extract(args.source, args.text)
        save_json(args.json, payload)
        if args.mode == "translate-marian":
            translate_payload_marian(payload, args.json)
        else:
            translate_payload(payload, args.json)
    else:
        payload = json.loads(args.json.read_text(encoding="utf-8"))
        render(payload, args.pdf)
        print(args.pdf)


if __name__ == "__main__":
    main()
