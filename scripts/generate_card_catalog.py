from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path


KIND_LABELS = {
    "argument": "argument",
    "definition": "définition",
    "distinction": "distinction",
    "example": "exemple",
    "hypothesis": "hypothèse",
    "method": "méthode",
    "objection": "objection",
}

LEVEL_LABELS = {
    "articulation": "articulation",
    "conceptual": "conceptuelle",
    "scientific": "scientifique",
}

TITLE_ACCENTS = {
    "actionabilite": "actionabilité",
    "adaptee": "adaptée",
    "adjacent": "adjacent",
    "aimees": "aimées",
    "ajoutee": "ajoutée",
    "apparaît": "apparaît",
    "apparait": "apparaît",
    "apres": "après",
    "capacite": "capacité",
    "capacites": "capacités",
    "celine": "céline",
    "coherence": "cohérence",
    "coincidence": "coïncidence",
    "coincident": "coïncident",
    "comprehension": "compréhension",
    "controle": "contrôle",
    "createur": "créateur",
    "creativite": "créativité",
    "creation": "création",
    "cree": "crée",
    "creer": "créer",
    "declarée": "déclarée",
    "declaree": "déclarée",
    "decouverte": "découverte",
    "dedoubler": "dédoubler",
    "definition": "définition",
    "degé": "degré",
    "degre": "degré",
    "democratie": "démocratie",
    "democratique": "démocratique",
    "depend": "dépend",
    "desire": "désire",
    "deformer": "déformer",
    "deja": "déjà",
    "difficulte": "difficulté",
    "difficultuosite": "difficultuosité",
    "diversite": "diversité",
    "ecoute": "écoute",
    "eliminant": "éliminant",
    "emergence": "émergence",
    "ennuyeuse": "ennuyeuse",
    "epreuve": "épreuve",
    "eprouve": "éprouve",
    "epuiser": "épuiser",
    "est": "est",
    "ete": "été",
    "ethologie": "éthologie",
    "etudier": "étudier",
    "evaluer": "évaluer",
    "evenement": "événement",
    "evoluer": "évoluer",
    "frequent": "fréquent",
    "generation": "génération",
    "generale": "générale",
    "generateur": "générateur",
    "generative": "générative",
    "generes": "générés",
    "gout": "goût",
    "hesitation": "hésitation",
    "homogeneisation": "homogénéisation",
    "hypothese": "hypothèse",
    "idee": "idée",
    "idees": "idées",
    "impossibilite": "impossibilité",
    "imprevu": "imprévu",
    "incorporee": "incorporée",
    "ininteressante": "inintéressante",
    "interessant": "intéressant",
    "interessante": "intéressante",
    "interessantes": "intéressantes",
    "interet": "intérêt",
    "isole": "isolé",
    "levee": "levée",
    "liberte": "liberté",
    "litteraire": "littéraire",
    "maitre": "maître",
    "manieres": "manières",
    "matiere": "matière",
    "mecanismes": "mécanismes",
    "medias": "médias",
    "melodique": "mélodique",
    "memoire": "mémoire",
    "meme": "même",
    "memes": "mêmes",
    "methode": "méthode",
    "modele": "modèle",
    "necessaire": "nécessaire",
    "necessite": "nécessité",
    "non-repetition": "non-répétition",
    "nouveaute": "nouveauté",
    "observee": "observée",
    "oeuvre": "œuvre",
    "oeuvres": "œuvres",
    "operationnalise": "opérationnalise",
    "operationalise": "opérationnalisé",
    "organisee": "organisée",
    "paraître": "paraître",
    "paraitre": "paraître",
    "pedale": "pédale",
    "pensee": "pensée",
    "percue": "perçue",
    "peut-etre": "peut-être",
    "popularite": "popularité",
    "preference": "préférence",
    "preserve": "préserve",
    "pretend": "prétend",
    "pretendre": "prétendre",
    "privilegie": "privilégié",
    "probleme": "problème",
    "progres": "progrès",
    "proprietes": "propriétés",
    "rate": "raté",
    "recompense": "récompense",
    "reconnait": "reconnaît",
    "reel": "réel",
    "reflexive": "réflexive",
    "reifier": "réifier",
    "repete": "répète",
    "repetition": "répétition",
    "repetitions": "répétitions",
    "reputation": "réputation",
    "reside": "réside",
    "resolution": "résolution",
    "resultats": "résultats",
    "retrospectivement": "rétrospectivement",
    "reseaux": "réseaux",
    "reponse": "réponse",
    "semantiques": "sémantiques",
    "sequences": "séquences",
    "selection": "sélection",
    "seduit": "séduit",
    "seduisent": "séduisent",
    "singularite": "singularité",
    "structuree": "structurée",
    "systeme": "système",
    "temporalite": "temporalité",
    "theoremes": "théorèmes",
    "theories": "théories",
    "valide": "validée",
    "verite": "vérité",
    "virtuosite": "virtuosité",
    "apparaitre": "apparaître",
    "creatif": "créatif",
    "credibilite": "crédibilité",
    "curiosite": "curiosité",
    "decouvrir": "découvrir",
    "definir": "définir",
    "distribuee": "distribuée",
    "eprouver": "éprouver",
    "etat": "état",
    "etre": "être",
    "familiarite": "familiarité",
    "fluidite": "fluidité",
    "frontiere": "frontière",
    "general": "général",
    "genese": "genèse",
    "hypertrophie": "hypertrophié",
    "interroge": "interrogé",
    "mesures": "mesurés",
    "micro-emotion": "micro-émotion",
    "mobilite": "mobilité",
    "mystere": "mystère",
    "nait": "naît",
    "plutot": "plutôt",
    "realisation": "réalisation",
    "resistance": "résistance",
    "resider": "résider",
    "sequence": "séquence",
    "similarite": "similarité",
}


