#!/usr/bin/env python3
"""Generate the offline reading packet for the thesis research programme."""

from __future__ import annotations

import re
from html import escape
from pathlib import Path

from lxml import html
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp" / "pdfs"
OUT = ROOT / "output" / "pdf" / "lecteur-avion-interessant-fr.pdf"

INK = colors.HexColor("#15243A")
MUTED = colors.HexColor("#637083")
PAPER = colors.HexColor("#FAF8F2")
BLUE = colors.HexColor("#234A73")
CORAL = colors.HexColor("#D96C55")
PALE_BLUE = colors.HexColor("#E8EEF4")
PALE_CORAL = colors.HexColor("#F7E8E2")
RULE = colors.HexColor("#CFD5DC")


def register_fonts() -> tuple[str, str, str]:
    candidates = [
        (
            "/System/Library/Fonts/Supplemental/Georgia.ttf",
            "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
            "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
        ),
        (
            "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
        ),
    ]
    for regular, bold, italic in candidates:
        if all(Path(p).exists() for p in (regular, bold, italic)):
            pdfmetrics.registerFont(TTFont("ReaderSerif", regular))
            pdfmetrics.registerFont(TTFont("ReaderSerifBold", bold))
            pdfmetrics.registerFont(TTFont("ReaderSerifItalic", italic))
            return "ReaderSerif", "ReaderSerifBold", "ReaderSerifItalic"
    return "Times-Roman", "Times-Bold", "Times-Italic"


REGULAR, BOLD, ITALIC = register_fonts()


class SectionMarker(Flowable):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def wrap(self, avail_width, avail_height):
        return 0, 0

    def draw(self):
        return


class CoverPage(Flowable):
    def __init__(self, height: float):
        super().__init__()
        self.height = height

    def wrap(self, avail_width, avail_height):
        return avail_width, min(self.height, avail_height)

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(INK)
        canvas.rect(-15 * mm, -14 * mm, A5[0], A5[1], stroke=0, fill=1)
        canvas.setFillColor(CORAL)
        canvas.rect(-15 * mm, -14 * mm, 7 * mm, A5[1], stroke=0, fill=1)
        x = 3 * mm
        top = self.height - 31 * mm
        canvas.setFont(BOLD, 8)
        canvas.setFillColor(colors.HexColor("#F4B8AA"))
        canvas.drawString(x, top, "PROGRAMME DE LECTURE · HORS LIGNE")
        canvas.setFont(BOLD, 25)
        canvas.setFillColor(colors.white)
        canvas.drawString(x, top - 19 * mm, "L'intéressant")
        canvas.setFont(REGULAR, 14)
        canvas.setFillColor(colors.HexColor("#DDE7F1"))
        canvas.drawString(x, top - 31 * mm, "Lecteur de voyage")
        text = canvas.beginText(x, top - 48 * mm)
        text.setFont(REGULAR, 10)
        text.setLeading(14)
        for line in (
            "Traductions françaises de travail, dossiers de lecture",
            "et feuilles d'extraction pour les dix séances",
            "du programme de recherche.",
        ):
            text.textLine(line)
        canvas.drawText(text)
        canvas.setFont(BOLD, 8)
        canvas.setFillColor(colors.HexColor("#F4B8AA"))
        canvas.drawString(x, 10 * mm, "VERSION DU 4 AOÛT 2026")
        canvas.restoreState()


class ReaderDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, **kwargs)
        self.running_section = "Mode d'emploi"
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="body",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(PageTemplate(id="reader", frames=[frame], onPage=self._page))

    def _page(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(PAPER)
        canvas.rect(0, 0, A5[0], A5[1], stroke=0, fill=1)
        if doc.page > 1:
            canvas.setStrokeColor(RULE)
            canvas.setLineWidth(0.4)
            canvas.line(15 * mm, A5[1] - 12 * mm, A5[0] - 15 * mm, A5[1] - 12 * mm)
            canvas.setFont(REGULAR, 7.2)
            canvas.setFillColor(MUTED)
            canvas.drawString(15 * mm, A5[1] - 9.3 * mm, self.running_section[:56])
            canvas.drawRightString(A5[0] - 15 * mm, 9 * mm, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, SectionMarker):
            self.running_section = flowable.title
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            if style in {"H1", "H2", "H2Loose"}:
                level = 0 if style == "H1" else 1
                text = flowable.getPlainText()
                key = f"h{level}-{self.seq.nextf('heading')}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level, closed=False)
                self.notify("TOCEntry", (level, text, self.page, key))


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom", parent=base["Title"], fontName=BOLD, fontSize=25,
            leading=28, textColor=colors.white, alignment=TA_LEFT, spaceAfter=7 * mm,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"], fontName=REGULAR, fontSize=11,
            leading=15, textColor=colors.HexColor("#DDE7F1"), spaceAfter=4 * mm,
        ),
        "kicker": ParagraphStyle(
            "Kicker", parent=base["Normal"], fontName=BOLD, fontSize=8,
            leading=10, textColor=colors.HexColor("#F4B8AA"), tracking=1.3,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName=BOLD, fontSize=18,
            leading=22, textColor=BLUE, spaceBefore=3 * mm, spaceAfter=5 * mm,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName=BOLD, fontSize=13,
            leading=16, textColor=INK, spaceBefore=5 * mm, spaceAfter=2.5 * mm,
            keepWithNext=False,
        ),
        "h2loose": ParagraphStyle(
            "H2Loose", parent=base["Heading2"], fontName=BOLD, fontSize=13,
            leading=16, textColor=INK, spaceBefore=5 * mm, spaceAfter=2.5 * mm,
            keepWithNext=False,
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading3"], fontName=BOLD, fontSize=10.5,
            leading=13, textColor=CORAL, spaceBefore=3 * mm, spaceAfter=1.5 * mm,
            keepWithNext=False,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName=REGULAR, fontSize=9.3,
            leading=13.4, textColor=INK, alignment=TA_LEFT, spaceAfter=2.4 * mm,
            allowWidows=0, allowOrphans=0,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName=REGULAR, fontSize=7.8,
            leading=10.6, textColor=MUTED, spaceAfter=1.7 * mm,
        ),
        "extract": ParagraphStyle(
            "Extract", parent=base["BodyText"], fontName=REGULAR, fontSize=8.6,
            leading=12.4, textColor=INK, leftIndent=5 * mm, rightIndent=3 * mm,
            borderColor=CORAL, borderWidth=1.2, borderPadding=(2, 0, 2, 7),
            spaceAfter=3 * mm, allowWidows=0, allowOrphans=0,
        ),
        "question": ParagraphStyle(
            "Question", parent=base["BodyText"], fontName=ITALIC, fontSize=8.7,
            leading=12, textColor=BLUE, leftIndent=4 * mm, spaceAfter=2 * mm,
        ),
        "toc0": ParagraphStyle(
            "TOC0", parent=base["Normal"], fontName=BOLD, fontSize=9.5,
            leading=13, textColor=INK, leftIndent=0, firstLineIndent=0,
            spaceBefore=2 * mm,
        ),
        "toc1": ParagraphStyle(
            "TOC1", parent=base["Normal"], fontName=REGULAR, fontSize=8,
            leading=10.5, textColor=MUTED, leftIndent=5 * mm, firstLineIndent=0,
        ),
        "badge": ParagraphStyle(
            "Badge", parent=base["Normal"], fontName=BOLD, fontSize=7.2,
            leading=9, textColor=colors.white, alignment=TA_CENTER,
        ),
    }


S = styles()


def p(text: str, style: str = "body") -> Paragraph:
    return Paragraph(escape(text).replace("\n", "<br/>"), S[style])


def rich(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, S[style])


def heading(text: str, level: int = 1):
    style = "h1" if level == 1 else "h2" if level == 2 else "h3"
    return Paragraph(escape(text), S[style])


def loose_heading(text: str):
    return Paragraph(escape(text), S["h2loose"])


def badge(label: str, color=BLUE):
    t = Table([[p(label, "badge")]], colWidths=[38 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX", (0, 0), (-1, -1), 0, color),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
    ]))
    return t


def callout(title: str, body: str, color=PALE_BLUE):
    data = [[p(title, "h3")], [p(body, "small")]]
    t = Table(data, colWidths=[A5[0] - 30 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def bullets(items: list[str], style="body") -> list[Paragraph]:
    return [Paragraph("• " + escape(item), S[style]) for item in items]


def notes(lines=4):
    data = [[""] for _ in range(lines)]
    t = Table(data, colWidths=[A5[0] - 30 * mm], rowHeights=[7 * mm] * lines)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.35, RULE)]))
    return t


def clean_spaces(text: str) -> str:
    text = re.sub(r"(\w)[¬-]\s*\n\s*(\w)", r"\1\2", text)
    text = re.sub(r"¬\s*", "", text)
    text = text.replace("’", "'")
    return re.sub(r"\s+", " ", text).strip()


def html_paragraphs(name: str) -> list[str]:
    path = TMP / name
    doc = html.fromstring(path.read_bytes().decode("utf-8"))
    return [clean_spaces(node.text_content()) for node in doc.xpath("//main//p")]


def schopenhauer_extracts() -> list[str]:
    paragraphs = html_paragraphs("schopenhauer.html")
    # The page repeats the essay in a second container; the first 16 are complete.
    return paragraphs[:16]


def schlegel_extracts() -> list[tuple[str, list[str]]]:
    paragraphs = html_paragraphs("schlegel.html")
    return [
        ("L'idéal moderne : la force esthétique subjective", [paragraphs[i] for i in (6, 11, 12)]),
        ("Pourquoi il n'existe pas de maximum de l'intéressant", [paragraphs[44]]),
        ("Surenchère, piquant et choquant", [paragraphs[46], paragraphs[213]]),
    ]


def kierkegaard_extracts() -> list[tuple[str, str]]:
    raw = (TMP / "kierkegaard.txt").read_text(encoding="utf-8", errors="replace")
    start = raw.index("At gaae ud fra en Grundsætning")
    end = raw.index("Forførerens Dagbog", start)
    block = raw[start:end]
    block = re.sub(
        r"\n\s*\d+ af \d+ sider\s*\n\f?Kierkegaard, Søren, Søren Kierkegaards Skrifter, Bd\. 2,\s*\n",
        " ",
        block,
    )
    lines = []
    for line in block.splitlines():
        s = line.strip()
        if not s:
            lines.append("")
            continue
        if s.startswith("Kierkegaard, Søren,") or re.match(r"^\d+ af \d+ sider$", s):
            continue
        lines.append(s)
    paragraphs = [clean_spaces(x) for x in re.split(r"\n\s*\n", "\n".join(lines)) if clean_spaces(x)]
    wanted = [
        ("L'ennui comme principe de mouvement", "At gaae ud fra en Grundsætning"),
        ("Le mot d'ordre : changer, mais selon un principe", "Naar nu som ovenfor udviklet"),
        ("La fausse rotation : changer sans fin de terrain", "Min Afvigelse fra den almindelige"),
        ("La vraie rotation : intensifier sous contrainte", "Den Methode, jeg foreslaaer"),
        ("Le même rapport revient autrement", "Men fordi man afholder sig fra Venskab"),
        ("Se varier soi-même", "Som man nu, ifølge den sociale"),
        ("L'arbitraire comme technique du regard", "I Vilkaarligheden ligger hele Hemmeligheden"),
    ]
    result = []
    for title, prefix in wanted:
        match = next((x for x in paragraphs if x.startswith(prefix)), None)
        if match:
            result.append((title, match))
    return result


