---
id: idea_0069
title: "La popularité musicale exige des traits générés, pas seulement mesurés"
kind: method
level: scientific
status: inbox
sources:
  - "input/ERCGrantPachetInterestingness.pdf"
  - "input/publications-francois-pachet/pachet-08c.pdf"
references:
  - pachetroy2008hitsong
source_notes:
  - "Grant ERC PDF p. 5-6"
  - "Hit Song Science Is Not Yet a Science, PDF p. 2-5 : 98 descripteurs audio génériques, 98 descripteurs spécifiques et 629 étiquettes humaines échouent à prédire les trois classes de popularité au-delà du hasard."
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

L'expérience de 2008 est ici un résultat négatif utile, non la preuve qu'un nouveau
descripteur résoudra nécessairement le problème. Elle montre que l'ajout massif de
mesures disponibles, y compris d'annotations humaines, ne suffit pas lorsque les traits
ne construisent pas la propriété relationnelle pertinente ou lorsque la cible elle-même
est produite par une dynamique sociale.

## Intérêt pour la thèse

Cette carte relie l'intéressant à la construction active des descripteurs.

## Liens

- Proche de `idea_0013`.
- Proche de `idea_0026`.
