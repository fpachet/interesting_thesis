---
id: idea_0017
title: "Une génération contrainte peut être validée tout en biaisant la distribution cible"
kind: argument
level: scientific
status: inbox
sources:
  - "input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf"
references:
  - pachet2026biases
source_notes:
  - "Hidden Biases, distinction entre génération pratique et conditionnement exact, PDF p. 1-3"
  - "Hidden Biases, dureté du conditionnement et de l'approximation, PDF p. 4-9"
  - "Hidden Biases, perte de support, inpainting et limites des résultats, PDF p. 9-14"
tags:
  - ia
  - contraintes
  - autoregressif
  - echantillonnage
---
## Idée

Satisfaire une contrainte ne signifie pas échantillonner exactement le modèle initial
conditionné par cette contrainte. Recherche heuristique, repondération locale,
reranking, rejet ou architecture spécialisée peuvent produire des objets valides tout en
modifiant la loi cible. Le biais est ici inférentiel et non hérite des données
d'apprentissage : le modèle est fixe, mais la procédure de contrôle change ce qui est
effectivement produit.

Cette distorsion prend deux formes indépendantes. La procédure peut conserver toutes les
solutions admissibles mais leur attribuer de mauvais poids; elle peut aussi perdre du
support, lorsqu'un préfixe élimine rend certaines solutions définitivement
inaccessibles. Greedy, top-k, top-p et beam search peuvent provoquer ce second effet en
donnant une probabilité nulle à une bifurcation pourtant nécessaire à une complétion
valide.

Ce n'est pas seulement un défaut d'implémentation. Pour la classe générale des modèles
autoregressifs succincts, le MAP exact est NP-difficile, la normalisation conditionnelle
exacte est #P-difficile, et même une approximation à moins d'un bit de surprisal moyen
par token reste NP-difficile dans le pire cas. Ces résultats ne mesurent cependant pas
le biais d'un système concret et ne disent pas que toute instance pratique est
difficile.

## Intérêt pour la thèse

Cette carte donne un ancrage technique à l'intuition philosophique : une contrainte
n'est pas un simple filtre après coup. La manière de l'imposer transforme la probabilité
des formes et parfois l'espace même de ce qui peut apparaître. Une production
convaincante ne prouve donc ni couverture des possibles ni fidélité au modèle
conditionné.

## Liens

- `idea_0100` précise la frontière entre les cas calculables exactement et les cas difficiles.
- Complète `idea_0016` : une direction globale exige d'anticiper les continuations.
- à distinguer de `idea_0098` : être valide ne garantit ni fidélité distributionnelle ni intérêt.
- Fournit la limite technique du pôle sampling dans la synthèse `idea_0109`.