def whitehead_extract() -> str:
    raw = (TMP / "whitehead.txt").read_text(encoding="utf-8", errors="replace")
    start = raw.index("To  summarize  this  discussion")
    end = raw.index("SECTION  III", start)
    excerpt = raw[start:end].replace("SECTION II", "").replace("SECTION  II", "")
    excerpt = re.sub(r"\n\s*4\s*\n\s*396\s+PROCESS\s+AND\s+REALITY\s*\n", "\n", excerpt)
    excerpt = re.sub(r"\n\s*PROPOSITIONS\s+AND\s+FEELINGS\s+397\s*\n", "\n", excerpt)
    return clean_spaces(excerpt)


# Traductions françaises de travail réalisées pour ce lecteur. Elles facilitent
# l'annotation, mais les citations de thèse doivent être contrôlées dans les
# textes originaux et les éditions indiquées.
GARVE_FR = [
    (
        "L'attention, l'effort et la douce traction de l'objet — p. 253–255",
        [
            "Notre attention, qui se partage ordinairement entre plusieurs choses ou passe rapidement de l'une à l'autre, peut parfois être rassemblée sur un seul objet, ou sur un ensemble d'objets liés entre eux, de telle sorte que nous oublions le reste des choses qui agissent sur nous ou en nous. Elle peut parfois être retenue si fermement sur ces objets que, pendant un temps considérable, nous ne passons plus à d'autres objets.",
            "Ce rassemblement et cet arrêt de notre attention sur un seul objet exigent toujours une force extraordinaire qui les produise : soit la force de l'homme lui-même, soit celle des choses qui le touchent. Dans le premier cas, son attention se nomme effort; la chose vers laquelle elle se dirige, occupation; et l'action qui en résulte, travail. Dans l'autre cas, c'est soit la simple puissance et la violence de l'impression, soit sa nature déterminée, qui fixe notre attention. La première est une contrainte : la douleur, avec tout ce qui menace de douleur, rend ainsi l'âme attentive malgré elle. La seconde est cette douce traction par laquelle le plaisir — ou, plus généralement, tout ce qui entretient un rapport particulier avec notre état, nos pensées et nos inclinations — détourne l'œil de notre esprit des autres objets et le dirige vers soi.",
            "Tous les objets, ou toutes les manières de les représenter, qui, sans effort volontaire de notre part, s'emparent de notre attention par l'agrément qu'ils éveillent en nous et la rendent stable : voilà, pensons-nous, ce que le mot intéressant doit distinguer des autres espèces d'objets. Il doit désigner les choses qui nous rendent désireux de leurs représentations de la même manière et par les mêmes ressorts que ce qui nous rend attentifs à ce qui peut contribuer à satisfaire notre intérêt propre.",
        ],
    ),
    (
        "Quand le contenu remplace le but extérieur — p. 255–257",
        [
            "Cette différence entre l'attention dont nous sommes nous-mêmes les auteurs et celle qui est l'œuvre des objets apparaît dans les occupations les plus communes de la vie. Supposons que l'on lise un ouvrage de généalogie ou de diplomatique. Il se peut que nous le lisions avec toute notre attention; mais nous avons alors conscience de l'effort qu'il nous coûte, des distractions qu'il faut repousser à chaque instant et de la résistance qu'il faut opposer à d'autres idées plus séduisantes qui cherchent à s'introduire. Ce ne sont pas les choses que nous lisons qui maintiennent l'âme dirigée vers elles, mais notre désir d'apprendre, notre devoir ou le but pour lequel ces informations nous sont nécessaires. Nous ne sommes pas attirés : nous nous plaçons nous-mêmes devant la chose et nous contraignons à y demeurer. Nous ne dirons jamais, dans ce cas, que le livre est intéressant; nous dirons seulement que nous travaillons avec application.",
            "Supposons au contraire qu'un autre ouvrage, commencé lui aussi par devoir ou par contrainte, contienne des récits, des descriptions et des discours qui, à mesure que nous avançons, nous fassent peu à peu oublier l'intention première pour laquelle nous lisions et nous occupent seulement des choses mêmes que nous découvrons à chaque instant. Supposons que le désir, d'abord dirigé vers une fin éloignée et vers la lecture comme simple moyen, se porte désormais sur le contenu même du livre : nous lisons alors uniquement pour savoir ce qui est dit et ce qui va suivre, sans penser davantage à un usage ultérieur. Nous demeurerons très attentifs, peut-être plus qu'auparavant, mais sans avoir conscience d'aucun effort pour conserver notre attention. La force qui arrête la mobilité naturelle de l'âme n'est plus notre résolution, mais l'impression des objets. Nous disons alors : le livre commence à nous intéresser.",
        ],
    ),
    (
        "Être déjà en avant de l'idée présente — p. 257–260",
        [
            "Un autre caractère distingue encore ces deux espèces d'attention; et c'est précisément celui auquel on pense lorsqu'on parle d'intéresser. Lorsque je demeure par simple résolution, avec mes pensées, dans une série déterminée de choses, je ne m'arrête à chaque instant qu'au membre actuellement présent de cette série et ne me soucie pas des suivants. J'interromps la série dès que mon but est atteint ou que le temps du travail est achevé, sans être le moins du monde inquiet de ce qui suivra.",
            "Lorsque, au contraire, je parcours cette série par la force attractive des objets eux-mêmes, mon attention est toujours déjà un peu en avant de l'idée présente. En considérant les membres actuels, je désire les suivants; et je ne peux m'arrêter paisiblement avant que la série ne soit parvenue à son terme ou à un point d'interruption. Dire qu'un spectacle ou un roman m'intéresse et dire que j'ai envie d'en connaître l'issue sont des expressions équivalentes. Le signe le plus sûr qu'un dramaturge a atteint son but d'intéresser est qu'il place le spectateur dans le désir et l'attente inquiète de l'avenir.",
            "Le désir de l'âme porte proprement toujours sur quelque chose de futur. S'il ne porte pas sur la chose même qui nous occupe, mais sur une fin extérieure qui doit seulement être atteinte par son moyen, rien, en dehors de la partie présente de la chose, ne reste devant nos yeux que cette fin. Là où le désir porte au contraire sur les choses mêmes auxquelles notre attention s'applique, il se dirige proprement vers leurs parties suivantes, puisque les parties présentes sont déjà goûtées. La satisfaction même que le présent procure à l'âme tourne son regard vers l'avenir afin d'y chercher de nouvelles satisfactions.",
            "Ainsi, tout ce qui, par l'impression d'agrément qu'il produit sur nous, nous maintient attentifs sans dessein de notre part et désireux de la continuation et de la suite nous intéresse. Tout agrément naît soit de ce qui occupe notre faculté de penser, soit de ce qui éveille nos sentiments. Celui qui veut nous intéresser doit nous donner beaucoup à penser ou nous mettre en mouvement affectivement.",
        ],
    ),
    (
        "Une difficulté doit avoir été éprouvée auparavant — p. 266–269",
        [
            "Il faut d'abord expliquer comment certaines idées acquièrent un rapport plus étroit avec la situation d'un homme, puis de combien de manières de tels rapports peuvent se former. On l'éprouve déjà dans l'enseignement des sciences abstraites. Si quelqu'un écoute ou lit un maître sur des matières au sujet desquelles il n'a jamais été conduit à réfléchir lui-même, seules la clarté et l'évidence des choses exposées, jointes à son propre goût pour la science, peuvent le gagner à ce qu'il entend et produire une certaine participation aux recherches entreprises. Même alors, il est presque certain qu'il laissera passer beaucoup de choses qui lui paraîtront indifférentes, bien qu'elles appartiennent immédiatement au dessein de l'orateur, et qu'il recueillera comme un gain beaucoup de choses insignifiantes qui ne servent que d'idées accessoires ou de remplissage.",
            "La nature veut que l'on suive, pour apprendre la vérité, le même chemin qu'elle suit pour la découvrir, si cette vérité doit produire son impression. De même que nous ne cherchons pas d'explication d'un phénomène avant d'en avoir été étonnés, et que presque toutes nos recherches sont entreprises pour résoudre des difficultés qui nous avaient auparavant inquiétés, de même, pour trouver de l'intérêt à ces explications et à ces solutions lorsqu'elles ont été découvertes par d'autres et nous sont présentées, il faut avoir fait au moins en passant les mêmes expériences et avoir perçu au moins obscurément les mêmes difficultés.",
            "Toute pensée rencontrée dans le discours ou l'écrit d'autrui, dont nous reconnaissons la vérité sans en sentir l'usage ni en apercevoir la visée, nous touche peu. Cet usage et cette visée ne peuvent consister que dans la lumière et la certitude que cette pensée répand sur d'autres pensées déjà possédées, qui nous avaient paru importantes mais dans lesquelles subsistaient encore obscurité ou doute; ou dans les règles et les secours qu'elle nous fournit pour des opérations qui nous importent et dans lesquelles nous ne pouvions avancer. Il faut donc avoir d'abord eu ces autres idées et avoir éprouvé leurs lacunes ou leur manque de clarté; il faut avoir été engagé dans ces opérations et avoir été arrêté par le défaut de ces connaissances, si l'on veut trouver dans l'enseignement l'intérêt fondé sur l'éclaircissement de ces obscurités et la réparation de ce manque.",
            "Ce n'est pas le bien en lui-même, dit Locke, qui éveille le désir, mais seulement le bien qui manque actuellement à l'achèvement de notre état : celui dont l'absence produit, dans notre constitution présente, une lacune qui nous inquiète. Le rapport que le bien entretient avec le désir, l'intéressant l'entretient avec l'entendement. Toute idée vraie, grande ou belle ne nous rend pas attentifs; seule le fait l'idée qui manque encore à la série des idées déjà présentes en nous et remarquées par nous, celle qui remplit une lacune aperçue dans nos connaissances et apaise une certaine inquiétude éprouvée à propos de notre ignorance sur ce point.",
        ],
    ),
    (
        "Les séries mentales et les matériaux déjà présents — p. 269–274",
        [
            "Nous voyons ainsi comment l'état antérieur de l'homme — la somme de ce qu'il a jusqu'ici éprouvé, senti et pensé — peut déterminer parmi les idées nouvelles celles auxquelles il prendra le plus de goût, celles qu'il s'appropriera le plus rapidement et celles auprès desquelles son attention s'arrêtera.",
            "À mesure que les désirs se développent, que leurs objets reviennent plus souvent et dans de nouvelles liaisons, les idées s'étendent et en engendrent d'autres. Beaucoup se rassemblent en certaines séries dont chaque membre éveille la prévision et le désir des autres; beaucoup s'unissent en certains touts qui se présentent à l'âme d'un seul coup et dans lesquels elle apprend, à partir de ce qui est présent, à sentir ce qui manque. Le flux toujours continu des objets et des événements extérieurs et intérieurs y ajoute de nouveaux concepts, fortifie ou modifie les anciens. Les objets nouveaux ne peuvent alors plus ébranler l'âme de manières entièrement nouvelles : s'ils veulent produire une impression, ils doivent en quelque sorte entrer dans les traces des anciens. L'âme ne reçoit plus tout ce qui s'offre à elle; elle cherche ce qui se rattache aux séries ou s'insère dans les ensembles qui se sont formés en elle et selon lesquels elle doit ordonner tout ce qui peut devenir pensable et sensible pour elle.",
            "En outre, chaque événement qui arrive à l'homme, chaque état dans lequel il tombe, dépose dans sa mémoire une certaine matière qui doit être travaillée; chaque idée qu'il reçoit le prépare à une idée nouvelle ou en contient la semence. Ce qui se construit à partir des matériaux déjà présents en lui, ce qui germe et mûrit à partir de cette semence déposée en lui, est pour lui beaucoup plus important, lui appartient beaucoup davantage, porte sa tête à une activité beaucoup plus grande et échauffe bien davantage son imagination que ce qui est composé d'une matière entièrement étrangère et produit sur un sol étranger.",
            "Les idées et les descriptions acquièrent donc un rapport plus précis avec notre état de quatre manières au moins : premièrement, lorsqu'elles complètent ce que nous savons déjà à moitié, nous font penser clairement ce que nous avions senti obscurément ou nous donnent à voir dans un cas singulier ce que nous avions appris en termes abstraits; deuxièmement, lorsqu'elles nous rappellent vivement quelque chose que nous avons nous-mêmes éprouvé avec plus ou moins d'émotion et nous permettent de revoir notre vie passée en comprenant ce qui nous avait alors échappé; troisièmement, lorsqu'elles nous fournissent un modèle ou une indication pour certaines affaires qui nous importent ou pour une conduite à laquelle nous aspirons; quatrièmement, lorsqu'elles nous provoquent à exercer nous-mêmes notre faculté de penser, en les reliant aux principes que nous connaissons, en les éclairant par les événements que nous avons vécus, ou en cherchant une parenté — de ressemblance ou de dépendance — entre elles et nos expériences anciennes.",
        ],
    ),
    (
        "L'intérêt comme degré supérieur de vie — p. 313–317",
        [
            "L'intérêt qui naît des passions ne peut être entièrement séparé de celui qui naît des représentations, puisque celles-ci ne deviennent importantes et attirantes pour l'attention que dans la mesure où elles contiennent quelque chose qui excite les passions ou les flatte. On peut néanmoins distinguer la part que nous prenons aux manifestations de l'entendement d'autrui de celle que nous prenons aux mouvements de son cœur; autrement dit, l'intérêt éveillé par les raisonnements ou les descriptions de celui qu'éveillent les émotions ou les destinées.",
            "Nous exprimerions peut-être mieux encore la vérité visée par cette division en disant : l'état d'un homme intéressé par quelque chose est une veille plus complète, un degré supérieur de vie. Il consiste à nous sentir nous-mêmes plus vivement et à avoir davantage de désirs et d'attentes qu'à l'ordinaire. Mais quels désirs, et de quoi? Soit de certaines modifications des circonstances qui nous sont présentes dans la réalité ou dans la représentation, soit de certaines modifications de nos pensées elles-mêmes. Une chose nous intéresse ou bien parce qu'elle contribue à notre propre perfection — c'est l'intérêt produit par la clarté et la multiplicité des représentations — ou bien parce qu'elle améliore quelque chose dans notre situation.",
            "Dans les événements, l'intéressant est toujours quelque chose de futur : un danger qui s'approche, une joie que nous attendons. Si le père parti chercher son fils dans un lieu étranger le trouve mort, il est ému avec la plus grande vivacité; il est occupé, mais il n'est pas intéressé. Si, en arrivant dans la ville étrangère, ce même père entend parler d'un jeune homme qui ressemble à son fils et que l'on s'apprête à enterrer, alors il est intéressé au plus haut degré.",
            "Il faut, deuxièmement, qu'une certaine obscurité subsiste dans cet avenir. Il s'agit d'une attente incertaine liée au désir ou à l'aversion. Dès qu'une issue heureuse ou malheureuse devient certaine, l'occupation de l'âme et son inquiétude diminuent. Dites au joueur qu'il gagnera : il pourra s'en réjouir davantage, mais son âme sera moins active. Pourquoi? Parce que l'activité de l'âme consiste dans le désir et que le désir cesse lorsque la chose est atteinte. Or l'avenir est lui aussi atteint dès qu'il devient certain.",
            "Il existe, dans la vie quotidienne de l'homme le plus retiré et le plus tranquille, mille petits événements agréables dont l'attente, à certaines heures et à certains moments, lui donne davantage de vivacité. Il y a chez chaque homme de petites obscurités du futur prochain qui le placent dans une certaine inquiétude et dans un mouvement plus intense.",
        ],
    ),
]

