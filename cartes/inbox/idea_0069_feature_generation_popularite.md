---
id: idea_0069
title: "La popularité musicale exige des traits générés, pas seulement mesurés"
kind: method
level: scientific
status: inbox
sources:
  - "input/ERCGrantPachetInterestingness.pdf"
source_notes:
  - "Grant ERC PDF p. 5-6"
tags:
  - erc
  - popularite
  - signal_processing
  - features
---
## Idée

Les traits audio génériques ne suffisent pas à expliquer la popularité ou la qualité
d'une harmonisation. Un apprentissage de descripteurs doit pouvoir inventer des
propriétés adaptées à une tâche supervisée, notamment des relations mélodico-harmoniques
et des structures longues.

La réduction usuelle d'un morceau à un sac de trames détruit précisément ces relations
temporelles. Générer de bons traits exige donc de représenter la séquence entière au
lieu d'agréger des mesures locales avant l'apprentissage.

## Intérêt pour la thèse

Cette carte relie l'intéressant à la construction active des descripteurs.

## Liens

- Proche de `idea_0013`.
- Proche de `idea_0026`.
