from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ACTIVITY_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ACTIVITY_DIR.parents[1]
DEFAULT_CONFIG = ACTIVITY_DIR / "config.json"
DEFAULT_OUTPUT = ACTIVITY_DIR / "generated"
QUESTION_ID = "__question__"
CONCLUSION_ID = "__conclusion__"

STOPWORDS = {
    "afin", "ainsi", "alors", "apres", "assez", "aucun", "aussi", "autre",
    "aux", "avec", "avoir", "car", "cette", "ces", "comme", "dans", "des",
    "donc", "dont", "elle", "elles", "encore", "entre", "est", "etre", "fait",
    "font", "ici", "ils", "leur", "leurs", "mais", "meme", "moins", "non",
    "notamment", "nous", "objet", "par", "parce", "pas", "peut", "plus", "pour",
    "quand", "que", "quel", "quelle", "qui", "sans", "ses", "sont", "sous",
    "sur", "tandis", "toute", "toutes", "tout", "tous", "tres", "une", "vers",
}

PREFERRED_TARGET_TO_SOURCE = {
    "specifies",
    "operationalizes",
    "illustrates",
    "limits",
    "objects_to",
}

ROLE_LABELS = {
    "core": "CORE",
    "derived": "DERIVED",
    "test": "TEST",
    "case": "CASE",
    "objection": "OBJECTION",
    "speculative": "SPECULATIVE",
    "unclassified": "À CLASSER",
}


@dataclass(frozen=True)
class Card:
    card_id: str
    title: str
    kind: str
    level: str
    architecture: str
    tags: frozenset[str]
    body: str
    family: str
    path: Path

    @property
    def document(self) -> str:
        body = self.body.split("## Liens", 1)[0]
        return " ".join((self.title, self.title, " ".join(sorted(self.tags)), body))


@dataclass(frozen=True)
class Relation:
    source: str
    kind: str
    target: str
    note: str


@dataclass
class Model:
    cards: dict[str, Card]
    core_sections: list[tuple[str, list[str]]]
    relations: list[Relation]
    local_links: set[frozenset[str]]
    graph_distances: dict[tuple[str, str], float]
    vectors: dict[str, dict[str, float]]
    config: dict[str, object]
    endpoint_titles: dict[str, str]

    def components(self, source: str, target: str) -> dict[str, float]:
        lexical = cosine_distance(self.vectors[source], self.vectors[target])
        source_card = self.cards.get(source)
        target_card = self.cards.get(target)
        if source_card is None or target_card is None:
            return {"lexical": lexical, "tags": 1.0, "family": 1.0, "graph": 1.0}
        tags = jaccard_distance(source_card.tags, target_card.tags)
        family = 0.0 if source_card.family == target_card.family else 1.0
        graph = self.graph_distances[ordered_pair(source, target)]
        return {"lexical": lexical, "tags": tags, "family": family, "graph": graph}

    def distance(self, source: str, target: str) -> float:
        components = self.components(source, target)
        weights = self.config["distance_weights"]
        assert isinstance(weights, dict)
        return sum(float(weights[key]) * value for key, value in components.items())

    def transition_cost(
        self,
        source: str,
        target: str,
        primary_anchor: dict[str, str] | None = None,
    ) -> float:
        cost = self.distance(source, target)
        bonuses = self.config["transition_bonuses"]
        assert isinstance(bonuses, dict)
        typed = [
            relation
            for relation in self.relations
            if {relation.source, relation.target} == {source, target}
        ]
        if typed:
            cost -= float(bonuses["typed_relation"])
            if any(
                relation.kind in PREFERRED_TARGET_TO_SOURCE
                and relation.target == source
                and relation.source == target
                for relation in typed
            ):
                cost -= float(bonuses["preferred_direction"])
        elif frozenset((source, target)) in self.local_links:
            cost -= float(bonuses["local_link"])

        if primary_anchor:
            source_anchor = primary_anchor.get(source, source if source in core_ids(self) else "")
            target_anchor = primary_anchor.get(target, target if target in core_ids(self) else "")
            if source_anchor and source_anchor == target_anchor:
                cost -= float(bonuses["same_primary_anchor"])
        return max(cost, 0.001)


def parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return str(json.loads(value))
        except json.JSONDecodeError:
            return value[1:-1]
    return value.strip("'")


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