SCHLEGEL_FR = [
    (
        "L'idéal moderne : la force esthétique subjective",
        [
            "Les amis de la poésie moderne ne prendront pas, je l'espère, l'introduction de l'essai sur l'étude de la poésie grecque pour mon jugement définitif sur la poésie moderne; du moins ne se hâteront-ils pas de conclure que mon goût est unilatéral. Je prends la poésie moderne au sérieux : depuis ma jeunesse, j'ai aimé plusieurs poètes modernes, j'en ai étudié beaucoup et je crois en connaître quelques-uns. Les penseurs exercés devineront aisément pourquoi j'ai dû choisir ce point de vue. S'il existe des lois pures de la beauté et de l'art, elles doivent valoir sans exception. Mais si l'on prend ces lois pures, sans détermination plus précise ni règle d'application, pour mesurer la poésie moderne, le jugement ne peut être que celui-ci : la poésie moderne, qui contredit presque partout ces lois, n'a absolument aucune valeur. Elle ne prétend même pas à l'objectivité, pourtant première condition de la valeur esthétique pure et inconditionnée; son idéal est l'intéressant, c'est-à-dire la force esthétique subjective. Voilà un jugement auquel le sentiment s'oppose avec force. On a déjà beaucoup gagné lorsqu'on ne se dissimule pas cette contradiction. C'est le plus court chemin pour découvrir le caractère propre de la poésie moderne, expliquer le besoin d'une poésie classique et, finalement, être surpris et récompensé par une éclatante justification des Modernes.",
            "Or, de l'avis même de la majorité des philosophes, l'un des caractères du beau est que le plaisir qu'il procure soit désintéressé. Quiconque admet que le concept du beau est pratique et spécifiquement distinct, même s'il ne le pose que comme problème et laisse indécises sa validité et son application, ne peut le nier. Le beau n'est donc pas l'idéal de la poésie moderne et il diffère essentiellement de l'intéressant.",
            "Dans tout le domaine des sciences esthétiques, la déduction de l'intéressant est peut-être la tâche la plus difficile et la plus embrouillée. Avant de justifier l'intéressant, il faut expliquer son origine et ce qui l'a suscité. Lorsque la culture naturelle accomplie des Anciens eut définitivement décliné et dégénéré sans remède, la perte de la réalité finie et la dissolution de la forme accomplie firent naître une aspiration à la réalité infinie, qui devint bientôt la tonalité générale de l'époque. Un même principe engendra les excès colossaux des Romains puis, après avoir vu ses espoirs déçus dans le monde sensible, l'étrange phénomène de la philosophie néoplatonicienne et la tendance générale de cette époque remarquable, où l'esprit humain semblait pris de vertige, vers une religion universelle et métaphysique. Les historiens perspicaces n'ont pas manqué le moment décisif de l'histoire morale romaine où le sens de la belle apparence et des jeux moraux disparut tout à fait, et où le genre humain descendit jusqu'à la réalité nue. Si l'on peut montrer que même la culture naturelle la plus heureuse, nécessairement limitée dans sa perfectibilité comme dans sa durée, ne peut satisfaire pleinement l'impératif esthétique; et si la culture esthétique artificielle, qui ne peut venir qu'après la dissolution complète de la culture naturelle et doit commencer là où celle-ci s'est arrêtée, c'est-à-dire avec l'intéressant, doit parcourir plusieurs degrés avant de parvenir à l'objectif et au beau suivant les lois d'une théorie objective et l'exemple de la poésie classique; alors il est également démontré que l'intéressant, comme préparation nécessaire à la perfectibilité infinie de la disposition esthétique, est esthétiquement permis. Car l'impératif esthétique est absolu; puisqu'il ne peut jamais être parfaitement accompli, la culture artificielle doit au moins s'en approcher indéfiniment. Selon cette déduction, qui fonde une science propre, la poétique appliquée, l'intéressant est ce qui possède une valeur esthétique provisoire. L'intéressant a certes nécessairement un contenu intellectuel ou moral; mais qu'il ait pour autant une valeur, j'en doute. Le bien doit être fait et le vrai connu, non représentés et ressentis. Je fais peu de cas d'une connaissance de l'homme puisée dans Shakespeare ou d'une vertu puisée dans Héloïse, quoi qu'en disent ceux qui aiment accumuler les recommandations en faveur de la poésie. Dans la poésie, l'intéressant ne possède donc jamais qu'une validité provisoire, comme le gouvernement despotique.",
        ],
    ),
    (
        "Pourquoi il n'existe pas de maximum de l'intéressant",
        [
            "Ce défaut d'universalité, cette domination du maniéré, du caractéristique et de l'individuel expliquent d'eux-mêmes l'orientation générale de la poésie, et même de toute la culture esthétique des Modernes, vers l'intéressant. Est intéressant tout individu original qui contient une quantité plus grande de contenu intellectuel ou d'énergie esthétique. Je dis à dessein : plus grande. Plus grande, en effet, que celle que possède déjà l'individu récepteur; car l'intéressant exige une réceptivité individuelle, et souvent même un état momentané de celle-ci. Puisque toute grandeur peut être augmentée à l'infini, on comprend pourquoi aucune satisfaction complète ne peut être atteinte par cette voie et pourquoi il n'existe pas d'intéressant suprême. Sous les formes et les orientations les plus diverses, à tous les degrés de force, le même besoin d'une satisfaction complète et la même aspiration à un maximum absolu de l'art se manifestent dans toute la masse de la poésie moderne. Ce que la théorie promettait, ce que l'on cherchait dans la nature et espérait trouver dans chaque idole particulière, qu'était-ce sinon un suprême esthétique? Plus le désir de satisfaction complète, enraciné dans la nature humaine, fut déçu par le particulier et le changeant, auxquels l'art s'était jusque-là exclusivement attaché, plus il devint violent et inquiet. Seuls l'universellement valable, le durable et le nécessaire — l'objectif — peuvent combler cette grande lacune; seul le beau peut apaiser cette ardente aspiration. Le beau — dont je ne pose ici le concept que problématiquement, en laissant pour l'instant indécises sa validité réelle et son applicabilité — est l'objet universellement valable d'un plaisir désintéressé, également indépendant de la contrainte du besoin et de celle de la loi, libre et pourtant nécessaire, entièrement sans fin et pourtant absolument conforme à une fin. L'excès de l'individuel conduit donc de lui-même à l'objectif; l'intéressant prépare le beau, et la fin ultime de la poésie moderne ne peut être autre que le beau suprême, un maximum de perfection esthétique objective.",
        ],
    ),
    (
        "Surenchère, piquant et choquant",
        [
            "La domination de l'intéressant n'est qu'une crise passagère du goût, car elle doit finalement se détruire elle-même. Mais les deux catastrophes entre lesquelles elle doit choisir sont de nature très différente. Si l'orientation se porte surtout vers l'énergie esthétique, le goût, de plus en plus habitué aux anciens excitants, n'en désirera que de plus violents et de plus aigus. Il passera bientôt au piquant et au frappant. Le piquant est ce qui excite convulsivement une sensibilité émoussée; le frappant est un aiguillon semblable pour l'imagination. Ce sont les signes avant-coureurs d'une mort prochaine. Le fade est la maigre nourriture de l'impuissant; le choquant — qu'il soit aventureux, répugnant ou horrible — est la dernière convulsion du goût mourant. Si, au contraire, le contenu philosophique prédomine dans la tendance du goût et si la nature est assez forte pour ne pas succomber aux secousses les plus violentes, la force d'aspiration, après s'être épuisée à produire une profusion excessive d'intéressant, se ressaisira avec violence et tentera de parvenir à l'objectif. C'est pourquoi, à notre époque, le goût authentique n'est ni un don de la nature ni le seul fruit de la culture : il n'est possible qu'à la condition d'une grande force morale et d'une ferme autonomie.",
            "Le choquant a trois sous-espèces : ce qui révolte l'imagination, l'aventureux; ce qui soulève les sens, le répugnant; ce qui tourmente et martyrise le sentiment, l'horrible. Cette évolution naturelle de l'intéressant explique très bien les voies différentes suivies par le meilleur art et par l'art commun.",
        ],
    ),
]


