---
id: idea_0016
title: "La génération a besoin d'un sens de la direction"
kind: argument
level: articulation
status: inbox
sources:
  - "input/old_docs/Paper citations_updated.docx"
  - "input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf"
  - "input/publications-francois-pachet/roy-16b.pdf"
  - "input/publications-francois-pachet/pachet-17d.pdf"
references:
  - pachet2026biases
  - papadopoulos2016flowcomposer
  - pachet2017variations
source_notes:
  - "Projet SenseOfDirection, résumé et challenge, rendu PDF p. 1-3"
  - "Projet SenseOfDirection, corrélations longues et synthèse, rendu PDF p. 5-6"
  - "Hidden Biases, contraintes de forme globales et dépendance aux continuations futures, PDF p. 1-3 et 12-14"
  - "Assisted Lead Sheet Composition, PDF p. 10-11 : génération autonome localement cohérente mais sans direction, et besoin de modèles de répétitions, variations et sections."
  - "Sampling Variations, PDF p. 1-2 et 6 : répétitions et variations imposées pour produire une cohérence à longue portée et l'impression d'une intention."
tags:
  - ia
  - generation
  - structure
  - direction
---
## Idée

Les systèmes génératifs imitent souvent des styles locaux, mais peinent à produire des
objets structures avec début, fin, climax, cohérence et direction. Une suite de
transitions plausibles ne suffit pas : la forme doit présenter des corrélations
ordonnées à plusieurs échelles, de la reprise locale jusqu'aux relations entre grandes
parties.

Le sens de la direction ne désigne donc pas nécessairement un plan explicite fixe à
l'avance. Il est l'impression qu'une séquence conserve, transforme et prépare ses
matériaux de telle sorte que les événements tardifs répondent aux précédents. Imposer le
patron d'une œuvre existante donne une structure superficielle; il faut que la structure
produite corresponde au contenu qu'elle organise.

Le problème possède aussi une forme computationnelle précise : une exigence portant sur
la fin, le mètre ou une position future couple les choix présents à l'ensemble de leurs
continuations possibles. Une bonne probabilité locale ne dit donc pas si le chemin
pourra satisfaire la forme globale, ni s'il restera probable une fois cette forme
imposée.

FlowComposer fournit un cas expérimental de cette limite. Les compositeurs utilisent
rarement la génération autonome au-delà de huit mesures : les fragments restent
localement cohérents, mais les pièces longues requièrent répétitions, variations et
sections. Le mécanisme de 2017 impose ces relations à longue portée et obtient une
forme qui « semble composée avec des intentions ». Ce succès reste partiel, puisque la
structure est empruntée à une œuvre cible plutôt qu'engendrée avec son propre matériau.

## Intérêt pour la thèse

Cette carte relie l'intéressant à la structure temporelle globale : un objet intéressant
doit savoir où il va, ou au moins donner cette impression.

## Liens

- Proche de `idea_0017`.
- Proche de `idea_0019` pour la chanson comme équilibre oriente.
