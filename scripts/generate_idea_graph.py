from __future__ import annotations

import math
import re
import textwrap
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, PathPatch, Polygon
from matplotlib.path import Path as MplPath


FAMILY_COLORS = (
    "#2364AA",
    "#3A7D44",
    "#B44C43",
    "#7251A6",
    "#C77B20",
    "#267C78",
    "#8B5E3C",
)

RELATION_STYLES = {
    "supports": ("#238B57", "soutient"),
    "motivates": ("#238B57", "motive"),
    "specifies": ("#2869A6", "précise"),
    "bridges": ("#2869A6", "relie"),
    "operationalizes": ("#7251A6", "opérationnalise"),
    "illustrates": ("#C77B20", "illustre"),
    "limits": ("#B33A3A", "limite"),
    "objects_to": ("#B33A3A", "objecte"),
    "contrasts_with": ("#4F5963", "contraste"),
}


def load_cards(card_dir: Path) -> tuple[dict[str, str], dict[str, set[str]]]:
    titles: dict[str, str] = {}
    local_links: dict[str, set[str]] = defaultdict(set)
    for path in sorted(card_dir.glob("idea_*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        card_id = re.search(r"^id:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
        title = re.search(r'^title:\s*"(.+)"\s*$', frontmatter, re.MULTILINE)
        if card_id is None or title is None:
            raise ValueError(f"Invalid card metadata: {path}")
        source = card_id.group(1)
        titles[source] = title.group(1)

        links = re.search(r"^## Liens\s*$\n(?P<body>.*)$", text, re.MULTILINE | re.DOTALL)
        if links:
            for target in re.findall(r"idea_\d{4}", links["body"]):
                if target != source:
                    local_links[source].add(target)
    return titles, local_links


def load_families(index_path: Path) -> list[tuple[str, list[str]]]:
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


def load_typed_edges(path: Path) -> list[tuple[str, str, str]]:
    edges = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        source, relation, target, _ = line.split("\t", 3)
        edges.append((source, relation, target))
    return edges


def bezier_points(start: tuple[float, float], end: tuple[float, float], pull: float):
    p0 = start
    p1 = (start[0] * pull, start[1] * pull)
    p2 = (end[0] * pull, end[1] * pull)
    p3 = end
    return p0, p1, p2, p3


def bezier_point(points, t: float) -> tuple[float, float]:
    p0, p1, p2, p3 = points
    mt = 1 - t
    return (
        mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0],
        mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1],
    )


def bezier_tangent(points, t: float) -> tuple[float, float]:
    p0, p1, p2, p3 = points
    mt = 1 - t
    return (
        3 * mt**2 * (p1[0] - p0[0])
        + 6 * mt * t * (p2[0] - p1[0])
        + 3 * t**2 * (p3[0] - p2[0]),
        3 * mt**2 * (p1[1] - p0[1])
        + 6 * mt * t * (p2[1] - p1[1])
        + 3 * t**2 * (p3[1] - p2[1]),
    )


def draw_arrow(ax, points, color: str) -> None:
    center = bezier_point(points, 0.88)
    tangent = bezier_tangent(points, 0.88)
    length = math.hypot(*tangent)
    if not length:
        return
    ux, uy = tangent[0] / length, tangent[1] / length
    nx, ny = -uy, ux
    size = 0.012
    triangle = Polygon(
        [
            (center[0] + ux * size, center[1] + uy * size),
            (center[0] - ux * size + nx * size * 0.55, center[1] - uy * size + ny * size * 0.55),
            (center[0] - ux * size - nx * size * 0.55, center[1] - uy * size - ny * size * 0.55),
        ],
        closed=True,
        facecolor=color,
        edgecolor="none",
        alpha=0.82,
        zorder=3,
    )
    ax.add_patch(triangle)