SCHOPENHAUER_FR = [
    "Dans les œuvres poétiques, notamment épiques et dramatiques, peut se rencontrer une propriété distincte de la beauté : l'intéressant. La beauté consiste en ce que l'œuvre d'art restitue clairement les Idées du monde en général, et la poésie, plus particulièrement, les Idées de l'homme, conduisant ainsi l'auditeur à leur connaissance. Pour y parvenir, la poésie met en scène des caractères significatifs et invente des événements qui produisent des situations riches de sens; ces situations amènent les caractères à déployer leurs particularités et à dévoiler leur intériorité, de sorte que cette représentation fait connaître plus clairement et plus complètement l'Idée multiforme de l'humanité. La beauté est, en général, la propriété inséparable de l'Idée devenue connaissable; est beau tout ce en quoi une Idée est connue, car être beau signifie précisément exprimer clairement une Idée. Nous voyons que la beauté relève toujours de la connaissance et s'adresse seulement au sujet connaissant, non à la volonté. Nous savons même que la saisie du beau suppose, chez le sujet, un silence complet de la volonté. Au contraire, nous appelons intéressant un drame ou un récit lorsque les événements et les actions représentés nous imposent une participation tout à fait semblable à celle que nous éprouvons devant des événements réels où notre propre personne se trouve engagée. Nous ressentons alors le destin des personnages comme le nôtre : nous attendons avec tension le développement des événements, nous en suivons avidement le cours, notre cœur bat réellement à l'approche du danger, notre pouls s'arrête lorsque celui-ci atteint son comble et s'accélère de nouveau lorsque le héros est soudain sauvé. Nous ne pouvons poser le livre avant d'être arrivés à la fin et veillons ainsi tard dans la nuit, prenant part aux inquiétudes de notre héros comme nous le ferions à nos propres soucis. À vrai dire, ces représentations nous feraient éprouver, au lieu de repos et de jouissance, toutes les peines que la vie réelle nous impose souvent, ou du moins celles d'un rêve angoissant, si le sol ferme de la réalité ne restait toujours à notre portée pendant la lecture ou au théâtre : dès qu'une souffrance trop vive nous atteint, nous pouvons nous y réfugier, interrompre à tout moment l'illusion, puis nous y abandonner de nouveau à volonté, sans le passage violent que suppose le réveil par lequel nous échappons enfin aux figures terrifiantes d'un cauchemar.",
    "Il est manifeste que ce qu'une poésie de cette espèce met en mouvement est notre volonté, et non la seule connaissance pure. Le mot « intéressant » désigne donc en général ce qui obtient la participation de la volonté individuelle, quod nostra interest. Ici le beau se sépare clairement de l'intéressant : le premier relève de la connaissance, et de la connaissance la plus pure; le second agit sur la volonté. En outre, le beau consiste dans la saisie des Idées, connaissance qui a quitté le principe de raison; l'intéressant, au contraire, naît toujours du cours des événements, c'est-à-dire d'enchaînements qui ne sont possibles que par le principe de raison sous ses diverses formes.",
    "La différence essentielle entre l'intéressant et le beau est maintenant claire. Nous avons reconnu dans le beau la fin propre de tout art, et donc aussi de la poésie. Il reste à demander si l'intéressant est peut-être une seconde fin de la poésie, un moyen de représenter le beau, un accident essentiel produit par lui et apparaissant de lui-même dès que le beau est présent, ou du moins quelque chose de compatible avec cette fin principale; ou bien, enfin, s'il lui est contraire et lui fait obstacle.",
    "Tout d'abord, l'intéressant ne se rencontre que dans les œuvres poétiques, non dans les arts plastiques, la musique ou l'architecture. Dans ceux-ci, on ne peut même pas le concevoir, sinon comme quelque chose de tout à fait individuel pour un ou quelques spectateurs : par exemple si le tableau est le portrait d'une personne aimée ou haïe, le bâtiment ma demeure ou ma prison, la musique la danse de mon mariage ou la marche sur laquelle je suis parti en campagne. Un intéressant de cette sorte est évidemment tout à fait étranger à l'essence et à la fin de l'art, et même perturbateur dans la mesure où il détourne entièrement de la contemplation artistique pure. Il pourrait se révéler que cela vaut, à un moindre degré, de tout intéressant.",
    "Puisque l'intéressant ne naît que lorsque notre participation à la représentation poétique devient semblable à celle que nous prenons à une réalité, il suppose évidemment que la représentation nous trompe pour un instant; elle ne le peut que par sa vérité. Or la vérité appartient à l'accomplissement de l'art. L'image ou le poème doit être vrai comme la nature elle-même; mais il doit en même temps, en faisant ressortir l'essentiel et le caractéristique, en concentrant toutes les manifestations essentielles de ce qui est représenté et en écartant l'inessentiel et l'accidentel, laisser apparaître son Idée à l'état pur et devenir ainsi une vérité idéale qui s'élève au-dessus de la nature. L'intéressant se rattache donc au beau par l'intermédiaire de la vérité, puisque celle-ci produit l'illusion. Mais le caractère idéal de la vérité pourrait déjà nuire à l'illusion, car il établit une différence constante entre poésie et réalité. Comme le réel peut cependant coïncider avec l'idéal, cette différence n'abolit pas nécessairement toute illusion. Dans les arts plastiques, la portée de leurs moyens impose une limite qui exclut l'illusion : la sculpture ne donne que la forme, sans couleur, sans yeux et sans mouvement; la peinture, qu'une vue prise d'un seul point, enfermée dans des limites nettes qui séparent le tableau de la réalité qui l'entoure immédiatement. L'illusion, et par conséquent une participation semblable à celle que suscite le réel — l'intéressant —, sont ainsi exclues; la volonté est aussitôt mise hors jeu et l'objet livré à la contemplation pure et sans participation. Il est très remarquable qu'une espèce bâtarde des arts plastiques franchisse ces limites, produise l'illusion du réel et, avec elle, l'intéressant, mais perde du même coup l'effet des arts authentiques et ne puisse plus servir à représenter le beau, c'est-à-dire à communiquer la connaissance des Idées : c'est l'art des figures de cire. Cette limite pourrait bien être celle qui l'exclut du domaine des beaux-arts. Lorsqu'une figure de cire est exécutée avec maîtrise, elle trompe parfaitement; mais, pour cette raison même, nous lui faisons face comme à un être humain réel qui, en tant que tel, est d'emblée un objet pour la volonté, donc intéressant : il éveille la volonté et abolit la connaissance pure. Nous nous approchons de la figure de cire avec la crainte et la prudence qu'inspire une personne réelle; notre volonté est excitée et attend de savoir si elle doit aimer ou haïr, fuir ou attaquer; elle attend une action. Mais, puisque la figure reste inanimée, elle produit l'impression d'un cadavre et devient déplaisante. L'intéressant est ici parfaitement atteint sans qu'aucune œuvre d'art ait été produite : l'intéressant n'est donc pas en lui-même une fin de l'art. Cela ressort aussi du fait que, même en poésie, seuls le drame et le récit peuvent être intéressants. Si l'intéressant était, à côté du beau, une fin de l'art, la poésie lyrique serait déjà, de ce seul fait, inférieure de moitié aux deux autres genres.",
    "Passons à la seconde question. Si l'intéressant était un moyen d'atteindre le beau, toute poésie intéressante devrait également être belle. Ce n'est nullement le cas. Il arrive souvent qu'un drame ou un roman nous captive par son intérêt tout en étant si dépourvu de beauté que nous avons ensuite honte d'y avoir consacré du temps. C'est le cas de maint drame qui ne donne aucune image pure de l'essence de l'humanité et de la vie, présente des caractères décrits de façon plate, voire défigurés, qui sont à proprement parler des monstruosités contraires à l'essence de la nature; mais le cours des événements et les enchevêtrements de l'action sont si compliqués, la situation du héros le recommande tellement à notre cœur, que nous ne pouvons nous satisfaire avant d'avoir vu le nœud se défaire et le héros mis en sûreté. Le cours de l'action est conduit avec tant d'adresse que nous restons tendus vers la suite sans pouvoir la deviner; entre tension et surprise, notre participation demeure vive et, agréablement divertis, nous ne sentons pas le temps passer. Telles sont la plupart des pièces de Kotzebue. C'est exactement ce qu'il faut au grand public, qui cherche divertissement et passe-temps, non connaissance. Or le beau relève de la connaissance; la réceptivité au beau varie donc autant que les facultés intellectuelles. Le grand public n'a aucun sens de la vérité intérieure de ce qui est représenté, de son accord ou de son opposition à l'essence de l'humanité. Ce qui est plat lui est accessible; c'est en vain qu'on ouvre devant lui les profondeurs de l'être humain.",
    "Il faut aussi remarquer que les représentations dont la valeur réside dans l'intéressant perdent à être répétées, car elles ne peuvent plus éveiller le désir d'une suite désormais connue. Des répétitions fréquentes les rendent fades et ennuyeuses pour le spectateur. En revanche, les œuvres dont la valeur réside dans le beau gagnent à être répétées, parce qu'on les comprend de mieux en mieux.",
    "À ces représentations dramatiques correspondent la plupart des récits, créatures de l'imagination de ces hommes qui, à Venise et à Naples, posent leur chapeau dans la rue et attendent qu'un auditoire se rassemble, puis commencent une histoire dont l'intérêt captive tant les auditeurs que, lorsque la catastrophe approche, le narrateur peut prendre son chapeau et recueillir son salaire auprès des participants cloués sur place sans craindre qu'ils ne s'éclipsent. En Allemagne, les mêmes hommes exercent leur métier moins directement, par l'intermédiaire des éditeurs, des foires de Leipzig et des cabinets de lecture; aussi ne se promènent-ils pas dans des habits aussi déchirés que leurs collègues d'Italie. Ils présentent au public les enfants de leur imagination sous les titres de romans, nouvelles, récits, poèmes romantiques, contes, etc.; installé derrière son poêle et en robe de chambre, celui-ci peut se préparer à jouir de l'intéressant avec plus de confort, mais aussi plus de patience. On sait combien de telles productions sont le plus souvent dépourvues de toute valeur esthétique; pourtant on ne peut refuser à beaucoup d'entre elles la propriété d'être intéressantes : autrement, comment rencontreraient-elles une telle participation?",
    "Nous voyons donc que l'intéressant ne produit pas nécessairement le beau : telle était la seconde question. Mais, inversement, le beau ne produit pas nécessairement l'intéressant. Des caractères significatifs peuvent être représentés, les profondeurs de la nature humaine peuvent s'ouvrir en eux, tout cela peut devenir visible dans des actions et des souffrances extraordinaires, de sorte que l'essence du monde et de l'homme nous fait face dans l'image avec les traits les plus forts et les plus clairs, sans que notre intérêt pour le cours des événements soit pour autant fortement excité par la progression continue de l'action, l'enchevêtrement et la résolution inattendue des circonstances. Les chefs-d'œuvre immortels de Shakespeare ont peu d'intéressant : l'action n'avance pas en ligne droite, elle hésite, comme dans tout Hamlet; elle s'étend latéralement, comme dans Le Marchand de Venise, tandis que la longueur est la dimension de l'intéressant; les scènes ne sont liées que lâchement, comme dans Henri IV. Les drames de Shakespeare n'agissent donc pas sensiblement sur le grand public.",
    "Les exigences d'Aristote, et tout particulièrement celle de l'unité d'action, visent l'intéressant, non le beau. D'une manière générale, elles sont formulées conformément au principe de raison; mais nous savons que l'Idée, et par conséquent le beau, n'existe que pour une connaissance qui s'est libérée de la domination de ce principe. Cela aussi sépare l'intéressant du beau : le premier appartient manifestement à la manière de considérer les choses qui suit le principe de raison, tandis que le beau reste toujours étranger au contenu de ce principe. La meilleure et la plus juste réfutation des unités d'Aristote est celle de Manzoni dans la préface de ses tragédies.",
    "Ce qui vaut des œuvres dramatiques de Shakespeare vaut également de celles de Goethe : même Egmont n'agit pas sur la foule parce qu'il n'y a presque aucun enchevêtrement ni développement; que dire alors de Tasso et d'Iphigénie! Il est manifeste que les tragiques grecs n'avaient pas l'intention d'agir sur les spectateurs par l'intéressant, puisqu'ils prenaient presque toujours pour matière de leurs chefs-d'œuvre des événements universellement connus et déjà souvent traités au théâtre. Nous voyons aussi par là combien le peuple grec était réceptif au beau : pour rehausser sa jouissance, il n'avait pas besoin de l'intérêt produit par des événements inattendus et une histoire nouvelle.",
    "Les chefs-d'œuvre narratifs possèdent eux aussi rarement la propriété de l'intéressant. Le vénérable Homère nous ouvre toute l'essence du monde et de l'homme, mais il ne cherche pas à exciter notre participation par l'enchevêtrement des événements ni à nous surprendre par des complications inattendues. Sa marche est lente; il demeure auprès de chaque scène et nous présente avec sérénité une image après l'autre, en la peignant soigneusement. En le lisant, aucune participation passionnée ne s'agite en nous; nous demeurons dans la connaissance pure. Il n'excite pas notre volonté, il la chante jusqu'au repos. Interrompre la lecture ne nous coûte aucun effort, car nous ne sommes pas en état de tension. Cela vaut plus encore de Dante, qui n'a pas à proprement parler donné une épopée, mais seulement un poème descriptif. Nous le voyons même dans les quatre romans immortels : Don Quichotte, Tristram Shandy, La Nouvelle Héloïse et Wilhelm Meister. Susciter notre intérêt n'y est nullement le but principal; à la fin de Tristram Shandy, le héros n'a même que huit ans.",
    "D'autre part, nous ne devons pas affirmer que l'intéressant ne se rencontre jamais dans les chefs-d'œuvre. Nous le trouvons déjà à un degré sensible dans les drames de Schiller, raison pour laquelle ils touchent aussi la foule; Œdipe roi de Sophocle le possède également. Parmi les chefs-d'œuvre narratifs, le Roland de l'Arioste le possède; et, comme exemple de l'intéressant au plus haut degré uni au beau, nous avons un excellent roman de Walter Scott, Tales of My Landlord, deuxième série. C'est l'œuvre poétique la plus intéressante que je connaisse; on peut y percevoir avec la plus grande clarté tous les effets de l'intéressant décrits plus haut en général. Mais ce roman est en même temps très beau : il nous montre les images les plus variées de la vie, dessinées avec une vérité frappante, et présente des caractères très divers avec beaucoup de justesse et de fidélité.",
    "L'intéressant est donc bien compatible avec le beau : telle était la troisième question. Toutefois, un faible degré d'intéressant mêlé au beau lui est probablement le plus utile, et le beau est et demeure la fin de l'art. Le beau s'oppose à l'intéressant sous un double rapport. Premièrement, le beau réside dans la connaissance de l'Idée, connaissance qui soustrait entièrement son objet aux formes exprimées par le principe de raison; l'intéressant, au contraire, réside principalement dans les événements, dont les enchaînements naissent précisément sous la conduite de ce principe. Deuxièmement, l'intéressant agit en excitant notre volonté, tandis que le beau n'existe que pour la connaissance pure et sans volonté. Pourtant, dans les œuvres dramatiques et narratives, un mélange d'intéressant est nécessaire — de même que les substances fugitives, purement gazeuses, ont besoin d'une base matérielle pour être conservées et communiquées. D'une part, il naît spontanément des événements qu'il faut inventer pour mettre les caractères en action; d'autre part, l'esprit se fatiguerait de passer, dans une connaissance entièrement détachée, de scène en scène et d'une image significative à une autre s'il n'y était conduit par un fil caché. Ce fil est précisément l'intéressant : c'est la participation que l'événement, comme tel, nous impose et qui, servant de lien à l'attention, rend l'esprit assez docile pour suivre le poète dans toutes les parties de sa représentation. Si l'intéressant suffit à remplir cette fonction, il a pleinement accompli son rôle. Il ne doit servir à relier les images par lesquelles le poète veut nous faire connaître l'Idée que comme le fil sur lequel les perles sont enfilées, qui les tient ensemble et en fait un collier. Mais l'intéressant devient nuisible au beau dès qu'il dépasse cette mesure : c'est le cas lorsqu'il nous entraîne à une participation si vive que nous nous impatientons devant toute description détaillée d'un objet par le poète narratif, ou devant toute longue réflexion que le dramaturge fait conduire à ses personnages, et que nous voudrions presser le poète pour suivre plus vite le développement des événements. Dans les œuvres épiques et dramatiques où le beau et l'intéressant sont également présents, l'intéressant peut être comparé au ressort d'une montre : il met l'ensemble en mouvement, mais, s'il agissait sans frein, il déroulerait tout le mécanisme en quelques minutes. Le beau, qui nous retient auprès de la contemplation et de la description détaillées de chaque objet, correspond au tambour de la montre qui ralentit le déploiement du ressort.",
    "L'intéressant est le corps du poème; le beau en est l'âme.",
    "Dans les poèmes épiques et dramatiques, l'intéressant, propriété nécessaire de l'action, est la matière; le beau est la forme, qui a besoin de cette matière pour devenir visible.",
]


