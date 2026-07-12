---
id: idea_0029
title: "Un motif fréquent n'est intéressant que par l'effet qu'il produit sur des croyances"
kind: argument
level: scientific
status: inbox
sources:
  - "input/old_docs/kdd95.pdf"
  - "input/old_docs/interestingness/fp perso/fdp/Papiers/Future of Music book/interestingness/tkde.pdf"
references:
  - silberschatz1995subjective
  - silberschatz1996patterns
source_notes:
  - "Silberschatz et Tuzhilin, croyances dures et souples, révision et mesure bayésienne, PDF p. 3-7"
  - "Version étendue, formalismes de degrés de croyance et processus de découverte, PDF p. 5-12"
tags:
  - knowledge_discovery
  - croyance
  - subjectivite
  - surprise
---
## Idée

La fréquence ou la régularité statistique d'un motif ne suffit pas à établir son
intérêt. Le même motif peut être trivial pour un utilisateur qui l'attend et décisif
pour un autre dont il contredit les croyances. Une mesure subjective de l'intéressant
doit donc représenter l'état de croyance avant la découverte et évaluer l'ampleur de sa
révision, plutôt que noter le motif seul.

Une contradiction n'appelle toutefois pas toujours la même révision. Si elle heurte une
croyance tenue pour une contrainte dure, elle signale d'abord une erreur possible dans
les données. Si elle heurte une croyance souple et que les données sont confirmées,
c'est le degré de croyance qui doit changer. L'intérêt d'un motif ne mesure donc pas
seulement un écart : il distribue le doute entre observation et modèle du monde.

## Intérêt pour la thèse

Cette carte donne une formulation opérationnelle du contexte subjectif : l'intéressant
dépend de ce qu'un sujet croyait déjà.

## Liens

- Proche de `idea_0002`.
- Proche de `idea_0027`.
- Complète la distinction surprise/action de `idea_0036`.
