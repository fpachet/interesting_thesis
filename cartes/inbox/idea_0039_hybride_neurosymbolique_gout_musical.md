---
id: idea_0039
title: "L'interessant d'une sequence nait de dimensions qui se contraignent mutuellement"
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
  - "NetNeg condense, apprentissage neuronal et negociation de contraintes, PDF p. 1-6"
  - "Modele unifie attente/contexte/metre, PDF p. 1-6"
  - "NetNeg developpe, architecture, experiences et limites, PDF p. 1-18"
  - "Projet SenseOfDirection, idee 3 sur la multidimensionnalite, rendu PDF p. 6"
  - "Dossier Jotney, profil analytique et equilibre melodie-harmonie, PDF p. 19-23 et 29-36"
tags:
  - musique
  - neurosymbolique
  - gout
  - apprentissage
---

## Idee

Une longue sequence interessante n'est jamais seulement melodique, harmonique,
rythmique ou sonore. Son interet peut apparaitre dans l'accord ou le conflit entre
ces dimensions : un timbre rend une harmonie singuliere, une orchestration donne
une fonction a une melodie, ou un reseau de personnages revele une structure que
l'intrigue seule ne montre pas. Modeliser chaque dimension independamment fait
disparaitre ces relations transversales.

Cette pluralite concerne aussi les representations. Les attentes ne sont ni
entierement deductibles de regles, ni reductibles a des frequences apprises. Un
modele peut faire negocier regles symboliques, concepts graduels, signal audio et
apprentissage statistique; l'echec d'une representation devient alors une
information exploitable par les autres plutot qu'une erreur terminale.

Dans NetNeg, cette cooperation est operationnelle : le reseau propose des notes
selon les regularites apprises, puis des agents negocient entre ces preferences et
les regles du contrepoint. Les essais separes echouent de facons complementaires :
le reseau produit des continuations plausibles mais illegales, les regles seules
des solutions legales mais pauvres. La qualite vient de leur compromis repete.

Le cas Jotney rend cette contrainte mutuelle particulierement nette : la mobilite
harmonique n'est interessante que si la melodie conserve sa coherence, tandis que
l'autonomie melodique devient perceptible parce qu'elle traverse les changements
d'harmonie. Mesurer une dimension sans l'autre manquerait donc precisement
l'equilibre que l'analyse cherche a expliquer.

## Interet pour la these

Cette carte formule une hypothese sur l'interessant et fournit une architecture
possible pour la tester sans reduire l'objet a une seule dimension.

## Liens

- Proche de `idea_0011`.
- Proche de `idea_0006`.
- Generalise l'equilibre musical de `idea_0111` en hypothese multidimensionnelle.
