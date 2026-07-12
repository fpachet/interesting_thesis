# Cartes d'idees

Ce dossier sert de boite de reception pour les idees extraites du corpus.

Le principe est volontairement simple :

- une carte = une proposition substantielle et manipulable ;
- les cartes commencent dans `inbox/` avec le statut `inbox` ;
- le registre indique quels documents ont ete lus, partiellement lus, ou seulement inventories ;
- l'organisation fine vient plus tard, dans les index et dans un futur plan de these.

Une carte ne doit pas seulement annoncer un theme (`la curiosite`, `la surprise`) ni
resumer une section. Elle doit formuler une affirmation, une hypothese, une
distinction forte ou une objection que la these pourrait soutenir, discuter ou
mettre a l'epreuve.

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
5. Ajouter les cartes aux index thematiques si un regroupement devient evident.
6. Ne pas forcer trop tot un plan lineaire : laisser les familles emerger.

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

Les identifiants ne sont jamais reutilises. Lorsqu'une carte trop faible est
fusionnee ou supprimee, son identifiant et sa destination sont conserves dans
`AUDIT_PROPOSITIONS.md`.
