---
id: idea_0027
title: "L'interessant mesure un progres de compression, pas une surprise"
kind: argument
level: articulation
status: inbox
sources:
  - "old docs /interestingness.pdf"
  - "input/ERCGrantPachetInterestingness.pdf"
source_notes:
  - "Schmidhuber, What's Interesting?, PDF p. 1-4 et 18-21"
  - "ERCGrantPachetInterestingness, beaute compressible et interet comme derivee, PDF p. 2"
tags:
  - schmidhuber
  - compression
  - curiosite
  - theorie
---

## Idee

L'interet ne vient ni de la complexite d'un objet, ni de sa nouveaute, ni de sa
surprise prises separement. Il vient du progres que fait l'observateur lorsqu'il
decouvre une regularite qui rend les donnees plus simples a representer ou a
predire. Autrement dit, ce qui est recompense n'est pas la compression deja
acquise, mais l'amelioration du compresseur ou du modele.

Cette proposition explique dans un meme mouvement pourquoi le parfaitement
previsible et le bruit blanc sont ennuyeux. Le premier est deja compresse et ne
produit plus de progres ; le second reste incompressible et ne permet aucun
progres durable. Une surprise n'est interessante que si elle annonce une
regularite apprenable.

Dans le papier de 1997, Schmidhuber formule ce mecanisme en termes de regularites
inattendues faciles a apprendre et de recompense pour croissance des connaissances.
Il ne parle pas encore explicitement de `compression progress`. Le projet ERC
reformule ensuite l'interet comme derivee d'une beaute comprise en termes de
compressibilite. La carte distingue donc la proposition generale du papier source
et cette reformulation, au lieu d'attribuer anachroniquement l'expression au
rapport de 1997.

Le mecanisme de confiance est essentiel. Une erreur de prediction ne suffit pas :
le systeme ne recompense une surprise que lorsqu'une partie s'etait engagee sur un
resultat et que l'autre pouvait raisonnablement anticiper son erreur. Cette
condition empeche le bruit blanc de devenir une reserve illimitee de recompenses.

## Interet pour la these

Cette proposition donne un critere operationnel plus fort que la simple "zone entre
trivialite et bruit" : on peut rechercher une variation de performance predictive
ou descriptive chez un observateur donne. Elle permet aussi de distinguer
l'interessant de l'etonnant.

## Liens

- Proche de `idea_0005`, qui affirme deja que l'inattendu ne suffit pas.
- Completee par `idea_0071`, sur la disparition de l'interet une fois la regularite apprise.
