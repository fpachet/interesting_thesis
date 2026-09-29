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
  - "Discussion du 29 septembre 2026, prompt sur la solution en quête de son problème : critères de reconstruction explicative et épreuve par variations ; extension proposée pour la thèse, non résultat établi par les publications citées. Voir la Défense, § 4.4."
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
dans lequel cette forme appartient à une petite classe de solutions. L'hypothèse est
que rendre sensible cette sélectivité peut engager une exploration intéressante.
La stabilité de la forme et la difficulté de sa découverte sont des propriétés
distinctes : aucune ne prouve à elle seule que les solutions soient peu nombreuses.

Tester cette hypothèse suppose d'inférer depuis l'objet le problème qu'il semble
résoudre, puis de comparer ses propriétés aux autres solutions légales. La rareté est
donc relative à une formulation du problème, non absolue dans le monde.

Le compromis est délicat : une contrainte trop générale laisse tant de solutions qu'elle
ne produit aucune rareté perceptible ; une contrainte trop particulière peut fabriquer
artificiellement une solution unique sans lui donner de portée. La rareté devient
signifiante lorsque des contraintes assez génériques relient globalement les parties de
l'objet tout en laissant une petite classe de solutions.

Le « Boulez Blues » fournit un cas construit de cette géométrie : les probabilités du
blues tonal de Charlie Parker sont croisées avec une contrainte `AllDifferent` issue
d'un principe sériel. Le résultat occupe une région extrêmement peu probable du modèle
et n'est atteint que par recherche globale. Le papier qualifie la combinaison
d'intéressante, mais ne mesure pas sa réception. Ce cas atteste une faible probabilité
sous le modèle et la difficulté de l'atteindre par génération locale ; il ne suffit
pas à établir un petit nombre de solutions admissibles ni leur intérêt pour un auditeur.

## Rareté, sélectivité et explication

Trois propriétés doivent être examinées séparément :

- **Rareté statistique** : faible probabilité d'un objet sous un modèle déterminé.
- **Sélectivité du problème** : petit nombre de solutions dans un espace admissible
  précisé, avec une granularité et, si nécessaire, des classes d'équivalence explicites.
- **Puissance explicative** : les contraintes rendent intelligibles des traits de
  l'objet et permettent des comparaisons ou des anticipations contrôlables.

Une solution statistiquement rare n'est pas forcément isolée parmi les solutions
légales. Un problème à solution unique peut ne rien expliquer. Inversement, une
reconstruction peut éclairer une forme tout en admettant beaucoup de solutions.
La sélectivité appartient donc à l'hypothèse particulière de cette carte ; elle
n'est pas une condition de toute reconstruction féconde ni de tout intérêt.

## Écarter les problèmes fabriqués sur mesure

« Trouver exactement cette séquence » sélectionne un objet sans expliquer sa forme.
Une condition cryptographique peut également sélectionner, dans un domaine fini
donné, un objet unique sans éclairer ses propriétés perceptibles. La brièveté de
la condition ne suffit donc pas à lui donner une portée explicative.

Le prompt du 29 septembre propose quatre dimensions : sélectivité, simplicité,
pertinence sémantique et reconstructibilité. Pour tester l'hypothèse, on les précise
ainsi et on leur adjoint une épreuve :

1. **Sélectivité.** Établir ou estimer la taille de la classe de solutions, sans la
   déduire du sentiment d'unicité ni de la difficulté du calcul.
2. **Simplicité relative.** Le problème ne doit pas recopier sa solution. Sa concision
   dépend du vocabulaire disponible ; un code court arbitraire n'est pas pour autant
   une explication, et une formulation élaborée peut être pertinente.
3. **Pertinence sémantique.** Les contraintes portent sur des propriétés du domaine
   dont le rôle peut être discuté, comme la continuité d'une mélodie ou la mobilité
   harmonique. Un vocabulaire familier ne garantit pas à lui seul leur pertinence.
4. **Reconstructibilité située.** Des traits de l'objet, des connaissances du sujet
   ou des comparaisons accessibles fournissent des indices pour formuler le problème.
   Cette possibilité dépend du sujet, de son horizon et du moment de l'enquête.
5. **Épreuve par variations.** La reconstruction permet de comprendre ce que des
   variantes conserveraient ou feraient perdre. Elle peut être contestée par une
   alternative qui réussit là où elle prévoyait un échec, ou par un transfert manqué.

Ces dimensions forment une grille de mise à l'épreuve, non une définition ni un score
garantissant l'intérêt. La cinquième relie la reconstruction à une prise contrôlable
(`idea_0123`). Dans le cas Jotney, comparer des substitutions harmoniques doit préciser
ce qui arrive à l'autonomie mélodique et à la mobilité harmonique. L'optale et la
pseudoptale (`idea_0113`) obligent à distinguer ces effets de la seule familiarité.

Le problème reconstruit peut différer de celui du créateur, et plusieurs formulations
peuvent expliquer des aspects différents de l'objet (`idea_0085`). Leur évaluation
porte sur ce qu'elles permettent de comprendre et d'éprouver. Une promesse déçue peut
avoir suscité un intérêt réel : l'échec de la reconstruction limite sa fécondité,
sans effacer rétrospectivement l'expérience (`idea_0124`).

## Intérêt pour la thèse

Cette proposition donne une interprétation computationnelle à la nécessité inventée et à
l'autostabilité des formes.

## Liens

- Propose une opérationnalisation partielle de `idea_0085` ; la rareté ne suffit pas à établir la nécessité ressentie ou l'autostabilité de `idea_0087`.
- `idea_0113` fournit l'épreuve par variantes et le faux positif de la familiarité.
- `idea_0123` distingue l'intérêt déclenché de la prise effectivement acquise.
- `idea_0124` empêche de confondre promesse de reconstruction et fécondité attestée.
- Doit être distinguée de la simple popularité de `idea_0053`.
- Fournit le pôle résolution de problèmes de `idea_0109`.
