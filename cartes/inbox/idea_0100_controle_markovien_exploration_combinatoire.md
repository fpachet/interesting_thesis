---
id: idea_0100
title: "La difficulté d'une contrainte dépend de l'état conjoint du modèle et de la forme"
kind: argument
level: scientific
status: inbox
sources:
  - "input/ERCGrantPachetInterestingness.pdf"
  - "input/old_docs/Paper citations_updated.docx"
  - "input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf"
references:
  - pachet2026biases
source_notes:
  - "PDF p. 6"
  - "Projet SenseOfDirection, corrélations longues et contraintes globales, rendu PDF p. 3-5"
  - "Hidden Biases, opposition entre état borne et contexte autoregressif général, PDF p. 3 et 10-14"
tags:
  - markov
  - controle
  - generation
  - combinatoire
---
## Idée

Une contrainte simple ou même régulière n'est pas automatiquement facile à imposer. Sa
tractabilité dépend du couple forme-modèle. Si le modèle possède un état suffisant
borne, comme un modèle de Markov d'ordre fini, et si la contrainte est reconnue par un
automate fini, leur produit fournit un état conjoint borne : programmation dynamique,
échantillonnage conditionnel exact et MAP exact deviennent alors calculables en temps
polynomial.

Pour un modèle autoregressif général, l'automate de la contrainte ne résume pas la
dépendance du modèle a tout le préfixe. Chaque décision requiert alors la masse des
continuations futures encore compatibles, sans statistique suffisante bornée générique.
La difficulté ne sépare donc pas simplement local et global, ni Markov et contrainte :
elle sépare les couples qui admettent une recursion d'état bornée de ceux qui exigent de
sommer ou d'optimiser globalement sur les suffixes.

## Intérêt pour la thèse

Cette proposition relie une limite technique précise des générateurs à la question
philosophique du sens de la direction. Elle évite aussi une conclusion trop forte : la
combinatoire d'une forme globale n'interdit pas toujours un contrôle exact; tout dépend
de la représentation conjointe du modèle et de la contrainte.

## Liens

- Précise `idea_0017`, qui décrit le biais produit lorsque le calcul exact est remplace par une heuristique.
- Donne une base technique a `idea_0016` sur les structures longues.
- à rapprocher du problème de la fin dans `idea_0082`.
- Décrit les conditions de calcul de l'articulation proposée dans `idea_0109`.
