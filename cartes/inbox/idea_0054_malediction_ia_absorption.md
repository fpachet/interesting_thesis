---
id: idea_0054
title: "L'IA apprend nos répétitions plutôt que la singularité des œuvres"
kind: argument
level: conceptual
status: inbox
sources:
  - "input/De l'impossibilité de créer.pdf"
  - "input/old_docs/Paper citations_updated.docx"
  - "input/publications-francois-pachet/ghedini-15b.pdf"
  - "input/publications-francois-pachet/papadopoulos-14a.pdf"
  - "input/publications-francois-pachet/max_order.pdf"
references:
  - ghedini2015flowmachines
  - papadopoulos2014avoiding
  - papadopoulos2016nonplagiaristic
source_notes:
  - "PDF p. 83-87"
  - "Projet SenseOfDirection, critique du style transfer, rendu PDF p. 2-5"
  - "Creating Music and Texts with Flow Machines, PDF p. 10-14 : opérationnalisation du style par un corpus et questions sur la typicalité humaine."
  - "Avoiding Plagiarism et Generating Non-Plagiaristic Markov Sequences, PDF p. 1-3 : un ordre plus élevé renforce l'impression de style en recopiant des fragments parfois bien plus longs que le contexte appris."
tags:
  - ia
  - corpus
  - creation
  - appropriation
---
## Idée

Un modèle génératif apprend ce qui revient assez souvent pour former une régularité. Un
corpus d'œuvres radicalement singulières et sans points communs lui apparaîtrait comme
du bruit. Sa performance ne prouve donc pas qu'il a absorbé l'essence des œuvres ; elle
révèle l'ampleur de l'auto-similarité de nos productions.

Utilisée comme anti-modèle, l'IA peut cartographier ce qui vient facilement, les pentes
statistiques d'un style et les solutions déjà disponibles. Créer avec elle consisterait
alors moins à accepter ses sorties qu'à chercher précisément ce qu'elle ne sait pas
généraliser.

Le transfert de style illustre cette limite : il peut reproduire une texture locale tout
en empruntant à une cible la structure globale qui lui manque. Cette apparence de
direction ne prouve pas que le modèle a appris à engendrer une forme adaptée à son
propre contenu.

Les expériences `MAXORDER` rendent cette limite mesurable. Augmenter l'ordre de
Markov améliore l'impression d'imitation, mais permet de reconstituer des fragments du
corpus beaucoup plus longs que cet ordre. Le système n'a pas absorbé une œuvre comme
singularité : il réenchaîne ses répétitions locales jusqu'à produire, parfois, une
copie longue qu'une contrainte supplémentaire doit explicitement interdire.

## Intérêt pour la thèse

Cette carte prolonge la question de la création impossible vers celle de la dépossession
contemporaine.

## Liens

- Proche de `idea_0055`.
- Proche de `idea_0017`.
- `idea_0150` isole le résultat scientifique sur la longueur des copies générées.