def load_families(path: Path) -> dict[str, str]:
    families: dict[str, str] = {}
    current = "Sans famille"
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^## \d+\. (.+?)(?: \(\d+\))?$", line)
        if heading:
            current = heading.group(1)
            continue
        card = re.match(r"^- `(idea_\d{4})` - ", line)
        if card:
            families[card.group(1)] = current
    return families


def load_cards(project_root: Path) -> tuple[dict[str, Card], set[frozenset[str]]]:
    families = load_families(project_root / "cartes" / "indexes" / "by_argument.md")
    cards: dict[str, Card] = {}
    local_links: set[frozenset[str]] = set()
    for path in sorted((project_root / "cartes" / "inbox").glob("idea_*.md")):
        text = path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text, path)
        card_id = str(metadata["id"])
        tags_value = metadata.get("tags", [])
        tags = frozenset(str(item) for item in tags_value) if isinstance(tags_value, list) else frozenset()
        cards[card_id] = Card(
            card_id=card_id,
            title=str(metadata["title"]),
            kind=str(metadata.get("kind", "")),
            level=str(metadata.get("level", "")),
            architecture=str(metadata.get("architecture", "unclassified")),
            tags=tags,
            body=body,
            family=families.get(card_id, "Sans famille"),
            path=path,
        )
        links = body.split("## Liens", 1)
        if len(links) == 2:
            for target in re.findall(r"idea_\d{4}", links[1]):
                if target != card_id:
                    local_links.add(frozenset((card_id, target)))
    return cards, local_links


def load_core_sections(path: Path) -> list[tuple[str, list[str]]]:
    text = path.read_text(encoding="utf-8")
    core_block = text.split("## Première passe", 1)[1].split("## Règle de la prochaine passe", 1)[0]
    sections: list[tuple[str, list[str]]] = []
    current: list[str] | None = None
    for line in core_block.splitlines():
        heading = re.match(r"^### (.+)$", line)
        if heading:
            current = []
            sections.append((heading.group(1), current))
            continue
        card = re.match(r"^- `(idea_\d{4})` - ", line)
        if card and current is not None:
            current.append(card.group(1))
    if not sections or any(not ids for _, ids in sections):
        raise ValueError("Aucune rubrique CORE exploitable dans l'index architectural")
    return sections


def load_relations(path: Path) -> list[Relation]:
    relations = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 4:
            raise ValueError(f"Relation invalide ligne {line_number}")
        relations.append(Relation(*fields))
    return relations


def ordered_pair(source: str, target: str) -> tuple[str, str]:
    return (source, target) if source < target else (target, source)


def build_graph_distances(
    card_ids: Iterable[str],
    relations: list[Relation],
    local_links: set[frozenset[str]],
    maximum_hops: int = 5,
) -> dict[tuple[str, str], float]:
    ids = sorted(card_ids)
    adjacency: dict[str, set[str]] = defaultdict(set)
    for relation in relations:
        adjacency[relation.source].add(relation.target)
        adjacency[relation.target].add(relation.source)
    for pair in local_links:
        if len(pair) == 2:
            source, target = tuple(pair)
            adjacency[source].add(target)
            adjacency[target].add(source)

    result: dict[tuple[str, str], float] = {}
    for source in ids:
        hops = {source: 0}
        frontier = [source]
        while frontier:
            current = frontier.pop(0)
            if hops[current] >= maximum_hops:
                continue
            for target in adjacency[current]:
                if target not in hops:
                    hops[target] = hops[current] + 1
                    frontier.append(target)
        for target in ids:
            if source >= target:
                continue
            hop_count = hops.get(target)
            if hop_count is None or hop_count >= maximum_hops:
                distance = 1.0
            else:
                distance = max(0.0, (hop_count - 1) / (maximum_hops - 1))
            result[(source, target)] = distance
    return result


def normalize_token(token: str) -> str:
    normalized = unicodedata.normalize("NFKD", token.casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def tokenize(text: str) -> list[str]:
    tokens = []
    for raw in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿŒœ]{3,}", text):
        token = normalize_token(raw)
        if token not in STOPWORDS:
            tokens.append(token)
    return tokens


def tfidf_vectors(documents: dict[str, str]) -> dict[str, dict[str, float]]:
    term_counts = {key: Counter(tokenize(text)) for key, text in documents.items()}
    document_frequency: Counter[str] = Counter()
    for counts in term_counts.values():
        document_frequency.update(counts.keys())
    total = len(documents)
    vectors: dict[str, dict[str, float]] = {}
    for key, counts in term_counts.items():
        vector = {
            term: (1.0 + math.log(count)) * (math.log((1.0 + total) / (1.0 + document_frequency[term])) + 1.0)
            for term, count in counts.items()
        }
        norm = math.sqrt(sum(value * value for value in vector.values())) or 1.0
        vectors[key] = {term: value / norm for term, value in vector.items()}
    return vectors