KIERKEGAARD_FR = [
    (
        "L'ennui comme principe de mouvement",
        "Les gens d'expérience affirment qu'il est très raisonnable de partir d'un principe. Je les suis et pars de ce principe : tous les hommes sont ennuyeux. Se trouvera-t-il quelqu'un d'assez ennuyeux pour me contredire? Ce principe possède au plus haut degré la force de répulsion que l'on exige toujours du négatif, lequel est proprement le principe du mouvement. Il n'est pas seulement répulsif, mais infiniment dissuasif; celui qui a ce principe derrière lui doit nécessairement avancer à une vitesse infinie dans ses découvertes. Si ma proposition est vraie, il suffit, selon que l'on veut ralentir ou accélérer son élan, de considérer avec plus ou moins de mesure combien l'ennui est funeste à l'homme; et, si l'on veut porter la vitesse du mouvement à son maximum, presque au péril de la locomotive, il suffit de se dire : l'ennui est une racine de tout mal. Il est assez étrange que l'ennui, être lui-même si calme et si posé, puisse avoir une telle force de mise en mouvement. L'effet qu'il exerce est absolument magique, à ceci près qu'il n'attire pas : il repousse.",
    ),
    (
        "Le mot d'ordre : changer, mais selon un principe",
        "Si, comme on vient de le montrer, l'ennui est une racine de tout mal, quoi de plus naturel que de chercher à le vaincre? Mais ici comme partout, il faut surtout réfléchir calmement, afin de ne pas, possédé démoniaquement par l'ennui et voulant le fuir, travailler à s'y enfoncer. Tous ceux qui s'ennuient réclament du changement. Je suis parfaitement d'accord avec eux; seulement, il faut agir suivant un principe.",
    ),
    (
        "La fausse rotation : changer sans fin de terrain",
        "Mon écart par rapport à l'opinion commune est suffisamment exprimé par le mot : rotation des cultures. Ce mot pourrait sembler équivoque. Si je voulais lui faire désigner la méthode ordinaire, je devrais dire que la rotation consiste à changer continuellement de terrain. Pourtant, le cultivateur n'emploie pas le terme en ce sens. Je vais néanmoins l'utiliser ainsi un instant pour parler de la rotation qui repose sur l'infinité illimitée du changement, sur sa dimension extensive.",
    ),
    (
        "La vraie rotation : intensifier sous contrainte",
        "La méthode que je propose ne consiste pas à changer de terrain, mais, comme dans la véritable rotation des cultures, à changer la méthode de culture et les espèces semées. Ici apparaît immédiatement le principe de limitation, le seul qui sauve dans le monde. Plus on se limite, plus on devient inventif. Un prisonnier solitaire condamné à vie est extrêmement inventif; une araignée peut beaucoup l'amuser. Que l'on se rappelle l'école, à l'âge où aucun souci esthétique ne préside au choix de ceux qui doivent nous instruire et où, pour cette raison, ils sont souvent très ennuyeux : comme on devient inventif! Quel amusement que d'attraper une mouche, de la retenir sous une coquille de noix et de regarder comment elle se déplace avec celle-ci; quel plaisir que de creuser un trou dans la table, d'y enfermer une mouche et de l'observer à travers un morceau de papier! Combien le bruit monotone d'une gouttière peut devenir divertissant! Quel observateur scrupuleux on devient : pas le moindre bruit, pas le moindre mouvement ne nous échappe. Voilà la pointe extrême du principe qui cherche l'apaisement non par l'extension, mais par l'intensité.",
    ),
    (
        "Le même rapport revient autrement",
        "S'abstenir de l'amitié ne signifie pas qu'il faille vivre sans contact avec les hommes. Au contraire, ces rapports peuvent parfois prendre un tour plus profond; il faut seulement, même lorsque l'on partage quelque temps la vitesse de leur mouvement, conserver assez d'avance pour pouvoir les distancer. On croit qu'une telle conduite laisse des souvenirs désagréables et que le désagrément tient à ce qu'un rapport qui avait été quelque chose pour nous se réduit à rien. C'est une méprise. Le désagréable est un ingrédient piquant de l'âpreté de la vie. En outre, le même rapport peut retrouver un sens d'une autre manière. Ce qu'il faut éviter, c'est de jamais s'enliser; pour cela, il faut toujours garder l'oubli à portée de l'oreille. Le cultivateur expérimenté laisse parfois la terre en jachère; la prudence sociale recommande la même chose. Tout revient, mais autrement. Ce qui est une fois entré dans la rotation y demeure, mais varie selon la méthode de culture. On espère donc, de façon tout à fait conséquente, retrouver ses anciens amis et connaissances dans un monde meilleur; mais on ne partage pas la crainte de la foule qu'ils aient tellement changé qu'on ne puisse plus les reconnaître : on craint plutôt qu'ils soient restés absolument inchangés. Il est incroyable de voir ce que l'homme le plus insignifiant peut gagner grâce à une culture aussi raisonnable.",
    ),
    (
        "Se varier soi-même",
        "Selon cette prudence sociale, on varie donc dans une certaine mesure le terrain : si l'on voulait ne vivre qu'en rapport avec une seule personne, la rotation fonctionnerait mal, comme pour un cultivateur qui ne posséderait qu'une seule parcelle et ne pourrait jamais la laisser en jachère, opération pourtant extrêmement importante. De même, il faut aussi se varier continuellement soi-même; tel est à proprement parler le secret. Il faut pour cela avoir nécessairement la maîtrise de ses dispositions. Les avoir en son pouvoir au sens de pouvoir les produire à volonté est impossible; mais la prudence enseigne à profiter du moment. De même que le marin expérimenté scrute toujours l'eau et aperçoit une rafale longtemps à l'avance, il faut toujours voir venir un peu sa disposition. Avant de la revêtir, on doit savoir comment elle agit sur soi et probablement sur les autres. On touche d'abord l'instrument pour faire naître des sons purs et voir ce qu'un homme a en lui; les demi-teintes viennent ensuite. Plus on a de pratique, plus on se convainc facilement qu'il existe souvent dans un homme beaucoup de choses auxquelles on ne pense jamais. Lorsque les personnes sensibles, qui comme telles sont extrêmement ennuyeuses, se mettent en colère, elles deviennent souvent amusantes. La taquinerie est surtout un excellent instrument d'exploration.",
    ),
    (
        "L'arbitraire comme technique du regard",
        "Tout le secret réside dans l'arbitraire. On croit qu'il n'y a aucun art à être arbitraire; pourtant, il faut une étude profonde pour l'être de telle façon qu'on ne s'y égare pas soi-même et qu'on y trouve du plaisir. On ne jouit pas immédiatement, mais de tout autre chose que l'on introduit soi-même arbitrairement. On regarde le milieu d'une pièce de théâtre, on lit le troisième volume d'un livre. On obtient ainsi une jouissance toute différente de celle que l'auteur a eu la bonté de nous destiner. On jouit de quelque chose de tout à fait accidentel; on considère toute l'existence depuis ce point de vue et l'on fait échouer sa réalité sur lui. Je vais donner un exemple. Il y avait un homme dont une relation de la vie m'obligeait à écouter la conversation. À chaque occasion, il était prêt à prononcer un petit exposé philosophique extrêmement ennuyeux. Près de désespérer, je découvre soudain qu'il transpirait extraordinairement lorsqu'il parlait. Cette sueur attira alors mon attention. Je vis les perles se rassembler sur son front, se réunir en ruisseaux, glisser le long de son nez et finir en une masse en forme de goutte suspendue à l'extrémité de celui-ci. À partir de ce moment, tout fut changé; je pouvais même prendre plaisir à l'inciter à commencer son enseignement philosophique, uniquement pour observer la sueur sur son front et son nez. Baggesen dit quelque part d'un homme qu'il est certainement très honnête, mais qu'il a contre lui ce défaut : rien ne rime avec son nom. Il est extrêmement salutaire de laisser ainsi les réalités de la vie s'indifférencier dans un intérêt arbitraire. On fait de quelque chose d'accidentel l'absolu et, comme tel, l'objet d'une admiration absolue. Cela agit particulièrement bien lorsque les esprits sont en mouvement. À l'égard de beaucoup d'hommes, cette méthode est un excellent moyen d'excitation. On considère tout dans la vie comme un pari, et ainsi de suite. Plus on sait maintenir son arbitraire avec conséquence, plus les combinaisons deviennent amusantes. Le degré de conséquence montre toujours si l'on est artiste ou maladroit, car tous les hommes font jusqu'à un certain point la même chose. L'œil avec lequel on regarde la réalité doit continuellement changer. Les néoplatoniciens supposaient que les hommes qui avaient été moins parfaits dans ce monde devenaient après leur mort des animaux plus ou moins parfaits selon leurs mérites; ceux qui avaient, par exemple, pratiqué les vertus civiques à un degré moindre — les détaillants — devenaient des animaux civiques, comme les abeilles. Une telle conception de la vie, qui voit ici-bas tous les hommes transformés en animaux ou en plantes — Plotin pensait également que certains devenaient des plantes — offre une riche diversité de variations. Le peintre Tischbein a tenté d'idéaliser chaque homme en animal. Sa méthode a le défaut d'être trop sérieuse et de chercher une ressemblance véritable.",
    ),
]


