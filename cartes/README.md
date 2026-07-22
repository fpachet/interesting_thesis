# Cartes d'idées

Ce dossier sert de boite de réception pour les idées extraites du corpus.

Le principe est volontairement simple :

- une carte = une proposition substantielle et manipulable ;
- les cartes commencent dans `inbox/` avec le statut `inbox` ;
- le registre indique quels documents ont été lus, partiellement lus, ou seulement inventoriés ;
- l'organisation reste réversible : les index et le graphe argumentatif précédent
  le futur plan de thèse.

Une carte ne doit pas seulement annoncer un thème (`la curiosité`, `la surprise`) ni
résumer une section. Elle doit formuler une affirmation, une hypothèse, une
distinction forte ou une objection que la thèse pourrait soutenir, discuter ou
mettre à l'épreuve.

Le français correct appartient à la carte elle-même : titres, rubriques et prose
doivent être accentués et relus dans `inbox/`. Le générateur du catalogue recopie
fidèlement ce texte et ne doit jamais réparer l'orthographe au moment du rendu.

## Trois niveaux de proposition

Les cartes distinguent désormais trois niveaux qui ne doivent pas être confondus :

- `conceptual` : proposition philosophique ou esthétique sur l'intéressant, la
  création, la compréhension ou la valeur ;
- `scientific` : résultat formel ou empirique, méthode, protocole, algorithme ou
  propriété d'un système scientifique ;
- `articulation` : proposition qui explicite ce qu'une activité, une construction
  ou un résultat scientifique permet de comprendre philosophiquement, sans
  prétendre que le second niveau démontre directement le premier.

Le niveau qualifie le rôle de la carte, pas le genre de sa source. Un article
scientifique peut contenir une intuition conceptuelle, et un essai peut décrire un
résultat scientifique. Une carte d'articulation doit signaler ce qui vient
directement des sources et ce qui relève de la reconstruction proposée par la
thèse. L'index `indexes/by_level.md` permet de parcourir ces trois ensembles.

## Trois vues complémentaires

L'organisation actuelle ne repose pas sur une taxonomie unique :

- `indexes/by_theme.md` rassemble les cartes par objet ou vocabulaire ;
- `indexes/by_level.md` distingue leur statut épistémique ;
- `indexes/by_argument.md` affecte chacune des 123 cartes à une famille
  argumentative principale, de manière exhaustive et réversible.

Le document `ORGANISATION.md` présente les pivots, les recouvrements et les
questions ouvertes. Le registre `relations.tsv` conserve un graphe plus restreint
de relations fortes et typées (`supports`, `limits`, `operationalizes`, etc.). Il
complète les liens associatifs inscrits dans chaque carte sans les remplacer.

## Catalogue partageable

`catalogue-idees.tex` rassemble le texte des 123 cartes dans l'ordre de
`indexes/by_argument.md`, avec leurs statuts, provenances et références. Il est
régénéré depuis les cartes, puis compile en PDF avec :

```bash
python3 scripts/generate_card_catalog.py
mkdir -p output/pdf
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -output-directory=output/pdf cartes/catalogue-idees.tex
```

Le rendu partageable est `output/pdf/catalogue-idees.pdf`. Le générateur refuse
de produire le document si l'index oublie une carte, contient un doublon ou cite
un identifiant inconnu.

On ne crée pas une carte pour chaque détail d'un argument. Les mécanismes, exemples,
résultats expérimentaux et limites restent dans la même carte lorsqu'ils servent une
seule proposition. On sépare deux cartes seulement lorsque les propositions peuvent
être contestées, utilisées ou reliées indépendamment.

## Cycle de travail

1. Lire ou relire un document source.
2. Identifier les propositions non triviales défendues ou suggérées par le texte.
3. Regrouper dans chaque carte les raisons, mécanismes et exemples qui soutiennent
   une même proposition.
4. Noter dans `REGISTRE_TRAITEMENT.md` le niveau de traitement du document.
5. Ajouter ou vérifier la référence dans `bibliographie/references.bib` lorsqu'il
   s'agit d'une publication citable, puis relier sa clé à la carte.
6. Affecter chaque nouvelle carte à une famille dans `indexes/by_argument.md` et
   l'ajouter aux index thématiques pertinents.
7. Si elle soutient, limite ou précise une proposition pivot, ajouter une relation
   expliquée dans `relations.tsv`.
8. Ne pas forcer trop tôt un plan linéaire : laisser les familles émerger.

## Format d'une carte

Chaque carte utilise un en-tête YAML minimal :

```md
---
id: idea_0001
title: "Titre court"
kind: argument
level: conceptual
status: inbox
sources:
  - "chemin/document.pdf"
references:
  - auteur2026mot
tags:
  - interessant
---
```

Les champs `kind` possibles pour l'instant : `definition`, `argument`, `objection`, `example`, `distinction`, `method`, `question`, `hypothesis`, `bibliographic_note`.

Le champ `level` est obligatoire et prend l'une des valeurs `conceptual`,
`scientific` ou `articulation`. `kind` indique la forme logique de la carte ;
`level` indique sa place dans le rapport entre activité scientifique et enquête
philosophique.

Le champ `sources` est obligatoire des qu'une provenance documentaire est connue.
Il contient le chemin exact du ou des documents qui soutiennent la proposition.
Le champ optionnel `source_notes` précise les pages ou sections lorsqu'elles sont
disponibles et fiables. Une carte issue d'une note fragmentaire doit le signaler
explicitement au lieu de présenter l'attribution comme établie.

Le champ optionnel `references` contient les clés de
`bibliographie/references.bib` correspondant aux publications citées. Il ne
remplace pas `sources` : une clé bibliographique identifie une publication, tandis
que le chemin local indique exactement quelle version a été lue.

Les identifiants ne sont jamais réutilisés. Lorsqu'une carte trop faible est
fusionnée ou supprimée, son identifiant et sa destination sont conservés dans
`AUDIT_PROPOSITIONS.md`.