def load_spell_accents() -> dict[str, str]:
    lexicon_path = Path(__file__).with_name("french_diacritics.tsv")
    accents: dict[str, str] = {}
    for line in lexicon_path.read_text(encoding="utf-8").splitlines():
        source, target = line.split("\t", 1)
        if target == target.lower():
            accents[source] = target
    return accents


TEXT_ACCENTS = load_spell_accents()
TEXT_ACCENTS.update(
    {
        "actionabilite": "actionabilité",
        "autostabilite": "autostabilité",
        "apparait": "apparaît",
        "apparaitrait": "apparaîtrait",
        "apparaitre": "apparaître",
        "arriere-plan": "arrière-plan",
        "echantillonne": "échantillonne",
        "echoue": "échoue",
        "connait": "connaît",
        "connaitre": "connaître",
        "cout": "coût",
        "coute": "coûte",
        "coutes": "coûtes",
        "couterait": "coûterait",
        "couteuse": "coûteuse",
        "couteux": "coûteux",
        "creative": "créative",
        "bayesienne": "bayésienne",
        "decouvrables": "découvrables",
        "developper": "développer",
        "different": "différent",
        "disparait": "disparaît",
        "disparaitre": "disparaître",
        "elle-meme": "elle-même",
        "enchainement": "enchaînement",
        "enchainements": "enchaînements",
        "enchainer": "enchaîner",
        "entraine": "entraîne",
        "entrainer": "entraîner",
        "etait": "était",
        "evenement": "événement",
        "extreme": "extrême",
        "forcement": "forcément",
        "generes": "générés",
        "gout": "goût",
        "gouts": "goûts",
        "interessant": "intéressant",
        "interessante": "intéressante",
        "interessantes": "intéressantes",
        "interessants": "intéressants",
        "inferentiel": "inférentiel",
        "differer": "différer",
        "difficultuosite": "difficultuosité",
        "isole": "isolé",
        "lui-meme": "lui-même",
        "maitre": "maître",
        "maitrise": "maîtrise",
        "melodico-harmoniques": "mélodico-harmoniques",
        "methodologiquement": "méthodologiquement",
        "meme": "même",
        "memes": "mêmes",
        "modele": "modèle",
        "necessite": "nécessité",
        "necessites": "nécessités",
        "nait": "naît",
        "naitre": "naître",
        "oeuvre": "œuvre",
        "oeuvres": "œuvres",
        "operationalise": "opérationnalise",
        "paraitre": "paraître",
        "parait": "paraît",
        "pedale": "pédale",
        "predit": "prédit",
        "predicteur": "prédicteur",
        "pole": "pôle",
        "rate": "raté",
        "reapprentissage": "réapprentissage",
        "reconnaitre": "reconnaître",
        "reducible": "réductible",
        "reponderation": "repondération",
        "retrospective": "rétrospective",
        "repertories": "répertoriés",
        "reserve": "réserve",
        "selection": "sélection",
        "soi-meme": "soi-même",
        "tache": "tâche",
        "tractabilite": "tractabilité",
        "tres": "très",
        "verifies": "vérifiés",
        "video": "vidéo",
        "juxtaposes": "juxtaposés",
        "oublies": "oubliés",
        "jusqu-ou": "jusqu'où",
    }
)

