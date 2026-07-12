---
id: idea_0027
title: "L'intéressant mesure un progrès de compression, pas une surprise"
kind: argument
level: articulation
status: inbox
sources:
  - "input/old_docs/interestingness.pdf"
  - "input/ERCGrantPachetInterestingness.pdf"
references:
  - schmidhuber1997interesting
source_notes:
  - "Schmidhuber, What's Interesting?, PDF p. 1-4 et 18-21"
  - "ERCGrantPachetInterestingness, beauté compressible et intérêt comme dérivée, PDF p. 2"
tags:
  - schmidhuber
  - compression
  - curiosite
  - theorie
---
## Idée

L'intérêt ne vient ni de la complexité d'un objet, ni de sa nouveauté, ni de sa surprise
prises séparément. Il vient du progrès que fait l'observateur lorsqu'il découvre une
régularité qui rend les données plus simples à représenter ou à prédire. Autrement dit,
ce qui est récompensé n'est pas la compression déjà acquise, mais l'amélioration du
compresseur ou du modèle.

Cette proposition explique dans un même mouvement pourquoi le parfaitement prévisible et
le bruit blanc sont ennuyeux. Le premier est déjà compressé et ne produit plus de
progrès ; le second reste incompressible et ne permet aucun progrès durable. Une
surprise n'est intéressante que si elle annonce une régularité apprenable.

Dans le papier de 1997, Schmidhuber formule ce mécanisme en termes de régularités
inattendues faciles à apprendre et de récompense pour croissance des connaissances. Il
ne parle pas encore explicitement de `compression progress`. Le projet ERC reformule
ensuite l'intérêt comme dérivée d'une beauté comprise en termes de compressibilité. La
carte distingue donc la proposition générale du papier source et cette reformulation, au
lieu d'attribuer anachroniquement l'expression au rapport de 1997.

Le mécanisme de confiance est essentiel. Une erreur de prédiction ne suffit pas : le
système ne récompense une surprise que lorsqu'une partie s'était engagée sur un résultat
et que l'autre pouvait raisonnablement anticiper son erreur. Cette condition empêche le
bruit blanc de devenir une réserve illimitée de récompenses.

## Intérêt pour la thèse

Cette proposition donne un critère opérationnel plus fort que la simple "zone entre
trivialité et bruit" : on peut rechercher une variation de performance prédictive ou
descriptive chez un observateur donné. Elle permet aussi de distinguer l'intéressant de
l'étonnant.

## Liens

- Proche de `idea_0005`, qui affirme déjà que l'inattendu ne suffit pas.
- Complétée par `idea_0071`, sur la disparition de l'intérêt une fois la régularité apprise.