def shorten(title: str, width: int = 42) -> str:
    if len(title) <= width:
        return title
    return textwrap.shorten(title, width=width, placeholder="…")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "output" / "graph"
    output_dir.mkdir(parents=True, exist_ok=True)

    titles, local_links = load_cards(project_root / "cartes" / "inbox")
    families = load_families(project_root / "cartes" / "indexes" / "by_argument.md")
    typed_edges = load_typed_edges(project_root / "cartes" / "relations.tsv")
    ordered_ids = [card_id for _, ids in families for card_id in ids]
    if set(ordered_ids) != set(titles) or len(ordered_ids) != len(titles):
        raise ValueError("The family index must contain every card exactly once")

    family_of = {
        card_id: family_index
        for family_index, (_, ids) in enumerate(families)
        for card_id in ids
    }

    gap = math.radians(2.2)
    usable = math.tau - len(families) * gap
    angles: dict[str, float] = {}
    family_ranges = []
    cursor = math.radians(95)
    for family_index, (family, ids) in enumerate(families):
        span = usable * len(ids) / len(ordered_ids)
        start = cursor
        step = span / len(ids)
        for offset, card_id in enumerate(ids):
            angles[card_id] = cursor - step * (offset + 0.5)
        cursor -= span
        end = cursor
        family_ranges.append((family, family_index, start, end))
        cursor -= gap

    positions = {
        card_id: (math.cos(angle), math.sin(angle)) for card_id, angle in angles.items()
    }
    typed_pairs = {(source, target) for source, _, target in typed_edges}
    typed_undirected = {frozenset((source, target)) for source, _, target in typed_edges}
    local_pairs = {
        frozenset((source, target))
        for source, targets in local_links.items()
        for target in targets
        if target in titles and frozenset((source, target)) not in typed_undirected
    }

    fig, ax = plt.subplots(figsize=(24, 24), facecolor="#FBFAF7")
    ax.set_facecolor("#FBFAF7")
    ax.set_aspect("equal")
    ax.axis("off")

    for pair in local_pairs:
        source, target = tuple(pair)
        points = bezier_points(positions[source], positions[target], 0.36)
        path = MplPath(points, [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4])
        ax.add_patch(
            PathPatch(path, facecolor="none", edgecolor="#7D858C", lw=0.42, alpha=0.12, zorder=1)
        )

    for source, relation, target in typed_edges:
        color = RELATION_STYLES[relation][0]
        pull = 0.22 if family_of[source] != family_of[target] else 0.48
        points = bezier_points(positions[source], positions[target], pull)
        path = MplPath(points, [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4])
        ax.add_patch(
            PathPatch(path, facecolor="none", edgecolor=color, lw=1.15, alpha=0.72, zorder=2)
        )
        draw_arrow(ax, points, color)

    for family, family_index, start, end in family_ranges:
        middle = (start + end) / 2
        start_deg = math.degrees(end)
        end_deg = math.degrees(start)
        color = FAMILY_COLORS[family_index]
        ax.add_patch(
            Arc((0, 0), 2.08, 2.08, theta1=start_deg, theta2=end_deg, lw=8, color=color, alpha=0.9, zorder=4)
        )
        label_pos = (1.47 * math.cos(middle), 1.47 * math.sin(middle))
        rotation = math.degrees(middle) - 90
        if math.cos(middle) < 0:
            rotation += 180
        ax.text(
            *label_pos,
            family,
            rotation=rotation,
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            color=color,
            zorder=6,
        )

    for card_id in ordered_ids:
        angle = angles[card_id]
        x, y = positions[card_id]
        color = FAMILY_COLORS[family_of[card_id]]
        ax.scatter([x], [y], s=34, facecolor=color, edgecolor="#FBFAF7", linewidth=0.8, zorder=5)

        radius = 1.09
        lx, ly = radius * math.cos(angle), radius * math.sin(angle)
        degrees = math.degrees(angle)
        on_left = math.cos(angle) < 0
        rotation = degrees + 180 if on_left else degrees
        label = f"{card_id[5:]}  {shorten(titles[card_id])}"
        ax.text(
            lx,
            ly,
            label,
            rotation=rotation,
            rotation_mode="anchor",
            ha="right" if on_left else "left",
            va="center",
            fontsize=5.7,
            color="#24282C",
            zorder=6,
        )

    ax.text(
        0,
        0.11,
        f"{len(titles)} idées",
        ha="center",
        va="center",
        fontsize=27,
        fontweight="bold",
        color="#24282C",
    )
    ax.text(
        0,
        0.025,
        f"{len(local_pairs)} liens associatifs\n{len(typed_edges)} relations fortes typées",
        ha="center",
        va="center",
        fontsize=12,
        color="#5A6269",
        linespacing=1.5,
    )
    ax.text(
        0,
        -0.105,
        "Les flèches colorées indiquent le sens des relations fortes.",
        ha="center",
        va="center",
        fontsize=9.5,
        color="#6A7177",
    )

    relation_groups = [
        ("#238B57", "soutient / motive"),
        ("#2869A6", "précise / relie"),
        ("#7251A6", "opérationnalise"),
        ("#C77B20", "illustre"),
        ("#B33A3A", "limite / objecte"),
        ("#4F5963", "contraste"),
        ("#7D858C", "lien associatif"),
    ]
    handles = [Line2D([0], [0], color=color, lw=2 if index < 6 else 0.7, alpha=0.8, label=label)
               for index, (color, label) in enumerate(relation_groups)]
    ax.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.035),
        ncol=4,
        frameon=False,
        fontsize=9.5,
        labelcolor="#3F464C",
    )

    ax.text(
        0,
        1.71,
        "L'émergence de l'intéressant — carte des propositions",
        ha="center",
        va="center",
        fontsize=23,
        fontweight="bold",
        color="#24282C",
    )
    ax.text(
        0,
        1.63,
        "Organisation argumentative provisoire — 12 juillet 2026",
        ha="center",
        va="center",
        fontsize=11,
        color="#667078",
    )
    ax.set_xlim(-1.72, 1.72)
    ax.set_ylim(-1.70, 1.78)
    fig.savefig(output_dir / "graphe-idees.svg", bbox_inches="tight", pad_inches=0.18)
    fig.savefig(output_dir / "graphe-idees.png", dpi=300, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    print(
        f"Generated graph with {len(titles)} nodes, {len(local_pairs)} local links "
        f"and {len(typed_edges)} typed relations."
    )


if __name__ == "__main__":
    main()
