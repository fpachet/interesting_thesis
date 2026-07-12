---
id: idea_0029
title: "Un motif frequent n'est interessant que par l'effet qu'il produit sur des croyances"
kind: argument
level: scientific
status: inbox
sources:
  - "input/old_docs/kdd95.pdf"
  - "input/old_docs/interestingness/fp perso/fdp/Papiers/Future of Music book/interestingness/tkde.pdf"
source_notes:
  - "Silberschatz et Tuzhilin, croyances dures et souples, revision et mesure bayesienne, PDF p. 3-7"
  - "Version etendue, formalismes de degres de croyance et processus de decouverte, PDF p. 5-12"
tags:
  - knowledge_discovery
  - croyance
  - subjectivite
  - surprise
---

## Idee

La frequence ou la regularite statistique d'un motif ne suffit pas a etablir son
interet. Le meme motif peut etre trivial pour un utilisateur qui l'attend et
decisif pour un autre dont il contredit les croyances. Une mesure subjective de
l'interessant doit donc representer l'etat de croyance avant la decouverte et
evaluer l'ampleur de sa revision, plutot que noter le motif seul.

Une contradiction n'appelle toutefois pas toujours la meme revision. Si elle
heurte une croyance tenue pour une contrainte dure, elle signale d'abord une erreur
possible dans les donnees. Si elle heurte une croyance souple et que les donnees
sont confirmees, c'est le degre de croyance qui doit changer. L'interet d'un motif
ne mesure donc pas seulement un ecart : il distribue le doute entre observation et
modele du monde.

## Interet pour la these

Cette carte donne une formulation operationnelle du contexte subjectif : l'interessant depend de ce qu'un sujet croyait deja.

## Liens

- Proche de `idea_0002`.
- Proche de `idea_0027`.
- Complete la distinction surprise/action de `idea_0036`.