def cosine_distance(left: dict[str, float], right: dict[str, float]) -> float:
    if len(left) > len(right):
        left, right = right, left
    similarity = sum(value * right.get(term, 0.0) for term, value in left.items())
    return min(1.0, max(0.0, 1.0 - similarity))


def jaccard_distance(left: frozenset[str], right: frozenset[str]) -> float:
    if not left and not right:
        return 1.0
    return 1.0 - len(left & right) / len(left | right)


def build_model(project_root: Path, config_path: Path) -> Model:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    cards, local_links = load_cards(project_root)
    sections = load_core_sections(project_root / "cartes" / "indexes" / "by_architecture.md")
    indexed_core = {card_id for _, ids in sections for card_id in ids}
    metadata_core = {card_id for card_id, card in cards.items() if card.architecture == "core"}
    if indexed_core != metadata_core:
        raise ValueError("Les CORE de l'index architectural et des cartes divergent")
    endpoint_titles = {
        QUESTION_ID: str(config["question"]["title"]),
        CONCLUSION_ID: str(config["conclusion"]["title"]),
    }
    documents = {card_id: card.document for card_id, card in cards.items()}
    documents[QUESTION_ID] = " ".join(str(value) for value in config["question"].values())
    documents[CONCLUSION_ID] = " ".join(str(value) for value in config["conclusion"].values())
    relations = load_relations(project_root / "cartes" / "relations.tsv")
    return Model(
        cards=cards,
        core_sections=sections,
        relations=relations,
        local_links=local_links,
        graph_distances=build_graph_distances(cards, relations, local_links),
        vectors=tfidf_vectors(documents),
        config=config,
        endpoint_titles=endpoint_titles,
    )


def core_ids(model: Model) -> set[str]:
    return {card_id for _, ids in model.core_sections for card_id in ids}


def exact_core_route(model: Model) -> tuple[list[str], float]:
    ordered_core = [card_id for _, ids in model.core_sections for card_id in ids]
    limit = int(model.config["exact_core_limit"])
    if len(ordered_core) > limit:
        raise ValueError(f"{len(ordered_core)} CORE dépassent la limite exacte configurée ({limit})")
    section_of = {
        card_id: section_index
        for section_index, (_, ids) in enumerate(model.core_sections)
        for card_id in ids
    }
    full_mask = (1 << len(ordered_core)) - 1
    dp: dict[tuple[int, int], tuple[float, tuple[int, ...]]] = {}
    for index, card_id in enumerate(ordered_core):
        if section_of[card_id] == 0:
            dp[(1 << index, index)] = (
                model.transition_cost(QUESTION_ID, card_id),
                (index,),
            )
    for mask_size in range(1, len(ordered_core)):
        states = [(state, value) for state, value in dp.items() if state[0].bit_count() == mask_size]
        for (mask, last), (cost, path) in states:
            remaining = [index for index in range(len(ordered_core)) if not mask & (1 << index)]
            if not remaining:
                continue
            next_section = min(section_of[ordered_core[index]] for index in remaining)
            for index in remaining:
                card_id = ordered_core[index]
                if section_of[card_id] != next_section:
                    continue
                next_mask = mask | (1 << index)
                next_cost = cost + model.transition_cost(ordered_core[last], card_id)
                key = (next_mask, index)
                if key not in dp or next_cost < dp[key][0]:
                    dp[key] = (next_cost, path + (index,))
    candidates = []
    for (mask, last), (cost, path) in dp.items():
        if mask == full_mask:
            candidates.append((cost + model.transition_cost(ordered_core[last], CONCLUSION_ID), path))
    if not candidates:
        raise ValueError("Aucun parcours CORE compatible avec les chapitres")
    total, best = min(candidates, key=lambda item: item[0])
    return [ordered_core[index] for index in best], total


def relation_to_core_bonus(model: Model, card_id: str, candidate: str) -> float:
    bonuses = model.config["transition_bonuses"]
    assert isinstance(bonuses, dict)
    if any({relation.source, relation.target} == {card_id, candidate} for relation in model.relations):
        return float(bonuses["typed_relation"])
    if frozenset((card_id, candidate)) in model.local_links:
        return float(bonuses["local_link"])
    return 0.0


