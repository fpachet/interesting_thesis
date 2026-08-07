---
id: idea_0096
title: "Un objet peut être intéressant parce qu'il apparaît comme une solution rare d'un problème implicite"
kind: hypothesis
level: articulation
status: inbox
sources:
  - "input/ERCGrantPachetInterestingness.pdf"
  - "input/old_docs/Synopsis MIT Press.doc"
  - "input/old_docs/TBKLullyNOTES.doc"
  - "input/publications-francois-pachet/pachet-06c.pdf"
  - "input/publications-francois-pachet/pachet-09c.pdf"
references:
  - pachet2000melodie
  - pachet2011markov
source_notes:
  - "PDF p. 4"
  - "Synopsis MIT Press, rendu PDF p. 22-23"
  - "TBKLullyNOTES, palindromes comme solutions rares, rendu PDF p. 6"
  - "Qu'est-ce qu'une mélodie intéressante ?, PDF p. 5-6 : hypothèse de la solution unique, avec la réserve qu'un problème trop particulier fabrique artificiellement l'unicité."
  - "Markov Constraints, PDF p. 8-9 : le Boulez Blues combine style tonal et AllDifferent, produisant une solution de très faible probabilité inaccessible en pratique à une marche gloutonne."
tags:
  - rarete
  - probleme
  - solution
  - combinatoire
---
## Idée

La rareté pertinente n'est pas la faible fréquence brute d'un objet. En percevant une
forme, le sujet peut reconstruire implicitement un espace combinatoire de contraintes
dans lequel cette forme constitue une solution peu nombreuse, stable ou difficile à
atteindre. L'objet devient intéressant parce qu'il rend sensible la petitesse de la
classe de solutions dont il fait partie.

Tester cette hypothèse suppose d'inférer depuis l'objet le problème qu'il semble
résoudre, puis de comparer ses propriétés aux autres solutions légales. La rareté est
donc relative à une formulation du problème, non absolue dans le monde.

Le compromis est délicat : une contrainte trop générale laisse tant de solutions qu'elle
ne produit aucune rareté perceptible; une contrainte trop particulière peut fabriquer
artificiellement une solution unique sans lui donner de portée. La rareté devient
signifiante lorsque des contraintes assez génériques relient globalement les parties de
l'objet tout en laissant une petite classe de solutions.

Le « Boulez Blues » fournit un cas construit de cette géométrie : les probabilités du
blues tonal de Charlie Parker sont croisées avec une contrainte `AllDifferent` issue
d'un principe sériel. Le résultat occupe une région extrêmement peu probable du modèle
et n'est atteint que par recherche globale. Le papier qualifie la combinaison
d'intéressante, mais ne mesure pas sa réception ; il établit la rareté relative au
problème, non la thèse générale selon laquelle toute solution rare intéresse.

## Intérêt pour la thèse

Cette proposition donne une interprétation computationnelle à la nécessité inventée et à
l'autostabilité des formes.

## Liens

- Opérationnalise `idea_0085` et `idea_0087`.
- Doit être distinguée de la simple popularité de `idea_0053`.
- Fournit le pôle résolution de problèmes de `idea_0109`.