CORE_DOSSIERS = [
    {
        "n": 1, "author": "Alessandro Nannini — Christian Garve et l'esthétique de l'intéressant",
        "status": "SYNTHÈSE + REPÉRAGE", "pages": "9–20, 36–41, 56–59, 71–80",
        "focus": "Reconstituer le passage d'inter-esse à une psychologie de la réception : l'objet fixe l'attention sans effort volontaire, par le plaisir qu'il promet et par les lacunes qu'il donne envie de combler.",
        "points": [
            "Distinguer l'intérêt comme fin déjà possédée par le sujet et l'effet intéressant exercé par l'objet.",
            "Suivre le rôle d'une connaissance antérieure incomplète : l'objet devient une énigme praticable.",
            "Séparer intéresser et émouvoir : maintenir une attente n'est pas seulement produire une émotion.",
            "Observer le tournant où l'intéressant relationnel devient stimulation fabriquée, puis surenchère et ennui.",
        ],
        "question": "Garve décrit-il déjà un déclencheur de construction mentale, ou seulement une économie de l'attention ?",
        "cards": "idea_0129, idea_0131, idea_0108",
    },
    {
        "n": 5, "author": "Anthony Eagan — Kierkegaard's Concept of the Interesting",
        "status": "GUIDE, OUVRAGE À OBTENIR", "pages": "1–32, 89–120, 161–178, 179–210",
        "focus": "Lire Eagan comme une architecture de Either/Or I : passage du beau à l'intéressant, variation réflexive, nouveauté, contrôle, puis herméneutique vorace.",
        "points": [
            "Le concept forme-t-il un gouffre historique entre beauté et modernité esthétique ?",
            "La variation produit-elle l'objet intéressant ou transforme-t-elle seulement la manière de l'appréhender ?",
            "La maîtrise esthétique évite-t-elle l'ennui au prix du solipsisme et du désespoir ?",
            "Toujours revenir aux voix pseudonymes de Kierkegaard : Eagan ne remplace pas le texte primaire.",
        ],
        "question": "Une construction qui ne sait pas finir devient-elle une herméneutique vorace ?",
        "cards": "idea_0117, idea_0122, idea_0124, idea_0131, idea_0132",
    },
    {
        "n": 6, "author": "Lothar Pikulik — Ästhetik des Interessanten",
        "status": "PROTOCOLE, OUVRAGE À OBTENIR", "pages": "Introduction, conclusion, index, bibliographie 223–228",
        "focus": "Tester si l'histoire de l'intéressant constitue une tradition réelle ou une reconstruction rétrospective restée extérieure au canon esthétique.",
        "points": [
            "Indexer Interesse, interessant, Schlegel, Schopenhauer, Langeweile, Subjektivismus, Reiz, Steigerung.",
            "Reconstituer la chronologie des textes primaires et noter les absences du corpus actuel.",
            "Distinguer passage du beau à l'intéressant et simple opposition polémique entre les deux.",
        ],
        "question": "La faible canonisation est-elle un fait historique ou un effet de notre reconstruction ?",
        "cards": "idea_0129, idea_0131",
    },
    {
        "n": 8, "author": "W. T. Stace — Interestingness",
        "status": "SYNTHÈSE, TEXTE PROTÉGÉ", "pages": "233–241, article entier",
        "focus": "Partir de Whitehead pour demander pourquoi la vérité ne suffit pas à la valeur d'une proposition et comment la nouveauté satisfait un palais intellectuel.",
        "points": [
            "Repérer la fonction exacte de l'analogie gustative.",
            "Vérifier si l'intéressant est une propriété, une réponse du sujet ou un rapport entre nouveauté et capacité.",
            "Déterminer si Stace défend, limite ou corrige la priorité fonctionnelle formulée par Whitehead.",
        ],
        "question": "Qu'ajoute l'intéressant au vrai, sans devenir un substitut du vrai ?",
        "cards": "idea_0129, idea_0132",
    },
    {
        "n": 9, "author": "Aurel Kolnai — On the Concept of the Interesting",
        "status": "SYNTHÈSE, ARTICLE À OBTENIR", "pages": "22–24, 27–32, 35–39",
        "focus": "Éprouver l'objectivité relative du jugement : A peut être plus intéressant que B alors que je suis personnellement davantage intéressé par B.",
        "points": [
            "Caractériser l'individuel, l'extraordinaire, le mystérieux et le multiple sur fond de familier.",
            "Comprendre l'expérience comme excursion vers une zone encore inexplorée.",
            "Examiner la familiarité inépuisée : l'ordinaire peut redevenir intéressant sans devenir spectaculaire.",
            "Distinguer intéressant, mystère et divertissement.",
        ],
        "question": "Peut-on justifier qu'un objet est intéressant sans réduire le jugement à ma préférence ?",
        "cards": "idea_0129, idea_0131, idea_0132",
    },
    {
        "n": 10, "author": "Mikhail Epstein — The Interesting",
        "status": "SYNTHÈSE, VERSION D'AUTEUR", "pages": "75–88",
        "focus": "Tester la formule centrale : une proposition intéressante combine improbabilité et possibilité de démonstration, donc surprise et intelligibilité.",
        "points": [
            "Distinguer intérêt intrinsèque et intérêt externe ou contextuel.",
            "Observer la dialectique du probable et de l'improbable dans le récit et d'autres domaines.",
            "Contrôler le risque d'intérêtisme : un intéressant prévisible finit par ennuyer.",
            "Pour la personne intéressante, examiner l'écart entre état actuel et possibilités de transformation.",
        ],
        "question": "L'improbable démontrable définit-il l'intéressant ou seulement une famille puissante d'énigmes ?",
        "cards": "idea_0129, idea_0130, idea_0132",
    },
    {
        "n": 11, "author": "Stephen Grimm — What Is Interesting?",
        "status": "SYNTHÈSE, ACCÈS OUVERT", "pages": "515–542",
        "focus": "Comprendre l'intéressant comme valeur épistémique des questions et principe d'allocation d'une attention limitée.",
        "points": [
            "Distinguer être intéressant, intéresser quelqu'un et éveiller sa curiosité.",
            "Tester les trois questions fondamentales : qu'y a-t-il, comment cela fonctionne-t-il, comment cela est-il devenu ainsi ?",
            "Examiner la réduction éventuelle à la question : comment dois-je vivre ?",
            "Repérer la dépendance aux capacités et situations des personnes.",
        ],
        "question": "L'énigme intéressante vaut-elle parce qu'elle promet une réponse ou parce que sa réponse orientera une vie ?",
        "cards": "idea_0116, idea_0129, idea_0132",
    },
    {
        "n": 12, "author": "Sianne Ngai — Merely Interesting",
        "status": "SYNTHÈSE, TEXTE PROTÉGÉ", "pages": "777–817",
        "focus": "Étudier un jugement esthétique faible qui suspend la décision, appelle des raisons et promet un retour futur plutôt qu'un verdict terminal.",
        "points": [
            "Chercher pourquoi aucune propriété non esthétique unique ne fonde le jugement.",
            "Suivre la temporalité de reprise : dire intéressant signifie souvent à revoir.",
            "Relier répétition, différence minimale, information et maintien de l'attention.",
            "Observer comment le jugement appelle un récit ou une justification.",
        ],
        "question": "La récursivité — l'intéressant est intéressant — vient-elle de cette obligation de reprise et de justification ?",
        "cards": "idea_0129, idea_0130, idea_0131, idea_0132",
    },
    {
        "n": 13, "author": "Sianne Ngai — Our Aesthetic Categories",
        "status": "GUIDE, OUVRAGE À OBTENIR", "pages": "1–23 et environ 110–173",
        "focus": "Lire la version développée de l'intéressant comme catégorie faible de la modernité : suspension, conceptualisation, art conceptuel, information et circulation.",
        "points": [
            "Situer l'intéressant avec le loufoque et le mignon dans le capitalisme contemporain.",
            "Décrire le passage du jugement initial à l'enquête ou à la narration prolongée.",
            "Repérer différence minimale, travail conceptuel et temporalité future.",
            "Distinguer mécanisme général et contexte socio-économique de la catégorie.",
        ],
        "question": "L'intéressant est-il faible par défaut ou puissant parce qu'il refuse de conclure trop tôt ?",
        "cards": "idea_0129, idea_0130, idea_0131, idea_0132",
    },
    {
        "n": 14, "author": "Alessandro Nannini — Interesting",
        "status": "SYNTHÈSE, ACCÈS OUVERT", "pages": "1–3, texte entier",
        "focus": "Utiliser cette entrée comme carte routière : étymologie, histoire condensée, grammaire du prédicat et psychologie de l'attention.",
        "points": [
            "Suivre le déplacement du juridique et financier vers l'esthétique.",
            "Noter Kant, Schlegel, Sibley, Cavell, James, Perry et Tomkins comme points de bifurcation.",
            "Examiner le prédicat esthétique générique sans base descriptive unique.",
            "Retenir la promesse de retour futur comme structure temporelle.",
        ],
        "question": "Pourquoi l'omniprésence grammaticale du prédicat n'a-t-elle pas produit un concept canonique ?",
        "cards": "idea_0129, idea_0130, idea_0131, idea_0132",
    },
    {
        "n": 15, "author": "Stephan Freivogel — L'intérêt et l'intéressant",
        "status": "SYNTHÈSE, ACCÈS OUVERT", "pages": "5–8, 23–31, 40–49, 63–68, 76–82",
        "focus": "Cartographier analytiquement l'intéressant entre psychologie, grammaire, objectivité et valeurs esthétique et épistémique.",
        "points": [
            "Distinguer concept, émotion, curiosité, attention, fascination et plaisir.",
            "Tester les couples nouveauté/complexité et intelligibilité/capacité de maîtrise.",
            "Extraire les valeurs pro tanto, prudentielle, cognitive et causale.",
            "Identifier les défauts : superficialité, diversion ou obstacle à d'autres valeurs.",
        ],
        "question": "Quelles propriétés non triviales restent propres à l'intéressant après toutes les distinctions ?",
        "cards": "idea_0116, idea_0123, idea_0131, idea_0132",
    },
    {
        "n": 16, "author": "Gerald J. Erion — Kolnai and the Interesting",
        "status": "GUIDE, CHAPITRE À OBTENIR", "pages": "62–69, chapitre entier",
        "focus": "Contrôler la reconstruction de Kolnai et la distinction entre valeur inhérente, valeur instrumentale et pouvoir causal de susciter l'intérêt.",
        "points": [
            "Examiner l'analogie avec le goût.",
            "Évaluer le recours à l'accord majoritaire.",
            "Distinguer une chose qui mérite l'intérêt d'une chose qui le cause effectivement.",
        ],
        "question": "Le pouvoir de déclencher suffit-il à constituer une valeur de l'objet ?",
        "cards": "idea_0132",
    },
    {
        "n": 17, "author": "R. S. D. Thomas — Beauty Is Not All There Is",
        "status": "SYNTHÈSE, TEXTE À OBTENIR", "pages": "116–127",
        "focus": "Prendre les mathématiques comme terrain : correction, originalité et intérêt sont nécessaires, mais l'intéressant n'est pas toujours la valeur suprême.",
        "points": [
            "Inventorier ce qui rend intéressants un résultat, une preuve ou une explication.",
            "Distinguer motivation de la recherche, orientation de l'enquête et valeur du résultat.",
            "Comparer curiosité, beauté et intérêt sans les hiérarchiser trop vite.",
        ],
        "question": "Une preuve peut-elle rester intéressante une fois son énigme résolue, par optimalité de sa forme ?",
        "cards": "idea_0028, idea_0116, idea_0132",
    },
    {
        "n": 18, "author": "Liang Xu — How Does the Interesting Become an Aesthetic Category?",
        "status": "SYNTHÈSE, ACCÈS OUVERT", "pages": "23–32, article entier",
        "focus": "Suivre la constitution de l'intéressant comme différence ou nouveauté de faible intensité, puis comme jugement demandant justification et participation.",
        "points": [
            "Relier retour des catégories esthétiques et fin de la domination de la théorie.",
            "Examiner la narrativisation et la suspension entre esthétique et non-esthétique.",
            "Contrôler la limite critique : l'ouverture du jugement s'inscrit-elle dans un cadre économique déjà fixé ?",
        ],
        "question": "La faiblesse initiale du signal est-elle précisément ce qui ouvre l'espace de construction ?",
        "cards": "idea_0131, idea_0132",
    },
]


