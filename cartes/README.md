# Cartes d'idees

Ce dossier sert de boite de reception pour les idees extraites du corpus.

Le principe est volontairement simple :

- une carte = une proposition substantielle et manipulable ;
- les cartes commencent dans `inbox/` avec le statut `inbox` ;
- le registre indique quels documents ont ete lus, partiellement lus, ou seulement inventories ;
- l'organisation reste reversible : les index et le graphe argumentatif precedent
  le futur plan de these.

Une carte ne doit pas seulement annoncer un theme (`la curiosite`, `la surprise`) ni
resumer une section. Elle doit formuler une affirmation, une hypothese, une
distinction forte ou une objection que la these pourrait soutenir, discuter ou
mettre a l'epreuve.

Le français correct appartient à la carte elle-même : titres, rubriques et prose
doivent être accentués et relus dans `inbox/`. Le générateur du catalogue recopie
fidèlement ce texte et ne doit jamais réparer l'orthographe au moment du rendu.

## Trois niveaux de proposition

Les cartes distinguent desormais trois niveaux qui ne doivent pas etre confondus :

- `conceptual` : proposition philosophique ou esthetique sur l'interessant, la
  creation, la comprehension ou la valeur ;
- `scientific` : resultat formel ou empirique, methode, protocole, algorithme ou
  propriete d'un systeme scientifique ;
- `articulation` : proposition qui explicite ce qu'une activite, une construction
  ou un resultat scientifique permet de comprendre philosophiquement, sans
  pretendre que le second niveau demontre directement le premier.

Le niveau qualifie le role de la carte, pas le genre de sa source. Un article
scientifique peut contenir une intuition conceptuelle, et un essai peut decrire un
resultat scientifique. Une carte d'articulation doit signaler ce qui vient
directement des sources et ce qui releve de la reconstruction proposee par la
these. L'index `indexes/by_level.md` permet de parcourir ces trois ensembles.

## Trois vues complementaires

L'organisation actuelle ne repose pas sur une taxonomie unique :

- `indexes/by_theme.md` rassemble les cartes par objet ou vocabulaire ;
- `indexes/by_level.md` distingue leur statut epistemique ;
- `indexes/by_argument.md` affecte chacune des 112 cartes a une famille
  argumentative principale, de maniere exhaustive et reversible.

Le document `ORGANISATION.md` presente les pivots, les recouvrements et les
questions ouvertes. Le registre `relations.tsv` conserve un graphe plus restreint
de relations fortes et typees (`supports`, `limits`, `operationalizes`, etc.). Il
complete les liens associatifs inscrits dans chaque carte sans les remplacer.

## Catalogue partageable

`catalogue-idees.tex` rassemble le texte des 112 cartes dans l'ordre de
`indexes/by_argument.md`, avec leurs statuts, provenances et references. Il est
regenere depuis les cartes, puis compile en PDF avec :

```bash
python3 scripts/generate_card_catalog.py
mkdir -p output/pdf
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -output-directory=output/pdf cartes/catalogue-idees.tex
```

Le rendu partageable est `output/pdf/catalogue-idees.pdf`. Le generateur refuse
de produire le document si l'index oublie une carte, contient un doublon ou cite
un identifiant inconnu.

On ne cree pas une carte pour chaque detail d'un argument. Les mecanismes, exemples,
resultats experimentaux et limites restent dans la meme carte lorsqu'ils servent une
seule proposition. On separe deux cartes seulement lorsque les propositions peuvent
etre contestees, utilisees ou reliees independamment.

## Cycle de travail

1. Lire ou relire un document source.
2. Identifier les propositions non triviales defendues ou suggerees par le texte.
3. Regrouper dans chaque carte les raisons, mecanismes et exemples qui soutiennent
   une meme proposition.
4. Noter dans `REGISTRE_TRAITEMENT.md` le niveau de traitement du document.
5. Ajouter ou verifier la reference dans `bibliographie/references.bib` lorsqu'il
   s'agit d'une publication citable, puis relier sa cle a la carte.
6. Affecter chaque nouvelle carte a une famille dans `indexes/by_argument.md` et
   l'ajouter aux index thematiques pertinents.
7. Si elle soutient, limite ou precise une proposition pivot, ajouter une relation
   expliquee dans `relations.tsv`.
8. Ne pas forcer trop tot un plan lineaire : laisser les familles emerger.

## Format d'une carte

Chaque carte utilise un en-tete YAML minimal :

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
`level` indique sa place dans le rapport entre activite scientifique et enquete
philosophique.

Le champ `sources` est obligatoire des qu'une provenance documentaire est connue.
Il contient le chemin exact du ou des documents qui soutiennent la proposition.
Le champ optionnel `source_notes` precise les pages ou sections lorsqu'elles sont
disponibles et fiables. Une carte issue d'une note fragmentaire doit le signaler
explicitement au lieu de presenter l'attribution comme etablie.

Le champ optionnel `references` contient les cles de
`bibliographie/references.bib` correspondant aux publications citees. Il ne
remplace pas `sources` : une cle bibliographique identifie une publication, tandis
que le chemin local indique exactement quelle version a ete lue.

Les identifiants ne sont jamais reutilises. Lorsqu'une carte trop faible est
fusionnee ou supprimee, son identifiant et sa destination sont conserves dans
`AUDIT_PROPOSITIONS.md`.
