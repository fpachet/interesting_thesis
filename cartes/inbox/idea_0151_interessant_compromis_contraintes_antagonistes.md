---
id: idea_0151
title: "L'intéressant peut être modélisé comme un compromis entre contraintes antagonistes"
kind: argument
level: articulation
status: inbox
architecture: case
sources:
  - "input/publications-francois-pachet/pachet-99m.pdf"
  - "input/Tonal_Parsimony_in_Chord_Sequence_Analysis.pdf"
references:
  - pachet1999programs
  - pachet2026tonalparsimony
source_notes:
  - "Automatic Generation of Music Programs, PDF p. 2 : le choix musical est ramené à deux désirs contradictoires, répétition et surprise, dont il faut trouver le bon compromis."
  - "Automatic Generation of Music Programs, PDF p. 4-5 et 8 : la qualité visée porte sur une séquence ; la continuité stylistique est exprimée par une contrainte de similarité, la variété par des contraintes de différence et de cardinalité."
  - "Automatic Generation of Music Programs, PDF p. 13-14 : un titre inconnu devient acceptable grâce à la continuité du programme ; les résultats qualitatifs annoncés restent préliminaires."
  - "Tonal Parsimony, arXiv:2606.03459v1, sections 2, 4 et 10 : la continuité locale C et la cardinalité globale K ne sont plus négociées comme un compromis scalaire, mais ordonnées lexicographiquement."
tags:
  - interessant
  - musique
  - contraintes
  - similarite
  - difference
  - continuite
  - rupture
  - surprise
  - repetition
  - trajectoire_scientifique
---
## Idée

Dans *Automatic Generation of Music Programs*, le problème de la sélection musicale
n'est pas traité comme l'optimisation d'une préférence unique. Il est formulé à partir
de deux désirs dits contradictoires : retrouver ce que l'on connaît et aime, mais aussi
rencontrer ce que l'on ne connaît pas encore. La solution n'est donc ni la répétition
pure ni la surprise pure, mais un compromis construit à l'échelle d'une séquence.

La parcimonie tonale prolonge cette architecture locale-globale tout en la transformant.
Le nombre de changements de tonalité `C` porte sur la continuité de la trajectoire ; le
nombre de tonalités distinctes `K` porte sur la cardinalité de son vocabulaire global.
Mais les critères ne sont pas additionnés : ils sont ordonnés lexicographiquement, de
sorte que la compression du vocabulaire ne peut acheter une transition supplémentaire.
Ce choix montre qu'une tension entre contraintes peut être réglée par priorité autant
que par compromis, et que cette priorité constitue elle-même une hypothèse musicale à
soumettre aux cas d'anti-compression.

RecitalComposer donne une forme calculable à ce compromis. Des contraintes de
similarité assurent une continuité locale entre les styles ; des contraintes de
différence et de cardinalité imposent de la variété à l'ensemble du programme. Un titre
qui ne serait pas particulièrement désirable isolément peut ainsi devenir « le bon
morceau au bon moment ». L'intéressant n'est plus seulement cherché dans un score
attribué à chaque objet : il peut émerger de la compatibilité provisoire entre des
exigences antagonistes distribuées dans le temps.

## Statut de la source

Le papier établit effectivement l'opposition répétition--surprise et formalise les
contraintes de similarité, différence et cardinalité. Il parle de continuité et de
variété, non d'une théorie générale de l'intéressant ni d'une contrainte explicite de
rupture. La thèse reformule la variété comme possibilité de rupture de la continuité,
mais cette extension doit rester signalée. De même, l'évaluation qualitative rapportée
avec des experts est préliminaire et ne démontre pas que les séquences calculées sont
intéressantes pour tout auditeur.

## Intérêt pour la thèse

Ce travail personnel fournit un antécédent formel direct à l'idée que l'intéressant
naît souvent d'une tension maintenue plutôt que de la maximisation d'une propriété.
Similarité et différence, continuité et possibilité de rupture, familiarité et surprise
ne sont pas des critères indépendants à additionner : chacun limite l'excès de l'autre.

La thèse relationnelle ajoute toutefois le sujet et son histoire. Une même combinaison
de contraintes peut être trop répétitive pour un auditeur, trop discontinue pour un
autre, ou changer de valeur au fil de l'écoute. Le système décrit donc des dispositions
de la séquence à intéresser, non une mesure complète de `I(F, S | H, t)`.

## Liens

- Renforce `idea_0014` : le parcours possède des propriétés irréductibles aux morceaux.
- Donne une source publiée au compromis abstrait de `idea_0103` entre ordre et hasard.
- Précise `idea_0005` : la continuité rend une surprise assimilable sans suffire à la rendre intéressante.
- Prolonge `idea_0146` : le programme objectiviste passe ici de la mélodie au programme musical.
- Trouve dans `idea_0159` un prolongement harmonique et une limite : l'ordre lexicographique produit une prise compacte, mais peut encore effacer une différence fonctionnelle.
