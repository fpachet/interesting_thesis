---
id: idea_0017
title: "Une generation contrainte peut etre valide tout en biaisant la distribution cible"
kind: argument
level: scientific
status: inbox
sources:
  - "input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf"
references:
  - pachet2026biases
source_notes:
  - "Hidden Biases, distinction entre generation pratique et conditionnement exact, PDF p. 1-3"
  - "Hidden Biases, durete du conditionnement et de l'approximation, PDF p. 4-9"
  - "Hidden Biases, perte de support, inpainting et limites des resultats, PDF p. 9-14"
tags:
  - ia
  - contraintes
  - autoregressif
  - echantillonnage
---

## Idee

Satisfaire une contrainte ne signifie pas echantillonner exactement le modele
initial conditionne par cette contrainte. Recherche heuristique, reponderation
locale, reranking, rejet ou architecture specialisee peuvent produire des objets
valides tout en modifiant la loi cible. Le biais est ici inferentiel et non herite
des donnees d'apprentissage : le modele est fixe, mais la procedure de controle
change ce qui est effectivement produit.

Cette distorsion prend deux formes independantes. La procedure peut conserver
toutes les solutions admissibles mais leur attribuer de mauvais poids; elle peut
aussi perdre du support, lorsqu'un prefixe elimine rend certaines solutions
definitivement inaccessibles. Greedy, top-k, top-p et beam search peuvent provoquer
ce second effet en donnant une probabilite nulle a une bifurcation pourtant
necessaire a une completion valide.

Ce n'est pas seulement un defaut d'implementation. Pour la classe generale des
modeles autoregressifs succincts, le MAP exact est NP-difficile, la normalisation
conditionnelle exacte est #P-difficile, et meme une approximation a moins d'un bit
de surprisal moyen par token reste NP-difficile dans le pire cas. Ces resultats ne
mesurent cependant pas le biais d'un systeme concret et ne disent pas que toute
instance pratique est difficile.

## Interet pour la these

Cette carte donne un ancrage technique a l'intuition philosophique : une contrainte
n'est pas un simple filtre apres coup. La maniere de l'imposer transforme la
probabilite des formes et parfois l'espace meme de ce qui peut apparaitre. Une
production convaincante ne prouve donc ni couverture des possibles ni fidelite au
modele conditionne.

## Liens

- `idea_0100` precise la frontiere entre les cas calculables exactement et les cas difficiles.
- Complete `idea_0016` : une direction globale exige d'anticiper les continuations.
- A distinguer de `idea_0098` : etre valide ne garantit ni fidelite distributionnelle ni interet.
- Fournit la limite technique du pole sampling dans la synthese `idea_0109`.
