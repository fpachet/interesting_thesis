#!/usr/bin/env python3
"""Extract, machine-translate, and typeset Garve's 1779 essay.

The script deliberately separates translation from rendering so that the local
Argos Translate environment can produce the JSON and the bundled document
runtime can render it with ReportLab.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_XML = Path("/tmp/garve_sammlung_1779.xml")
DEFAULT_JSON = ROOT / "tmp/pdfs/garve_interessirende_translation.json"
DEFAULT_PDF = ROOT / "output/pdf/garve-quelques-pensees-sur-l-interessant-traduction-de-travail.pdf"
SOURCE_URL = "https://www.deutschestextarchiv.de/book/show/garve_sammlung_1779"

BLOCK_TAGS = {"p", "head", "item"}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalize_historical_german(text: str) -> str:
    replacements = {
        "ſ": "s",
        "aͤ": "ä",
        "Aͤ": "Ä",
        "oͤ": "ö",
        "Oͤ": "Ö",
        "uͤ": "ü",
        "Uͤ": "Ü",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"-\s*\n\s*", "", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    return text.strip()


def extract_blocks(xml_path: Path) -> list[dict[str, object]]:
    root = ET.parse(xml_path).getroot()
    body = next((node for node in root.iter() if local_name(node.tag) == "body"), root)
    state: dict[str, object] = {"active": False, "page": None}
    blocks: list[dict[str, object]] = []

    def append_text(buffer: list[str], value: str | None) -> None:
        if value:
            buffer.append(value)

    def collect(node: ET.Element, buffer: list[str], skip_notes: bool = True) -> None:
        tag = local_name(node.tag)
        if tag == "pb":
            page = node.attrib.get("n")
            state["page"] = page
            state["active"] = page is not None and page.isdigit() and 253 <= int(page) < 440
            return
        if tag == "fw":
            return
        if tag == "note" and skip_notes:
            return
        if tag == "lb":
            buffer.append("\n")
            return
        append_text(buffer, node.text)
        for child in node:
            collect(child, buffer, skip_notes=skip_notes)
            append_text(buffer, child.tail)

    def walk(node: ET.Element, inside_block: bool = False) -> None:
        tag = local_name(node.tag)
        if tag == "pb":
            collect(node, [])
            return
        if tag == "fw":
            return
        if tag in BLOCK_TAGS and not inside_block and state["active"]:
            start_page = state["page"]
            buffer: list[str] = []
            collect(node, buffer)
            text = normalize_historical_german("".join(buffer))
            if text:
                blocks.append(
                    {
                        "kind": "heading" if tag == "head" else "note" if tag == "item" else "paragraph",
                        "page": int(start_page) if start_page else None,
                        "source": text,
                        "translation": None,
                    }
                )
            for note in (descendant for descendant in node.iter() if local_name(descendant.tag) == "note"):
                note_buffer: list[str] = []
                collect(note, note_buffer, skip_notes=False)
                note_text = normalize_historical_german("".join(note_buffer))
                if note_text:
                    blocks.append(
                        {
                            "kind": "note",
                            "page": int(start_page) if start_page else None,
                            "source": note_text,
                            "translation": None,
                        }
                    )
            return
        for child in node:
            walk(child, inside_block)

    walk(body)
    return blocks


def save_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def split_for_translation(text: str, limit: int = 1450) -> list[str]:
    if len(text) <= limit:
        return [text]
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ])", text)
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if not current:
            current = sentence
        elif len(current) + 1 + len(sentence) <= limit:
            current += " " + sentence
        else:
            chunks.append(current)
            current = sentence
    if current:
        chunks.append(current)
    return chunks


def translate_blocks(xml_path: Path, json_path: Path) -> None:
    from argostranslate import translate

    if json_path.exists():
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        blocks = payload["blocks"]
    else:
        blocks = extract_blocks(xml_path)
        payload = {
            "title": "Quelques pensées sur l’intéressant",
            "author": "Christian Garve",
            "source_edition": "Sammlung einiger Abhandlungen, Leipzig, 1779, p. 253–439",
            "source_url": SOURCE_URL,
            "blocks": blocks,
        }
        save_json(json_path, payload)

    total = len(blocks)
    for index, block in enumerate(blocks):
        if block.get("translation"):
            continue
        source = str(block["source"])
        translated_chunks = [translate.translate(chunk, "de", "fr") for chunk in split_for_translation(source)]
        translation_text = " ".join(part.strip() for part in translated_chunks if part.strip())
        block["translation"] = translation_text or "[Traduction non produite]"
        save_json(json_path, payload)
        print(f"[{index + 1:03d}/{total:03d}] p. {block.get('page')} — {len(source)} caractères", flush=True)


def french_cleanup(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace(" ,", ",").replace(" .", ".")
    text = re.sub(r"\s*([;:!?])", "\u00a0" + r"\1", text)
    text = text.replace("--", "—")
    return text


def render_pdf(json_path: Path, pdf_path: Path) -> None:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        KeepTogether,
        PageBreak,
        PageTemplate,
        Paragraph,
        Spacer,
    )

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    blocks = payload["blocks"]
    unfinished = [block for block in blocks if not block.get("translation")]
    if unfinished:
        raise RuntimeError(f"{len(unfinished)} blocs ne sont pas encore traduits")

    font_dir = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("GarveSerif", str(font_dir / "Times New Roman.ttf")))
    pdfmetrics.registerFont(TTFont("GarveSerif-Bold", str(font_dir / "Times New Roman Bold.ttf")))
    pdfmetrics.registerFont(TTFont("GarveSerif-Italic", str(font_dir / "Times New Roman Italic.ttf")))
    pdfmetrics.registerFontFamily(
        "GarveSerif",
        normal="GarveSerif",
        bold="GarveSerif-Bold",
        italic="GarveSerif-Italic",
        boldItalic="GarveSerif-Bold",
    )

    page_width, page_height = A4
    left = 24 * mm
    right = 22 * mm
    top = 22 * mm
    bottom = 20 * mm
    frame = Frame(left, bottom, page_width - left - right, page_height - top - bottom, id="main")

    class GarveDocTemplate(BaseDocTemplate):
        pass

    doc = GarveDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=left,
        rightMargin=right,
        topMargin=top,
        bottomMargin=bottom,
        title="Quelques pensées sur l’intéressant — Christian Garve",
        author="Christian Garve",
        subject="Traduction française de travail de Einige Gedanken über das Interessirende (1779)",
    )

    def page_decor(canvas, document) -> None:
        if document.page == 1:
            return
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#B9B3AA"))
        canvas.setLineWidth(0.35)
        canvas.line(left, 14.5 * mm, page_width - right, 14.5 * mm)
        canvas.setFont("GarveSerif", 8.2)
        canvas.setFillColor(colors.HexColor("#6A655F"))
        canvas.drawString(left, 10.3 * mm, "Christian Garve — Quelques pensées sur l’intéressant")
        canvas.drawRightString(page_width - right, 10.3 * mm, str(document.page - 1))
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="essay", frames=[frame], onPage=page_decor)])

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleGarve",
        parent=styles["Title"],
        fontName="GarveSerif-Bold",
        fontSize=25,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2A2825"),
        spaceAfter=9 * mm,
    )
    author = ParagraphStyle(
        "AuthorGarve",
        parent=styles["Normal"],
        fontName="GarveSerif",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#5A554E"),
    )
    meta = ParagraphStyle(
        "MetaGarve",
        parent=styles["Normal"],
        fontName="GarveSerif",
        fontSize=9.4,
        leading=13,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#4B4741"),
        spaceAfter=3 * mm,
    )
    warning = ParagraphStyle(
        "WarningGarve",
        parent=meta,
        borderColor=colors.HexColor("#B39463"),
        borderWidth=0.6,
        borderPadding=8,
        backColor=colors.HexColor("#F7F2E8"),
        leading=13.5,
    )
    body = ParagraphStyle(
        "BodyGarve",
        parent=styles["BodyText"],
        fontName="GarveSerif",
        fontSize=10.35,
        leading=14.4,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#252321"),
        firstLineIndent=5 * mm,
        spaceAfter=3.1 * mm,
        allowWidows=0,
        allowOrphans=0,
    )
    heading = ParagraphStyle(
        "HeadingGarve",
        parent=styles["Heading1"],
        fontName="GarveSerif-Bold",
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#302C27"),
        spaceBefore=7 * mm,
        spaceAfter=5 * mm,
        keepWithNext=True,
    )
    small_note = ParagraphStyle(
        "NoteGarve",
        parent=body,
        fontName="GarveSerif-Italic",
        fontSize=9.2,
        leading=12.6,
        firstLineIndent=0,
        leftIndent=8 * mm,
        rightIndent=8 * mm,
        textColor=colors.HexColor("#5A554E"),
    )
    page_marker = ParagraphStyle(
        "PageMarkerGarve",
        parent=styles["Normal"],
        fontName="GarveSerif-Italic",
        fontSize=7.8,
        leading=9,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#8A837A"),
        spaceBefore=1.5 * mm,
        spaceAfter=1.5 * mm,
    )

    story = [
        Spacer(1, 30 * mm),
        Paragraph("Christian Garve", author),
        Spacer(1, 12 * mm),
        Paragraph("Quelques pensées<br/>sur l’intéressant", title),
        Paragraph("<i>Einige Gedanken über das Interessirende</i> (1779)", author),
        Spacer(1, 27 * mm),
        Paragraph(
            "<b>Traduction française de travail.</b> Version produite automatiquement par traduction "
            "locale allemand–anglais–français, sans révision philologique exhaustive. Elle vise la "
            "lecture et le repérage conceptuel&nbsp;; toute citation savante doit être contrôlée sur "
            "l’original allemand.",
            warning,
        ),
        Spacer(1, 8 * mm),
        Paragraph(
            "Texte source&nbsp;: Christian Garve, <i>Sammlung einiger Abhandlungen aus der Neuen "
            "Bibliothek der schönen Wissenschaften und der freyen Künste</i>, Leipzig, 1779, "
            "p.&nbsp;253–439. Transcription du Deutsches Textarchiv.",
            meta,
        ),
        Paragraph(
            f'<link href="{SOURCE_URL}" color="#68523A">{SOURCE_URL}</link>',
            meta,
        ),
        Paragraph("Document préparé le 4 août 2026.", meta),
        PageBreak(),
    ]

    last_source_page = None
    first_heading = True
    for block in blocks:
        page = block.get("page")
        if page != last_source_page and page is not None:
            story.append(Paragraph(f"[édition de 1779, p.&nbsp;{page}]", page_marker))
            last_source_page = page
        translated = french_cleanup(str(block["translation"]))
        safe = html.escape(translated).replace("\n", "<br/>")
        kind = block["kind"]
        if kind == "heading":
            if not first_heading:
                story.append(Spacer(1, 2 * mm))
            story.append(Paragraph(safe, heading))
            first_heading = False
        elif kind == "note":
            story.append(KeepTogether([Paragraph(safe, small_note), Spacer(1, 1.5 * mm)]))
        else:
            story.append(Paragraph(safe, body))

    story.extend(
        [
            Spacer(1, 8 * mm),
            Paragraph("Fin de la traduction de travail", heading),
            Paragraph(
                "Les repères de page entre crochets renvoient au début des paragraphes dans "
                "l’édition de 1779. Les graphies historiques ont été normalisées avant traduction, "
                "notamment le s long et les trémas typographiques.",
                meta,
            ),
        ]
    )

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("extract", "translate", "render"))
    parser.add_argument("--xml", type=Path, default=DEFAULT_XML)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()

    if args.mode == "extract":
        blocks = extract_blocks(args.xml)
        payload = {
            "title": "Quelques pensées sur l’intéressant",
            "author": "Christian Garve",
            "source_edition": "Sammlung einiger Abhandlungen, Leipzig, 1779, p. 253–439",
            "source_url": SOURCE_URL,
            "blocks": blocks,
        }
        save_json(args.json, payload)
        print(f"{len(blocks)} blocs extraits dans {args.json}")
    elif args.mode == "translate":
        translate_blocks(args.xml, args.json)
    else:
        render_pdf(args.json, args.pdf)
        print(args.pdf)


if __name__ == "__main__":
    main()
