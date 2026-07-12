---
id: idea_0069
title: "La popularite musicale exige des traits generes, pas seulement mesures"
kind: method
level: scientific
status: inbox
sources:
  - "input/ERCGrantPachetInterestingness.pdf"
  - "old docs /ERCGrantPachetInterestingness (1).docx"
source_notes:
  - "Grant ERC PDF p. 5-6"
tags:
  - erc
  - popularite
  - signal_processing
  - features
---

## Idee

Les traits audio generiques ne suffisent pas a expliquer la popularite ou la
qualite d'une harmonisation. Un apprentissage de descripteurs doit pouvoir inventer
des proprietes adaptees a une tache supervisee, notamment des relations
melodico-harmoniques et des structures longues.

La reduction usuelle d'un morceau a un sac de trames detruit precisement ces
relations temporelles. Generer de bons traits exige donc de representer la sequence
entiere au lieu d'agreger des mesures locales avant l'apprentissage.

## Interet pour la these

Cette carte relie l'interessant a la construction active des descripteurs.

## Liens

- Proche de `idea_0013`.
- Proche de `idea_0026`.
