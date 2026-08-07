---
id: idea_0098
title: "Satisfaire toutes les contraintes syntaxiques ne permet pas de distinguer une bonne solution"
kind: argument
level: articulation
status: inbox
sources:
  - "input/ERCGrantPachetInterestingness.pdf"
  - "input/old_docs/Synopsis MIT Press.doc"
  - "input/publications-francois-pachet/pachet-06c.pdf"
  - "input/publications-francois-pachet/roy-16b.pdf"
references:
  - pachet2000melodie
  - papadopoulos2016flowcomposer
source_notes:
  - "PDF p. 5"
  - "Synopsis MIT Press, rendu PDF p. 9 et 22"
  - "Qu'est-ce qu'une mélodie intéressante ?, PDF p. 4-5 : près de deux millions d'harmonisations légales de la Marseillaise, que le solveur ne sait pas départager."
  - "Assisted Lead Sheet Composition, PDF p. 11-13 : une réharmonisation de Yesterday est décrite comme nouvelle, valide et stylistiquement Beatles, mais probablement moins intéressante que l'originale."
tags:
  - syntaxe
  - contrainte
  - harmonisation
  - valeur
---
## Idée

Un solveur peut énumérer rapidement toutes les harmonisations conformes aux règles d'un
style sans disposer d'aucun critère pour séparer les solutions musicales des solutions
seulement légales. La correction syntaxique définit l'espace admissible mais ne
l'ordonne pas selon la singularité, l'intérêt ou la valeur.

Le problème de l'intéressant commence donc là où la satisfaction des contraintes
s'arrête. Il exige des propriétés structurelles, notamment à long terme, qui ne sont pas
nécessairement connues avant l'exploration des solutions.

FlowComposer fournit une confirmation particulièrement nette : une réharmonisation de
*Yesterday* peut être nouvelle, valide et reconnaissable comme appartenant au style
des Beatles, tout en étant jugée probablement moins intéressante que l'originale. La
validité, la nouveauté et l'appartenance stylistique ne composent donc pas, même
réunies, un critère suffisant de l'intéressant.

## Intérêt pour la thèse

Cette proposition fournit un cas technique net de la différence entre forme correcte et
forme qui mérite l'attention.

## Liens

- Exemple concret de la troisième couche de `idea_0003`.
- Motive la génération de traits de `idea_0069`.
- `idea_0150` montre symétriquement que l'absence de plagiat est une garantie distincte, elle aussi insuffisante.