def assign_to_core(model: Model, route: list[str]) -> tuple[dict[str, str], dict[str, list[tuple[str, float]]]]:
    primary: dict[str, str] = {}
    alternatives: dict[str, list[tuple[str, float]]] = {}
    count = int(model.config["secondary_anchor_count"])
    core = set(route)
    for card_id in sorted(set(model.cards) - core):
        ranked = sorted(
            (
                (candidate, max(0.0, model.distance(card_id, candidate) - relation_to_core_bonus(model, card_id, candidate)))
                for candidate in route
            ),
            key=lambda item: (item[1], route.index(item[0])),
        )
        primary[card_id] = ranked[0][0]
        alternatives[card_id] = ranked[: max(1, count)]
    return primary, alternatives


def local_chapter_route(
    model: Model,
    chapter_core: list[str],
    satellites: Iterable[str],
    primary: dict[str, str],
    left_boundary: str,
    right_boundary: str,
) -> list[str]:
    route = list(chapter_core)
    remaining = set(satellites)
    while remaining:
        best: tuple[float, str, int] | None = None
        extended = [left_boundary, *route, right_boundary]
        for card_id in sorted(remaining):
            for position, (left, right) in enumerate(itertools.pairwise(extended)):
                delta = (
                    model.transition_cost(left, card_id, primary)
                    + model.transition_cost(card_id, right, primary)
                    - model.transition_cost(left, right, primary)
                )
                candidate = (delta, card_id, position)
                if best is None or candidate < best:
                    best = candidate
        assert best is not None
        _, card_id, position = best
        route.insert(position, card_id)
        remaining.remove(card_id)
    return route


def grouped_core_route(model: Model, route: list[str]) -> list[tuple[str, list[str]]]:
    result = []
    route_index = {card_id: index for index, card_id in enumerate(route)}
    for title, ids in model.core_sections:
        result.append((title, sorted(ids, key=route_index.__getitem__)))
    return result


def card_title(model: Model, card_id: str) -> str:
    if card_id in model.cards:
        return model.cards[card_id].title
    return model.endpoint_titles[card_id]


def route_cost(model: Model, route: list[str], primary: dict[str, str] | None = None) -> float:
    return sum(model.transition_cost(left, right, primary) for left, right in itertools.pairwise(route))


def build_result(model: Model) -> dict[str, object]:
    route, total = exact_core_route(model)
    primary, alternatives = assign_to_core(model, route)
    sections = grouped_core_route(model, route)
    chapter_results = []
    for index, (title, chapter_core) in enumerate(sections):
        core_set = set(chapter_core)
        satellites = [card_id for card_id, anchor in primary.items() if anchor in core_set]
        left_boundary = QUESTION_ID if index == 0 else sections[index - 1][1][-1]
        right_boundary = CONCLUSION_ID if index == len(sections) - 1 else sections[index + 1][1][0]
        local_route = local_chapter_route(
            model,
            chapter_core,
            satellites,
            primary,
            left_boundary,
            right_boundary,
        )
        chapter_results.append(
            {
                "title": title,
                "core_route": chapter_core,
                "local_route": local_route,
                "local_cost": route_cost(model, [left_boundary, *local_route, right_boundary], primary),
                "role_counts": dict(sorted(Counter(model.cards[card_id].architecture for card_id in local_route).items())),
            }
        )
    transitions = []
    full_core_route = [QUESTION_ID, *route, CONCLUSION_ID]
    for source, target in itertools.pairwise(full_core_route):
        transitions.append(
            {
                "source": source,
                "target": target,
                "cost": model.transition_cost(source, target),
                "components": model.components(source, target),
            }
        )
    anchor_loads = Counter(primary.values())
    ambiguous = []
    distant = []
    for card_id, ranked in alternatives.items():
        margin = ranked[1][1] - ranked[0][1] if len(ranked) > 1 else 1.0
        if margin <= 0.05:
            ambiguous.append(
                {
                    "card": card_id,
                    "margin": margin,
                    "first": ranked[0][0],
                    "second": ranked[1][0],
                }
            )
        if ranked[0][1] >= 0.8:
            distant.append({"card": card_id, "core": ranked[0][0], "cost": ranked[0][1]})
    return {
        "summary": {
            "card_count": len(model.cards),
            "core_count": len(route),
            "chapter_count": len(sections),
            "architecture_counts": dict(sorted(Counter(card.architecture for card in model.cards.values()).items())),
            "core_route_cost": total,
        },
        "endpoints": {
            "question": model.config["question"],
            "conclusion": model.config["conclusion"],
        },
        "core_route": route,
        "core_transitions": transitions,
        "primary_anchor": primary,
        "anchor_alternatives": {
            card_id: [{"core": core, "cost": cost} for core, cost in ranked]
            for card_id, ranked in alternatives.items()
        },
        "chapters": chapter_results,
        "diagnostics": {
            "anchor_loads": dict(sorted(anchor_loads.items())),
            "ambiguous_assignments": sorted(ambiguous, key=lambda item: (item["margin"], item["card"])),
            "distant_assignments": sorted(distant, key=lambda item: (-item["cost"], item["card"])),
        },
    }


