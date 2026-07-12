---
id: idea_0039
title: "L'intéressant d'une séquence naît de dimensions qui se contraignent mutuellement"
kind: method
level: scientific
status: inbox
sources:
  - "input/old_docs/interestingness/fp perso/fdp/Papiers/Future of Music book/interestingness/Dan Gang/aaai99A.pdf"
  - "input/old_docs/interestingness/fp perso/fdp/Papiers/Future of Music book/interestingness/Dan Gang/aaai99B.pdf"
  - "input/old_docs/interestingness/fp perso/fdp/Papiers/Future of Music book/interestingness/Dan Gang/netneg.pdf"
  - "input/old_docs/Paper citations_updated.docx"
  - "input/The Mystery of Jotney Songs -full.pdf"
references:
  - gang1999unified
  - goldman1999netneg
source_notes:
  - "NetNeg condense, apprentissage neuronal et négociation de contraintes, PDF p. 1-6"
  - "Modèle unifie attente/contexte/mètre, PDF p. 1-6"
  - "NetNeg développe, architecture, expériences et limites, PDF p. 1-18"
  - "Projet SenseOfDirection, idée 3 sur la multidimensionnalite, rendu PDF p. 6"
  - "Dossier Jotney, profil analytique et équilibre mélodie-harmonie, PDF p. 19-23 et 29-36"
tags:
  - musique
  - neurosymbolique
  - gout
  - apprentissage
---
## Idée

Une longue séquence intéressante n'est jamais seulement mélodique, harmonique, rythmique
ou sonore. Son intérêt peut apparaître dans l'accord ou le conflit entre ces dimensions
: un timbre rend une harmonie singulière, une orchestration donne une fonction à une
mélodie, ou un réseau de personnages révèle une structure que l'intrigue seule ne montre
pas. Modéliser chaque dimension indépendamment fait disparaître ces relations
transversales.

Cette pluralité concerne aussi les représentations. Les attentes ne sont ni entièrement
déductibles de règles, ni réductibles à des fréquences apprises. Un modèle peut faire
négocier règles symboliques, concepts graduels, signal audio et apprentissage
statistique; l'échec d'une représentation devient alors une information exploitable par
les autres plutôt qu'une erreur terminale.

Dans NetNeg, cette coopération est opérationnelle : le réseau propose des notes selon
les régularités apprises, puis des agents négocient entre ces préférences et les règles
du contrepoint. Les essais séparés échouent de façons complémentaires : le réseau
produit des continuations plausibles mais illégales, les règles seules des solutions
légales mais pauvres. La qualité vient de leur compromis répété.

Le cas Jotney rend cette contrainte mutuelle particulièrement nette : la mobilité
harmonique n'est intéressante que si la mélodie conserve sa cohérence, tandis que
l'autonomie mélodique devient perceptible parce qu'elle traverse les changements
d'harmonie. Mesurer une dimension sans l'autre manquerait donc précisément l'équilibre
que l'analyse cherche à expliquer.

## Intérêt pour la thèse

Cette carte formule une hypothèse sur l'intéressant et fournit une architecture possible
pour la tester sans réduire l'objet à une seule dimension.

## Liens

- Proche de `idea_0011`.
- Proche de `idea_0006`.
- Généralise l'équilibre musical de `idea_0111` en hypothèse multidimensionnelle.