NEIGHBORS = [
    ("Kant, Critique de la faculté de juger", "§§ 1–5, puis § 40", "Désintéressement du beau et communicabilité; ne pas confondre absence d'intérêt pratique et absence d'activité cognitive."),
    ("William James, Principles of Psychology I", "chap. XI, env. 402–403; curiosité env. 429", "L'intérêt sélectionne l'attention; la curiosité naît de la perception d'une lacune."),
    ("Ralph Barton Perry, General Theory of Value", "autour de 115", "Rapport entre objet de l'intérêt et valeur."),
    ("Silvan Tomkins, Affect, Imagery, Consciousness I", "autour de 347–348", "Affect d'intérêt, attention soutenue et retour."),
    ("Frank Sibley, Approach to Aesthetics", "34–35 et 47", "Rapport entre termes esthétiques et propriétés non esthétiques."),
    ("Stanley Cavell, Philosophy the Day After Tomorrow", "autour de 6", "Demander ce qui intéresse comme demande de raisons ou d'aveu critique."),
    ("Nelson Goodman, Languages of Art", "99–126", "Référence en avant, projetabilité et effets de l'expérience antérieure."),
    ("Adorno, Aesthetic Theory", "ouverture, env. 1–15", "Soupçon envers l'intérêt immédiat et autonomie de l'art."),
    ("Habermas, Knowledge and Human Interests", "introduction et appendice", "Intérêts constitutifs de connaissance, distincts du prédicat intéressant."),
]


def add_source_header(story, title, source, status="TEXTE ORIGINAL INCLUS"):
    story.extend([
        SectionMarker(title),
        heading(title, 1),
        badge(status, CORAL if ("ORIGINAL" in status or "TRADUCTION" in status) else BLUE),
        Spacer(1, 2 * mm),
        p(source, "small"),
    ])