MONTHS = (
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
)


@dataclass(frozen=True)
class Card:
    card_id: str
    title: str
    kind: str
    level: str
    sources: tuple[str, ...]
    source_notes: tuple[str, ...]
    references: tuple[str, ...]
    sections: dict[str, str]


def frontmatter_value(frontmatter: str, field: str) -> str:
    match = re.search(rf"^{re.escape(field)}:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    if match is None:
        raise ValueError(f"Missing frontmatter field: {field}")
    return match.group(1).strip().strip('"')


def frontmatter_list(frontmatter: str, field: str) -> tuple[str, ...]:
    match = re.search(
        rf"^{re.escape(field)}:\s*$\n(?P<items>(?:^  - .*$\n?)+)",
        frontmatter,
        re.MULTILINE,
    )
    if match is None:
        return ()
    return tuple(
        item.strip().strip('"')
        for item in re.findall(r"^  - (.+?)\s*$", match["items"], re.MULTILINE)
    )


def body_sections(body: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## (.+?)\s*$", body, re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[match.group(1)] = body[start:end].strip()
    return sections


def load_cards(card_dir: Path) -> dict[str, Card]:
    cards: dict[str, Card] = {}
    for path in sorted(card_dir.glob("idea_*.md")):
        parts = path.read_text(encoding="utf-8").split("---", 2)
        if len(parts) != 3:
            raise ValueError(f"Invalid card frontmatter: {path}")
        frontmatter, body = parts[1], parts[2]
        card = Card(
            card_id=frontmatter_value(frontmatter, "id"),
            title=frontmatter_value(frontmatter, "title"),
            kind=frontmatter_value(frontmatter, "kind"),
            level=frontmatter_value(frontmatter, "level"),
            sources=frontmatter_list(frontmatter, "sources"),
            source_notes=frontmatter_list(frontmatter, "source_notes"),
            references=frontmatter_list(frontmatter, "references"),
            sections=body_sections(body),
        )
        if card.card_id in cards:
            raise ValueError(f"Duplicate card id: {card.card_id}")
        if "Idée" not in card.sections or "Intérêt pour la thèse" not in card.sections:
            raise ValueError(f"Incomplete card: {path}")
        cards[card.card_id] = card
    return cards


def load_argument_order(index_path: Path) -> list[tuple[str, list[str]]]:
    families: list[tuple[str, list[str]]] = []
    current: list[str] | None = None
    for line in index_path.read_text(encoding="utf-8").splitlines():
        family = re.match(r"^## \d+\. (.+?) \(\d+\)$", line)
        if family:
            current = []
            families.append((family.group(1), current))
            continue
        card = re.match(r"^- `(idea_\d{4})` - ", line)
        if card and current is not None:
            current.append(card.group(1))
    return families


def latex_escape(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in text)


def latex_inline(text: str) -> str:
    tokens: dict[str, str] = {}

    def token(command: str, content: str) -> str:
        marker = f"@@TOKEN{len(tokens)}@@"
        tokens[marker] = rf"\{command}{{{latex_escape(content)}}}"
        return marker

    text = re.sub(r"`([^`]+)`", lambda match: token("texttt", match.group(1)), text)
    text = re.sub(r"\*([^*\n]+)\*", lambda match: token("emph", match.group(1)), text)
    escaped = latex_escape(text)
    for marker, replacement in tokens.items():
        escaped = escaped.replace(marker, replacement)
    return escaped


def restore_title_accents(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    for source, target in sorted(TITLE_ACCENTS.items(), key=lambda item: -len(item[0])):
        def replacement(match: re.Match[str]) -> str:
            if match.group(0)[0].isupper():
                return target[0].upper() + target[1:]
            return target

        text = re.sub(
            rf"(?<!\w){re.escape(source)}(?!\w)",
            replacement,
            text,
            flags=re.IGNORECASE,
        )

    contextual = {
        r"\ba l'": "à l'",
        r"\ba la\b": "à la",
        r"\ba un observateur\b": "à un observateur",
        r"\ba expliquer\b": "à expliquer",
        r"\ba falsifier\b": "à falsifier",
        r"\ba jour\b": "à jour",
        r"\ba penser\b": "à penser",
        r"\ba créer\b": "à créer",
        r"\ba paraître\b": "à paraître",
        r"\ba admirer\b": "à admirer",
        r"\bfin a un\b": "fin à un",
        r"\bpropre a\b": "propre à",
    }
    for pattern, replacement in contextual.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def restore_text_accents(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    for source, target in sorted(TEXT_ACCENTS.items(), key=lambda item: -len(item[0])):
        def replacement(match: re.Match[str]) -> str:
            if match.group(0)[0].isupper():
                return target[0].upper() + target[1:]
            return target

        text = re.sub(
            rf"(?<!\w){re.escape(source)}(?!\w)",
            replacement,
            text,
            flags=re.IGNORECASE,
        )

    contextual = {
        r"\bcette catégorie privilégié\b": "cette catégorie privilégie",
        r"\bne résumé pas\b": "ne résume pas",
        r"\bobjet préfère\b": "objet préféré",
        r"\best récompense\b": "est récompensé",
        r"\bdéjà compresse\b": "déjà compressé",
        r"\ba motive\b": "a motivé",
        r"\besprit ([^.!?]{0,80}) constitue\b": r"esprit \1 constitué",
        r"\bobservateur donne\b": "observateur donné",
        r"\bordre donne\b": "ordre donné",
        r"\bespace donne\b": "espace donné",
        r"\bniveau donne\b": "niveau donné",
        r"\bcontenu crée\b": "contenu créé",
        r"\bni entièrement génère\b": "ni entièrement généré",
        r"\bpeut être change\b": "peut être changé",
        r"\bdoit être confronte\b": "doit être confronté",
        r"\bpassage examine\b": "passage examiné",
        r"\bécart mesure\b": "écart mesuré",
        r"\bprivilège accorde\b": "privilège accordé",
        r"\bprivilège ([^,.]{0,30}) accorde\b": r"privilège \1 accordé",
        r"\best applique\b": "est appliqué",
        r"\bsont exposes\b": "sont exposés",
        r"\bapprentissage oriente\b": "apprentissage orienté",
        r"\bmodèle conditionne\b": "modèle conditionné",
        r"\bmodèle ([^,.]{0,25}) conditionne\b": r"modèle \1 conditionné",
        r"\bmécanisme implemente\b": "mécanisme implémenté",
        r"\bgeste maitrise\b": "geste maîtrisé",
        r"\bavoir absorbe\b": "avoir absorbé",
        r"\ba absorbe\b": "a absorbé",
        r"\bni génère au\b": "ni généré au",
        r"\bdéjà donne\b": "déjà donné",
        r"\bbien formes\b": "bien formés",
        r"\bdoit lui-même être qualifie\b": "doit lui-même être qualifié",
        r"\bdoit être traite\b": "doit être traité",
        r"\bcontextes conserves\b": "contextes conservés",
        r"\bont laisse\b": "ont laissé",
        r"\bobjet évalue\b": "objet évalué",
        r"\bprogramme ordonne\b": "programme ordonné",
        r"\bespace explore\b": "espace exploré",
        r"\brégime nomme\b": "régime nommé",
        r"\btraits proposes\b": "traits proposés",
        r"\bavait transforme\b": "avait transformé",
        r"\bcas contraste\b": "cas contrasté",
        r"\bcomportement situe\b": "comportement situé",
        r"\bêtre explore\b": "être exploré",
        r"\bêtre traite\b": "être traité",
        r"\bdéjà fonctionne\b": "déjà fonctionné",
        r"\baurait fonctionne\b": "aurait fonctionné",
        r"\ba déjà été montre\b": "a déjà été montré",
        r"\bpeut être consomme\b": "peut être consommé",
        r"\bpeut être pense\b": "peut être pensé",
        r"\bpoint trouve\b": "point trouvé",
        r"\bmots inventes\b": "mots inventés",
        r"\bêtre surexploite\b": "être surexploité",
        r"\best prépare\b": "est préparé",
        r"\bêtre mobilises\b": "être mobilisés",
        r"\bété formules\b": "été formulés",
        r"\bêtre reformules\b": "être reformulés",
        r"\bobjets préfères\b": "objets préférés",
        r"\bexemples orientes\b": "exemples orientés",
        r"\bgestes incorpores\b": "gestes incorporés",
        r"\battracteurs déjà incorpores\b": "attracteurs déjà incorporés",
        r"\bbien représente\b": "bien représenté",
        r"\bessais abandonnes\b": "essais abandonnés",
        r"\bcompromis répète\b": "compromis répété",
        r"\baccord d'ouverture trouve\b": "accord d'ouverture trouvé",
        r"\bintérêt fonde\b": "intérêt fondé",
        r"\bintérêt plus informe\b": "intérêt plus informé",
        r"\beffet destine\b": "effet destiné",
        r"\bdirectement lie\b": "directement lié",
        r"\bjeu propose\b": "jeu proposé",
        r"\bparamètre d'attachement propose\b": "paramètre d'attachement proposé",
        r"\bmorceau ignore\b": "morceau ignoré",
        r"\ba active\b": "a activé",
        r"\bnon optimise et expose\b": "non optimisé et exposé",
        r"\bsont pas seulement trompes\b": "ne sont pas seulement trompés",
        r"\ba lui\b": "à lui",
        r"\ba laquelle\b": "à laquelle",
        r"\ba elle-même\b": "à elle-même",
        r"\ba échelle\b": "à échelle",
        r"\ba quel\b": "à quel",
        r"\ba moins\b": "à moins",
        r"\ba trois\b": "à trois",
        r"\ba portée\b": "à portée",
        r"\ba faible\b": "à faible",
        r"\ba long terme\b": "à long terme",
        r"\bincarne (?:a|à) la distinction\b": "incarne la distinction",
        r"\ba une\b": "à une",
        r"\ba un\b": "à un",
        r"\ba des\b": "à des",
        r"\ba (?=[A-Za-zÀ-ÖØ-öø-ÿŒœ-]+(?:er|ir|re)\b)": "à ",
        r"\ba l'": "à l'",
        r"\ba la\b": "à la",
        r"\ba ce\b": "à ce",
        r"\ba cet\b": "à cet",
        r"\ba cette\b": "à cette",
        r"\ba ces\b": "à ces",
        r"\ba son\b": "à son",
        r"\ba sa\b": "à sa",
        r"\ba ses\b": "à ses",
        r"\ba leur\b": "à leur",
        r"\ba leurs\b": "à leurs",
        r"\ba partir\b": "à partir",
        r"\ba travers\b": "à travers",
        r"\ba chaque\b": "à chaque",
        r"\ba plusieurs\b": "à plusieurs",
        r"\ba nouveau\b": "à nouveau",
        r"\ba mesure\b": "à mesure",
        r"\ba condition\b": "à condition",
        r"\ba force\b": "à force",
        r"\ba propos\b": "à propos",
        r"\ba priori\b": "a priori",
        r"\ba posteriori\b": "a posteriori",
        r"\ba même\b": "à même",
        r"\ba quoi\b": "à quoi",
        r"\ba qui\b": "à qui",
        r"\ba expliquer\b": "à expliquer",
        r"\ba falsifier\b": "à falsifier",
        r"\ba jour\b": "à jour",
        r"\ba penser\b": "à penser",
        r"\ba créer\b": "à créer",
        r"\ba paraître\b": "à paraître",
        r"\ba admirer\b": "à admirer",
        r"\ba distinguer\b": "à distinguer",
        r"\ba décrire\b": "à décrire",
        r"\ba produire\b": "à produire",
        r"\ba comprendre\b": "à comprendre",
        r"\ba reconstruire\b": "à reconstruire",
        r"\ba rendre\b": "à rendre",
        r"\ba ouvrir\b": "à ouvrir",
        r"\ba relier\b": "à relier",
        r"\ba maintenir\b": "à maintenir",
        r"\ba transformer\b": "à transformer",
        r"\ba comparer\b": "à comparer",
        r"\ba observer\b": "à observer",
        r"\ba reconnaître\b": "à reconnaître",
        r"\ba entendre\b": "à entendre",
        r"\ba apprendre\b": "à apprendre",
        r"\ba devenir\b": "à devenir",
        r"\bpropre a\b": "propre à",
        r"\bfin a un\b": "fin à un",
        r"\bcas ou\b": "cas où",
        r"\bmoment ou\b": "moment où",
        r"\bsituation ou\b": "situation où",
        r"\brégime ou\b": "régime où",
        r"\bdécisions ou\b": "décisions où",
        r"\bpseudoptale, ou\b": "pseudoptale, où",
        r"\bsavoir ou\b": "savoir où",
        r"\bd'ou\b": "d'où",
        r"\bjusqu'ou\b": "jusqu'où",
        r"\blà ou\b": "là où",
        r"\bla ou\b": "là où",
        r"\bdes son\b": "dès son",
        r"\ba du\b": "a dû",
        r"\baurait du\b": "aurait dû",
        r"\bauraient du\b": "auraient dû",
        r"\bêtre sur que\b": "être sûr que",
        r"\bd'un cote\b": "d'un côté",
        r"\bde l'autre cote\b": "de l'autre côté",
    }
    for pattern, replacement in contextual.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def latex_paragraphs(markdown: str) -> str:
    paragraphs = re.split(r"\n\s*\n", markdown.strip())
    return "\n\n".join(
        latex_inline(" ".join(part.splitlines()))
        for part in paragraphs
    )


def source_label(source: str) -> str:
    path = Path(source)
    return path.stem.replace("_", " ") + path.suffix


def render_card(card: Card) -> str:
    kind = KIND_LABELS.get(card.kind, card.kind)
    level = LEVEL_LABELS.get(card.level, card.level)
    metadata = (
        rf"\texttt{{{latex_escape(card.card_id)}}}"
        rf"\quad\textbullet\quad {latex_escape(kind)}"
        rf"\quad\textbullet\quad {latex_escape(level)}"
    )
    parts = [
        r"\Needspace{8\baselineskip}",
        rf"\subsection{{{latex_inline(card.title)}}}",
        rf"{{\small\color{{metadata}} {metadata}\par}}",
        "",
        latex_paragraphs(card.sections["Idée"]),
    ]

    for heading in ("Exemple", "Exemples", "Statut de la source", "Contexte bibliographique"):
        if heading in card.sections:
            parts.extend(
                [
                    "",
                    rf"\paragraph{{{latex_escape(heading)}}}",
                    latex_paragraphs(card.sections[heading]),
                ]
            )

    parts.extend(
        [
            "",
            r"\begin{quote}",
            r"\textbf{Intérêt pour la thèse.} "
            + latex_paragraphs(card.sections["Intérêt pour la thèse"]),
            r"\end{quote}",
        ]
    )

    provenance = "; ".join(source_label(source) for source in card.sources)
    if card.source_notes:
        provenance += ". " + " ".join(card.source_notes)
    parts.extend(
        [
            rf"{{\footnotesize\color{{metadata}}\textbf{{Provenance :}} "
            + latex_inline(provenance)
            + r"\par}",
        ]
    )
    if card.references:
        parts.append(
            rf"{{\footnotesize\color{{metadata}}\textbf{{Références :}} "
            rf"\parencite{{{','.join(card.references)}}}\par}}"
        )
    return "\n".join(parts)


def render_document(
    families: list[tuple[str, list[str]]], cards: dict[str, Card], generated: date
) -> str:
    ordered_ids = [card_id for _, ids in families for card_id in ids]
    if len(ordered_ids) != len(set(ordered_ids)):
        raise ValueError("The argument index contains duplicate card ids")
    if set(ordered_ids) != set(cards):
        missing = sorted(set(cards) - set(ordered_ids))
        unknown = sorted(set(ordered_ids) - set(cards))
        raise ValueError(f"Index mismatch; missing={missing}, unknown={unknown}")

    family_blocks = []
    for family, ids in families:
        family_blocks.append(rf"\section{{{latex_inline(family)}}}")
        family_blocks.extend(render_card(cards[card_id]) for card_id in ids)

    reference_keys = sorted({key for card in cards.values() for key in card.references})
    date_label = f"{generated.day} {MONTHS[generated.month - 1]} {generated.year}"
    preamble = rf"""\documentclass[10pt,a4paper]{{article}}

\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage[french]{{babel}}
\usepackage{{lmodern}}
\usepackage{{microtype}}
\usepackage[a4paper,margin=2.2cm,headheight=20pt]{{geometry}}
\usepackage{{enumitem}}
\usepackage{{needspace}}
\usepackage{{xcolor}}
\usepackage{{fancyhdr}}
\usepackage[autostyle]{{csquotes}}
\usepackage[hidelinks]{{hyperref}}
\usepackage[backend=biber,style=authoryear,maxcitenames=2,maxbibnames=12]{{biblatex}}
\addbibresource{{bibliographie/references.bib}}
\hypersetup{{
  pdftitle={{L'émergence de l'intéressant - Catalogue provisoire des idées}},
  pdfauthor={{François Pachet}}
}}

\definecolor{{metadata}}{{HTML}}{{59636B}}
\definecolor{{rulecolor}}{{HTML}}{{C8CDD1}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{0.55em}}
\setlength{{\emergencystretch}}{{2em}}
\setcounter{{tocdepth}}{{1}}
\setlist[itemize]{{leftmargin=1.5em,itemsep=0.25em}}
\renewcommand{{\familydefault}}{{\sfdefault}}
\renewcommand{{\sectionmark}}[1]{{\markright{{#1}}}}
\pagestyle{{fancy}}
\fancyhf{{}}
\fancyhead[L]{{\small Catalogue provisoire des idées}}
\fancyhead[R]{{\small\color{{metadata}}\rightmark}}
\fancyfoot[C]{{\thepage}}
\renewcommand{{\headrulewidth}}{{0.3pt}}
\renewcommand{{\headrule}}{{\hbox to\headwidth{{\color{{rulecolor}}\leaders\hrule height \headrulewidth\hfill}}}}

\title{{L'émergence de l'intéressant\\\large Catalogue provisoire des idées}}
\author{{François Pachet}}
\date{{État de travail du {date_label}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
Ce document rassemble les {len(cards)} propositions actuellement extraites du corpus du projet de thèse. Il suit l'ordre des sept familles argumentatives de l'index de travail. Cette organisation est provisoire : elle sert à partager, comparer et discuter les propositions avant de fixer un plan de thèse. Les formulations et les attributions documentaires pourront encore être révisées.
\end{{abstract}}

\tableofcontents
\clearpage
"""
    bibliography = rf"""
\clearpage
\nocite{{{','.join(reference_keys)}}}
\printbibliography[title={{Bibliographie des cartes}}]

\end{{document}}
"""
    return preamble + "\n\n".join(family_blocks) + bibliography


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the provisional card catalogue")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("cartes/catalogue-idees.tex"),
        help="LaTeX output path, relative to the repository root",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    cards = load_cards(project_root / "cartes" / "inbox")
    families = load_argument_order(project_root / "cartes" / "indexes" / "by_argument.md")
    output = args.output if args.output.is_absolute() else project_root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_document(families, cards, date.today()), encoding="utf-8")
    print(f"Generated {output} from {len(cards)} cards in {len(families)} families.")


if __name__ == "__main__":
    main()