def write_distances(model: Model, path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("source", "target", "lexical", "tags", "family", "graph", "combined", "typed_relation", "local_link"))
        for source, target in itertools.combinations(sorted(model.cards), 2):
            components = model.components(source, target)
            writer.writerow(
                (
                    source,
                    target,
                    f"{components['lexical']:.6f}",
                    f"{components['tags']:.6f}",
                    f"{components['family']:.6f}",
                    f"{components['graph']:.6f}",
                    f"{model.distance(source, target):.6f}",
                    int(any({relation.source, relation.target} == {source, target} for relation in model.relations)),
                    int(frozenset((source, target)) in model.local_links),
                )
            )


def render_report(model: Model, result: dict[str, object]) -> str:
    summary = result["summary"]
    assert isinstance(summary, dict)
    lines = [
        "# Parcours hiérarchique expérimental des cartes",
        "",
        "> Résultat dérivé : ce rapport ne modifie ni le statut ni l'ordre canonique des cartes.",
        "> Les proximités TF-IDF et de graphe constituent une ligne de base, non un jugement philosophique.",
        "",
        "## Vue d'ensemble",
        "",
        f"- {summary['card_count']} cartes, dont {summary['core_count']} `CORE` ;",
        f"- {summary['chapter_count']} chapitres repris de l'index architectural ;",
        f"- coût du parcours `CORE` : {summary['core_route_cost']:.4f} ;",
    ]
    architecture_counts = summary["architecture_counts"]
    assert isinstance(architecture_counts, dict)
    for role, count in architecture_counts.items():
        lines.append(f"- {count} cartes {ROLE_LABELS.get(role, role.upper())}.")

    lines.extend(["", "## Colonne vertébrale `CORE`", ""])
    question = model.config["question"]
    conclusion = model.config["conclusion"]
    assert isinstance(question, dict) and isinstance(conclusion, dict)
    lines.append(f"**Départ — {question['title']}.** {question['text']}")
    chapters = result["chapters"]
    assert isinstance(chapters, list)
    for chapter_index, chapter in enumerate(chapters, start=1):
        assert isinstance(chapter, dict)
        lines.extend(["", f"### Chapitre {chapter_index} — {chapter['title']}", ""])
        for card_id in chapter["core_route"]:
            lines.append(f"- `{card_id}` — {model.cards[card_id].title}")
    lines.extend(["", f"**Arrivée — {conclusion['title']}.** {conclusion['text']}"])

    lines.extend(["", "## Transitions `CORE` les plus coûteuses", ""])
    transitions = result["core_transitions"]
    assert isinstance(transitions, list)
    for transition in sorted(transitions, key=lambda item: item["cost"], reverse=True)[:8]:
        lines.append(
            f"- `{transition['source']}` → `{transition['target']}` "
            f"({transition['cost']:.4f}) — {card_title(model, transition['source'])} → "
            f"{card_title(model, transition['target'])}"
        )

    diagnostics = result["diagnostics"]
    assert isinstance(diagnostics, dict)
    anchor_loads = diagnostics["anchor_loads"]
    ambiguous = diagnostics["ambiguous_assignments"]
    distant = diagnostics["distant_assignments"]
    assert isinstance(anchor_loads, dict) and isinstance(ambiguous, list) and isinstance(distant, list)
    lines.extend(["", "## Diagnostic architectural", ""])
    chapter_sizes = [len(chapter["local_route"]) for chapter in chapters]
    lines.append("Tailles des chapitres proposés : " + ", ".join(str(size) for size in chapter_sizes) + ".")
    lines.append("")
    lines.append("Charges des ancrages `CORE` (cartes satellites) :")
    lines.append("")
    for card_id, count in sorted(anchor_loads.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{card_id}` : {count} — {model.cards[card_id].title}")
    lines.extend(
        [
            "",
            f"Rattachements ambigus (écart ≤ 0,05 entre les deux premiers `CORE`) : {len(ambiguous)}.",
            "",
        ]
    )
    for item in ambiguous[:15]:
        lines.append(
            f"- `{item['card']}` : `{item['first']}` / `{item['second']}` "
            f"(écart {item['margin']:.3f}) — {model.cards[item['card']].title}"
        )
    if len(ambiguous) > 15:
        lines.append(f"- … {len(ambiguous) - 15} autres dans `parcours.json`.")
    lines.extend(["", f"Rattachements éloignés (coût ≥ 0,8) : {len(distant)}.", ""])
    for item in distant[:15]:
        lines.append(
            f"- `{item['card']}` → `{item['core']}` ({item['cost']:.3f}) — "
            f"{model.cards[item['card']].title}"
        )
    if len(distant) > 15:
        lines.append(f"- … {len(distant) - 15} autres dans `parcours.json`.")

    lines.extend(["", "## Composition proposée des chapitres", ""])
    primary = result["primary_anchor"]
    alternatives = result["anchor_alternatives"]
    assert isinstance(primary, dict) and isinstance(alternatives, dict)
    for chapter_index, chapter in enumerate(chapters, start=1):
        assert isinstance(chapter, dict)
        lines.extend([f"### Chapitre {chapter_index} — {chapter['title']}", ""])
        role_counts = chapter["role_counts"]
        assert isinstance(role_counts, dict)
        counts = ", ".join(f"{ROLE_LABELS.get(role, role)} : {count}" for role, count in role_counts.items())
        lines.append(f"Composition : {counts}. Coût local indicatif : {chapter['local_cost']:.4f}.")
        lines.extend(["", "Ordre local suggéré (les `CORE` sont en gras) :", ""])
        for position, card_id in enumerate(chapter["local_route"], start=1):
            card = model.cards[card_id]
            role = ROLE_LABELS.get(card.architecture, card.architecture.upper())
            marker = "**CORE**" if card.architecture == "core" else role
            anchor_note = ""
            if card.architecture != "core":
                ranked = alternatives[card_id]
                first = ranked[0]
                anchor_note = f" — ancrage `{primary[card_id]}` ({first['cost']:.3f})"
            lines.append(f"{position}. `{card_id}` — {card.title} [{marker}]{anchor_note}")
        lines.append("")

    unclassified = sorted(
        (card for card in model.cards.values() if card.architecture == "unclassified"),
        key=lambda card: (primary.get(card.card_id, ""), card.card_id),
    )
    lines.extend(["## Cartes restant à classer", ""])
    lines.append(
        f"Le calcul place provisoirement {len(unclassified)} cartes sans leur attribuer de statut. "
        "Leur ancrage proposé peut servir à la prochaine passe éditoriale."
    )
    lines.append("")
    for card in unclassified:
        lines.append(f"- `{card.card_id}` → `{primary[card.card_id]}` — {card.title}")

    lines.extend(
        [
            "",
            "## Lecture des résultats",
            "",
            "Les séquences et rattachements sont des hypothèses à comparer au jugement éditorial. "
            "Une transition coûteuse peut signaler une articulation manquante ; un `CORE` attirant "
            "beaucoup de cartes peut être trop large ; une carte dont les trois meilleurs ancrages "
            "ont des coûts voisins est structurellement instable.",
            "",
        ]
    )
    return "\n".join(lines)


def generate(project_root: Path, config_path: Path, output_dir: Path) -> dict[str, object]:
    model = build_model(project_root, config_path)
    result = build_result(model)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "parcours.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "parcours.md").write_text(render_report(model, result), encoding="utf-8")
    write_distances(model, output_dir / "distances.tsv")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Calcule un parcours hiérarchique dérivé du catalogue de cartes")
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = generate(args.project_root.resolve(), args.config.resolve(), args.output.resolve())
    summary = result["summary"]
    print(
        f"Parcours généré : {summary['card_count']} cartes, "
        f"{summary['core_count']} CORE, {summary['chapter_count']} chapitres."
    )
    print(args.output.resolve() / "parcours.md")


if __name__ == "__main__":
    main()