def build_story():
    story = [SectionMarker("Mode d'emploi")]

    # Cover
    story.append(CoverPage(A5[1] - 31 * mm))
    story.append(PageBreak())

    story.extend([
        SectionMarker("Mode d'emploi"), heading("Mode d'emploi", 1),
        callout(
            "Ce que contient réellement ce lecteur",
            "Les passages allemands et danois du domaine public sont donnés en traduction française de travail. Whitehead est conservé en anglais. Pour les œuvres contemporaines encore protégées, le document donne une synthèse substantielle, les pages exactes, les problèmes à suivre et une feuille de notes, mais ne reproduit pas de longs passages. Les mentions texte à obtenir signalent les lacunes matérielles du corpus.",
            PALE_CORAL,
        ),
        Spacer(1, 4 * mm),
        p("Chaque unité doit produire six éléments : une définition, le porteur de la valeur, le mécanisme déclenché, la temporalité, le mode de disparition et une objection. La question transversale est de savoir si l'intéressant est une énigme praticable qui déclenche une construction et meurt — ou change de régime — lorsqu'elle est résolue."),
        heading("Légende", 2),
    ])
    legend = [
        [badge("TRADUCTION", CORAL), p("Traduction française de travail d'un texte du domaine public; contrôler l'original avant citation.", "small")],
        [badge("SYNTHÈSE", BLUE), p("Paraphrase de travail avec pagination; aucune phrase ne doit être citée comme si elle venait de l'auteur.", "small")],
        [badge("À OBTENIR", MUTED), p("Repérage fiable ou protocole de recherche, mais texte intégral non disponible dans le corpus.", "small")],
    ]
    lt = Table(legend, colWidths=[42 * mm, 70 * mm])
    lt.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.extend([lt, Spacer(1, 4 * mm), heading("Sommaire", 2)])
    toc = TableOfContents()
    toc.levelStyles = [S["toc0"], S["toc1"]]
    story.extend([toc, PageBreak()])

    story.extend([SectionMarker("Parcours en dix séances"), heading("Parcours en dix séances", 1)])
    sessions = [
        ("1", "Nannini + Garve", "Une histoire discontinue mais réelle ?"),
        ("2", "Garve", "L'objet stabilise-t-il l'attention sans contrainte ?"),
        ("3", "Schlegel", "Valeur, symptôme moderne ou étape à dépasser ?"),
        ("4", "Schopenhauer", "Pourquoi l'intrigue s'épuise-t-elle ?"),
        ("5", "Kierkegaard", "Changer d'objet ou changer la manière de cultiver ?"),
        ("6", "Whitehead + Stace", "Que vaut une proposition intéressante avant son jugement ?"),
        ("7", "Kolnai", "Quelles propriétés phénoménologiques sont propres à l'intéressant ?"),
        ("8", "Epstein + Grimm", "L'intéressant est-il une énigme promettant une résolution ?"),
        ("9", "Ngai", "Pourquoi le jugement appelle-t-il reprise et raisons ?"),
        ("10", "Freivogel + contrôles", "Que reste-t-il après comparaison avec les notions voisines ?"),
    ]
    rows = [[p("SÉANCE", "small"), p("LECTURE", "small"), p("QUESTION", "small")]]
    rows += [[p(a, "small"), p(b, "small"), p(c, "small")] for a, b, c in sessions]
    tt = Table(rows, colWidths=[18 * mm, 33 * mm, 61 * mm], repeatRows=1)
    tt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_BLUE]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.extend([tt, PageBreak()])

    # Garve dossier
    add_source_header(
        story,
        "1. Christian Garve — Einige Gedanken über das Interessirende",
        "Sammlung einiger Abhandlungen (Leipzig, 1779), p. 253–274 et 313–317. Transcription du Deutsches Textarchiv, CC BY-SA 4.0; traduction française de travail. Nannini (2018), p. 9–20 et 36–41, sert de guide historique, non de texte de substitution.",
        "TRADUCTION FRANÇAISE DE TRAVAIL",
    )
    garve = CORE_DOSSIERS[0]
    story.append(callout(
        "Orientation donnée par Nannini",
        "Lire Garve comme une théorie relationnelle de l'attention : l'objet ne contraint pas le sujet et le sujet ne s'impose pas arbitrairement un but. Une douce traction stabilise l'attention, ouvre une série et fait éprouver une lacune dont la résolution est désirée. Les passages ci-dessous sont le texte primaire de Garve, et non une synthèse de Nannini.",
    ))
    for title, paras in GARVE_FR:
        story.append(heading(title, 2))
        story.extend([p(para, "extract") for para in paras])
    story.extend([p("Question : " + garve["question"], "question"), heading("Notes", 2), notes(4), PageBreak()])

    # Schlegel
    add_source_header(
        story,
        "2. Friedrich Schlegel — l'intéressant moderne",
        "Über das Studium der griechischen Poesie, texte allemand TextGrid. Traduction française de travail des extraits correspondant aux problèmes signalés dans le programme.",
        "TRADUCTION FRANÇAISE DE TRAVAIL",
    )
    story.append(callout("Orientation", "Schlegel donne à l'intéressant un statut ambivalent : idéal de la poésie moderne, valeur esthétique provisoire, mécanisme sans maximum interne et crise appelée soit à se dépasser, soit à dégénérer en stimulation toujours plus forte."))
    for title, paras in SCHLEGEL_FR:
        story.append(heading(title, 2))
        for para in paras:
            story.append(p(para, "extract"))
        story.append(p("Question de marge : que devient ici l'intéressant lorsque la satisfaction est impossible par principe ?", "question"))
    story.extend([heading("Notes", 2), notes(5), PageBreak()])

    # Schopenhauer
    add_source_header(
        story,
        "3. Arthur Schopenhauer — Ueber das Interessante",
        "Handschriftlicher Nachlass, essai de 1821 avec ajout de 1840; transcription Projekt Gutenberg-DE; p. 381–389 dans le volume Piper de 1923. Traduction française de travail.",
        "TRADUCTION FRANÇAISE DE TRAVAIL",
    )
    story.append(callout("Orientation", "Lire l'essai comme une opération de déclassement : l'intéressant mobilise la volonté et retient l'attention dans les arts narratifs, mais il s'épuise à la répétition et reste subordonné au beau contemplatif."))
    for para in SCHOPENHAUER_FR:
        story.append(p(para, "extract"))
    story.extend([p("Question : la mort de l'intéressant après résolution est-elle ici démontrée par la perte de tension lors de la répétition ?", "question"), heading("Notes", 2), notes(5), PageBreak()])

    # Kierkegaard
    add_source_header(
        story,
        "4. Søren Kierkegaard — Vexel-Driften",
        "Enten–Eller I, édition critique danoise, p. 285–306; traduction française de travail d'une sélection. Dans la traduction Hong : The Rotation of Crops, p. 281–300.",
        "TRADUCTION FRANÇAISE DE TRAVAIL",
    )
    story.append(callout("Règle d'attribution", "Ces propositions appartiennent à la voix esthétique « A ». Elles ne doivent pas être attribuées directement à Kierkegaard. La technique de variation est intellectuellement féconde, mais le texte en montre aussi la dimension existentielle, arbitraire et potentiellement destructrice."))
    for title, para in KIERKEGAARD_FR:
        title_flowable = loose_heading(title) if title.startswith(("Le même", "L'arbitraire")) else heading(title, 2)
        story.extend([title_flowable, p(para, "extract")])
    story.extend([p("Question : la contrainte intensive conserve-t-elle l'intéressant ou fabrique-t-elle artificiellement une stimulation ?", "question"), heading("Notes", 2), notes(5), PageBreak()])

    # Whitehead
    add_source_header(
        story,
        "7. Alfred North Whitehead — propositions et sentiments",
        "Process and Reality (1929), partie III, chapitre VI, section II, p. 395–397 dans l'édition originale numérisée.",
        "TEXTE ANGLAIS ORIGINAL",
    )
    story.append(callout("Orientation", "La proposition n'est pas seulement le support d'un jugement vrai ou faux. Elle est une possibilité offerte au sentir, une amorce d'expérience. L'intérêt est donc fonctionnellement antérieur au jugement, sans abolir la vérité."))
    story.append(p(whitehead_extract(), "extract"))
    story.extend([p("Question : l'intéressant est-il ici le pouvoir d'une proposition de devenir une donnée pour une construction ultérieure ?", "question"), heading("Notes", 2), notes(5), PageBreak()])

    # Modern dossiers
    story.extend([SectionMarker("Dossiers de lecture contemporains"), heading("Dossiers de lecture contemporains", 1)])
    story.append(callout("Important", "Les pages suivantes sont des synthèses rédigées pour préparer la lecture. Elles ne contiennent pas d'extraits longs des œuvres protégées et ne doivent jamais être citées comme paroles des auteurs." , PALE_CORAL))
    for dossier in CORE_DOSSIERS[1:]:
        story.append(PageBreak())
        dossier_elements = [
            heading(f"{dossier['n']}. {dossier['author']}", 2),
            badge(dossier["status"], MUTED if "OBTENIR" in dossier["status"] else BLUE),
            Spacer(1, 1.5 * mm),
            p("Pages à lire : " + dossier["pages"], "small"),
            p(dossier["focus"]),
            heading("Points à suivre", 3),
            *bullets(dossier["points"], "small"),
            p("Question : " + dossier["question"], "question"),
            p("Cartes : " + dossier["cards"], "small"),
            Spacer(1, 3 * mm),
            notes(3),
        ]
        story.extend(dossier_elements)

    story.extend([PageBreak(), SectionMarker("Textes voisins"), heading("Textes voisins", 1)])
    story.append(p("Ces textes ne forment pas une tradition explicite de l'intéressant. Ils servent à séparer les fonctions prises en charge par des concepts concurrents : beauté, attention, curiosité, intérêt, projectibilité ou autonomie."))
    rows = [[p("TEXTE", "small"), p("PASSAGE", "small"), p("DISTINCTION", "small")]]
    rows += [[p(a, "small"), p(b, "small"), p(c, "small")] for a, b, c in NEIGHBORS]
    nt = Table(rows, colWidths=[38 * mm, 27 * mm, 47 * mm], repeatRows=1)
    nt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_BLUE]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.extend([nt, PageBreak()])

    story.extend([
        SectionMarker("Matrice transversale"), heading("Matrice transversale", 1),
        p("Remplir une ligne par auteur. La matrice doit permettre de décider si l'intéressant possède une structure commune ou seulement une famille de ressemblances."),
    ])
    matrix_rows = [[p(x, "small") for x in ["Auteur", "Porteur", "Déclencheur", "Construction", "Mort / reprise"]]]
    for _ in range(12):
        matrix_rows.append(["", "", "", "", ""])
    mt = Table(matrix_rows, colWidths=[23 * mm, 22 * mm, 22 * mm, 25 * mm, 20 * mm], rowHeights=[9 * mm] + [11 * mm] * 12, repeatRows=1)
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.extend([mt, PageBreak()])

    story.extend([
        SectionMarker("Fiche d'extraction"), heading("Fiche d'extraction reproductible", 1),
        p("Dupliquer mentalement cette page pour chaque lecture. Une source n'entre dans la thèse que lorsque le passage, la voix, la pagination et la conséquence conceptuelle ont été contrôlés."),
    ])
    labels = [
        "Référence et édition", "Passage et pages", "Voix ou contexte d'énonciation",
        "Objet dit intéressant", "Sujet pour lequel il l'est", "Propriété, relation ou opération",
        "Fonction : attention / cognition / narration / esthétique / existence",
        "Temporalité : saisie / attente / reprise / transformation", "Mode de disparition",
        "Rapport au vrai", "Concepts voisins ou substituts", "Citation courte à vérifier",
        "Cartes à modifier", "Question non résolue",
    ]
    form_rows = []
    for label in labels:
        form_rows.append([p(label, "small"), ""])
    form_heights = [9.3 * mm] * len(form_rows)
    form_heights[6] = 14 * mm
    form_heights[7] = 14 * mm
    ft = Table(form_rows, colWidths=[42 * mm, 70 * mm], rowHeights=form_heights)
    ft.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), PALE_BLUE),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.extend([ft, PageBreak()])

    story.extend([
        SectionMarker("Hypothèses à garder ouvertes"), heading("Hypothèses à garder ouvertes", 1),
        callout("Énigme", "L'intéressant pourrait être une énigme dotée de facteurs favorisant l'envie de résolution. Tant que la construction reste possible et non achevée, son pouvoir déclencheur persiste; une fois résolue, elle meurt ou se convertit en admiration de la forme trouvée."),
        callout("Dispositionnalité", "Une chose peut être intéressante sans intéresser actuellement : elle possède une disposition relationnelle à déclencher une construction chez un sujet adéquatement situé."),
        callout("Productivité représentationnelle", "L'objet intéressant engendre des représentations, hypothèses, récits, variations ou essais. Son intérêt se mesure moins au choc initial qu'à la qualité et à la durée de cette production."),
        callout("Résistance et épluchage", "Après le déclenchement, le sujet épluche l'objet jusqu'à épuisement. L'objet résiste plus ou moins; la contemplation, au contraire, suspend ou repousse la construction."),
        callout("Récursivité", "L'intéressant est lui-même intéressant : le concept déclenche l'enquête dont il est l'objet. Cette réflexivité explique en partie son caractère insaisissable et oblige à distinguer propriété, jugement et processus."),
        callout("Fin et création", "La vie de l'intéressant est liée au processus créatif et pose le problème de la fin. Une œuvre ou une solution peut cesser d'être déclenchante tout en devenant optale : elle paraît optimale, impossible à améliorer, comme une solution de mots croisés devenue évidente après coup."),
        Spacer(1, 4 * mm),
        heading("Note libre pour l'avion", 2), notes(10),
    ])
    return story


def main():
    required = [
        TMP / "schlegel.html", TMP / "schopenhauer.html",
        TMP / "kierkegaard.txt", TMP / "whitehead.txt",
    ]
    missing = [str(x) for x in required if not x.exists()]
    if missing:
        raise SystemExit("Missing source files: " + ", ".join(missing))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = ReaderDocTemplate(
        str(OUT), pagesize=A5,
        leftMargin=15 * mm, rightMargin=15 * mm,
        topMargin=17 * mm, bottomMargin=14 * mm,
        title="L'intéressant — lecteur de voyage",
        author="Programme de recherche sur l'intéressant",
        subject="Extraits du domaine public, synthèses et feuilles de lecture",
    )
    doc.multiBuild(build_story())
    print(OUT)


if __name__ == "__main__":
    main()
