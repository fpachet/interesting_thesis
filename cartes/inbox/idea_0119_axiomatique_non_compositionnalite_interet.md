---
id: idea_0119
title: "L'intérêt du tout ne se déduit pas de l'intérêt de ses parties"
kind: hypothesis
level: conceptual
status: inbox
sources:
  - "projet-these/BUT_DE_LA_THESE.md"
  - "input/projet thèse philo.pdf"
source_notes:
  - "Programme de formalisation : relation entre forme, sujet, horizon collectif et temps"
  - "Projet de thèse V1, temporalité de l'agencement et émergence relationnelle, PDF p. 1-2"
tags:
  - interessant
  - axiomatique
  - formalisation
  - compositionnalite
  - emergence
  - temporalite
---
## Idée

Une axiomatique de l'intéressant doit commencer par préciser sa signature. Soient un
sujet `p`, des objets ou séquences `o`, un horizon `H`, un moment `t`, une évaluation
`I(p, o | H, t)` et une opération `o1 + o2` qui combine deux objets. `I` peut d'abord
être booléen, puis devenir une grandeur ou une trajectoire si les cas l'exigent.

La première propriété candidate est une non-compositionnalité :

`I(p, o1) et I(p, o2)` n'impliquent pas `I(p, o1 + o2)`.

Deux morceaux, idées ou mécanismes intéressants peuvent former un ensemble
inintéressant, confus ou saturé. La réciproque échoue aussi : `I(p, o1 + o2)` n'implique
pas que `I(p, o1)` ou `I(p, o2)`. Une relation, un contraste ou un ordre peut rendre le
tout intéressant alors qu'aucune partie ne l'est isolément. Il n'existe donc pas
nécessairement de fonction indépendante du contexte qui calcule l'intérêt du tout à
partir du seul intérêt de ses parties.

Cette proposition ouvre un programme de propriétés à tester plutôt qu'une liste
d'axiomes déjà admis :

- non-commutativité : changer l'ordre des parties peut changer l'intérêt ;
- non-idempotence : répéter un objet peut l'épuiser, le renforcer ou le révéler ;
- non-monotonie : ajouter une partie peut augmenter ou détruire l'intérêt ;
- dépendance historique : le même couple sujet-objet change avec l'exposition ;
- non-universalité : l'intérêt pour un sujet ne se transmet pas automatiquement à un autre.

Ces « non-lois » ne sont pas des défauts de la théorie. Elles peuvent caractériser un
objet dont la valeur appartient à des agencements et à des transformations plutôt qu'à
une somme de propriétés locales.

## Intérêt pour la thèse

Cette carte donne une forme rigoureuse à plusieurs intuitions du corpus : primauté de
l'agencement temporel, émergence de relations globales, variation avec la mémoire du
sujet et insuffisance des traits locaux. Elle permettrait de comparer musique, jeux,
textes et systèmes génératifs dans un même langage formel.

Le terme « axiomatique » doit rester provisoire. Chaque propriété doit être accompagnée
de cas positifs, de contre-exemples et de conditions de validité. Si toutes les
exceptions sont absorbées dans le contexte `H`, le formalisme deviendrait irréfutable ;
il faut donc spécifier quelles variables contextuelles sont observables et quelles
prédictions la propriété exclut.

## Liens

- Formalise la primauté de l'agencement dans `idea_0001`.
- Étend la contrainte mutuelle des dimensions décrite dans `idea_0039`.
- Reprend la dépendance au sujet et au temps de `idea_0071` et `idea_0084`.
- Fournit un cadre aux dissociations entre préférence et intérêt de `idea_0118`.
- Doit rester limitée par l'exigence de falsifiabilité de `idea_0095`.
