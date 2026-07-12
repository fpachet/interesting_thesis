---
id: idea_0100
title: "La difficulte d'une contrainte depend de l'etat conjoint du modele et de la forme"
kind: argument
level: scientific
status: inbox
sources:
  - "input/ERCGrantPachetInterestingness.pdf"
  - "input/old_docs/Paper citations_updated.docx"
  - "input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf"
references:
  - pachet2026biases
source_notes:
  - "PDF p. 6"
  - "Projet SenseOfDirection, correlations longues et contraintes globales, rendu PDF p. 3-5"
  - "Hidden Biases, opposition entre etat borne et contexte autoregressif general, PDF p. 3 et 10-14"
tags:
  - markov
  - controle
  - generation
  - combinatoire
---

## Idee

Une contrainte simple ou meme reguliere n'est pas automatiquement facile a imposer.
Sa tractabilite depend du couple forme-modele. Si le modele possede un etat suffisant
borne, comme un modele de Markov d'ordre fini, et si la contrainte est reconnue par
un automate fini, leur produit fournit un etat conjoint borne : programmation
dynamique, echantillonnage conditionnel exact et MAP exact deviennent alors
calculables en temps polynomial.

Pour un modele autoregressif general, l'automate de la contrainte ne resume pas la
dependance du modele a tout le prefixe. Chaque decision requiert alors la masse des
continuations futures encore compatibles, sans statistique suffisante bornee
generique. La difficulte ne separe donc pas simplement local et global, ni Markov et
contrainte : elle separe les couples qui admettent une recursion d'etat bornee de
ceux qui exigent de sommer ou d'optimiser globalement sur les suffixes.

## Interet pour la these

Cette proposition relie une limite technique precise des generateurs a la question
philosophique du sens de la direction. Elle evite aussi une conclusion trop forte :
la combinatoire d'une forme globale n'interdit pas toujours un controle exact; tout
depend de la representation conjointe du modele et de la contrainte.

## Liens

- Precise `idea_0017`, qui decrit le biais produit lorsque le calcul exact est remplace par une heuristique.
- Donne une base technique a `idea_0016` sur les structures longues.
- A rapprocher du probleme de la fin dans `idea_0082`.
- Decrit les conditions de calcul de l'articulation proposee dans `idea_0109`.
