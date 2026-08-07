---
id: idea_0150
title: "Une séquence peut être statistiquement nouvelle et pourtant copier le corpus"
kind: distinction
level: scientific
status: inbox
architecture: case
sources:
  - "input/publications-francois-pachet/papadopoulos-14a.pdf"
  - "input/publications-francois-pachet/max_order.pdf"
references:
  - papadopoulos2014avoiding
  - papadopoulos2016nonplagiaristic
source_notes:
  - "Avoiding Plagiarism, PDF p. 1-2 et 7 : l'ordre de Markov borne la mémoire utilisée pour apprendre, mais non la longueur des fragments recopiés pendant la génération."
  - "Generating non-plagiaristic Markov sequences, PDF p. 1-4 et 15-18 : formulation par no-goods, perte de solutions et échantillonnage exact sous contrainte de maximum order."
tags:
  - ia
  - generation
  - nouveaute
  - plagiat
  - markov
  - contraintes
  - trajectoire_scientifique
---
## Idée

Une marche aléatoire dans un modèle de Markov peut produire une séquence qui n'existe
pas comme totalité dans le corpus tout en recopiant mot pour mot de longs fragments de
celui-ci. Augmenter l'ordre du modèle accentue même ce risque : l'ordre borne la
longueur du contexte utilisé pendant l'apprentissage, mais ne borne pas la longueur des
fragments que plusieurs transitions successives peuvent reconstituer à la génération.

La nouveauté statistique d'une sortie, sa plausibilité locale et l'absence de copie sont
donc trois propriétés distinctes. Pour garantir la dernière, les travaux sur
`MAXORDER` construisent explicitement l'ensemble des fragments interdits, puis
échantillonnent parmi les séquences qui n'en contiennent aucun. Le chapitre de 2016
montre en outre qu'une marche aléatoire dans l'automate des séquences admissibles
déforme encore leurs probabilités ; l'échantillonnage exact exige une propagation
globale.

## Statut de la source

La distinction entre ordre d'apprentissage et longueur effectivement recopiée, ainsi
que la garantie algorithmique de non-copie, sont des résultats propres aux deux
publications. Leur portée esthétique est plus limitée : éviter tout fragment interdit
ne suffit pas à rendre une production intéressante, originale au sens fort ou adaptée
à son matériau.

## Intérêt pour la thèse

Ce cas donne une forme technique précise au risque de substitution de cible. Déclarer
une sortie « nouvelle » parce qu'elle n'est pas identique à un objet du corpus laisse
échapper les copies longues ; garantir la non-copie résout ce problème précis, mais ne
classe toujours pas les formes selon leur intérêt. L'originalité doit ainsi être
décomposée en propriétés testables sans être confondue avec l'intéressant.

## Liens

- Précise la critique de l'apprentissage des répétitions dans `idea_0054`.
- Fournit un cas scientifique à la recomposition forme--matière de `idea_0080`.
- Complète `idea_0098` : une solution non plagiaire peut rester seulement admissible.
- Prolonge `idea_0017` : satisfaire une contrainte ne garantit pas que l'échantillonnage respecte la loi conditionnelle visée.
