---
id: idea_0158
title: "Une intelligence inventive doit articuler exploration en largeur et résolution en profondeur"
kind: hypothesis
level: articulation
status: inbox
architecture: test
sources:
  - "input/publications-francois-pachet/pachet-09c.pdf"
  - "input/publications-francois-pachet/barbieri-12a.pdf"
  - "input/publications-francois-pachet/roy-16b.pdf"
  - "input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf"
references:
  - kahneman2011thinking
  - pachet2011markov
  - barbieri2012lyrics
  - papadopoulos2016flowcomposer
  - pachet2026biases
source_notes:
  - "Hidden Biases : version longue de 16 pages soumise à NeurIPS ; la version publique arXiv:2604.07855v1 compte 9 pages."
  - "Kahneman fournit l'opposition métaphorique entre pensée rapide et pensée lente ; largeur et profondeur sont une transposition computationnelle proposée par la carte, non ses catégories."
  - "Markov Constraints, PDF p. 1-8 et 21-23 : couplage entre probabilités locales et recherche globale sous contraintes arbitraires."
  - "Markov Constraints for Lyrics, PDF p. 1-5 : comparaison entre modèle probabiliste seul, contraintes seules et processus markovien contraint."
  - "Assisted Lead Sheet Composition, PDF p. 1-8 et 13-15 : réalisation du couplage dans un outil de composition assistée."
  - "Hidden Biases, version longue soumise à NeurIPS, PDF p. 1-9 : MAP exact NP-difficile et normalisation conditionnelle exacte #P-difficile pour les modèles autorégressifs généraux ; persistance de la difficulté sous certaines contraintes unaires, métriques ou régulières."
tags:
  - intelligence_artificielle
  - transformers
  - resolution_de_problemes
  - contraintes
  - invention
  - combinatoire
---
## Idée

Une intelligence artificielle capable de traiter des problèmes vraiment difficiles ne
devrait être identifiée ni à la seule génération neuronale ni à la seule recherche
symbolique. Elle doit articuler deux régimes complémentaires. Un transformer explore
en largeur : il mobilise rapidement des associations apprises, produit plusieurs
hypothèses, reformulations, analogies et décompositions plausibles. Un solveur explore
en profondeur : SAT, SMT, programmation par contraintes, planification ou démonstration
parcourent avec persistance les conséquences d'une formulation, reviennent en arrière
et fournissent une solution, une preuve, un contre-exemple ou un diagnostic d'échec.

L'opposition de Kahneman entre pensée rapide et pensée lente fournit ici une analogie
féconde. Elle ne doit toutefois pas être transformée en identité : le système 1 et le
système 2 décrivent chez Kahneman des régimes de la cognition humaine, tandis que
largeur et profondeur désignent ici des fonctions dans une architecture de calcul. Un
transformer n'est pas un système 1 psychologique, et un solveur SAT n'est pas un système
2. La transposition sert à poser une question de conception : comment faire coopérer
production intuitive de candidats et examen délibéré de leurs conséquences ?

La coopération décisive est une boucle, non une simple succession. Le modèle neuronal
formalise le problème, propose des variables auxiliaires, des contraintes, des lemmes
ou des décompositions ; le solveur renvoie des conflits, des noyaux insatisfaisables,
des contre-exemples ou des coûts de recherche ; le modèle interprète ces retours et
invente une meilleure représentation. Sur des problèmes NP-difficiles, la contribution
du modèle ne consiste donc pas à abolir la combinatoire. Elle consiste à découvrir la
représentation, la symétrie, l'invariant ou la décomposition qui rend la recherche
effective. L'invention peut résider moins dans la solution finale que dans le langage
intermédiaire qui permet de la trouver.

Les travaux sur les contraintes de Markov constituent un antécédent personnel précis.
Ils couplent un modèle probabiliste, qui ordonne ou échantillonne des continuations
stylistiquement plausibles, avec une recherche globale qui garantit des propriétés de
forme. Les expériences sur les paroles et FlowComposer montrent l'intérêt de cette
division du travail. La version longue de l'article *Hidden Biases in Conditioning
Autoregressive Models*, soumise à NeurIPS, dont une version courte est disponible sur
arXiv, en établit la nécessité computationnelle : le
MAP exact est NP-difficile et la normalisation conditionnelle exacte est #P-difficile
pour les modèles autorégressifs généraux, alors que la génération locale reste facile.
Il montre également qu'une heuristique locale peut déformer la distribution visée.
Ces systèmes ne réalisent pas encore l'architecture générale proposée ici : les
représentations et les contraintes y sont largement données par les concepteurs. Le pas
supplémentaire est de faire porter l'apprentissage sur leur invention et leur révision.

## Hypothèse expérimentale

Comparer, sur des familles de problèmes combinatoires, un transformer seul, un solveur
seul et une boucle hybride. Les instances devraient comporter une structure cachée qui
rend la formulation brute difficile mais une reformulation courte efficace. On
mesurerait le taux de résolution, le temps et la taille de l'arbre de recherche, la
validité vérifiable des résultats, le transfert vers des instances plus grandes et la
réutilisation des abstractions inventées. Le test central serait de déterminer si le
système hybride apprend seulement à choisir de meilleures branches ou s'il découvre
des représentations qui changent effectivement la difficulté pratique du problème.

## Intérêt pour la thèse

La proposition transforme l'IA en laboratoire de l'invention d'un problème et de ses
prises opératoires. Elle fournit une architecture testable pour étudier comment une
intuition large devient une construction profonde, et comment l'échec vérifiable d'une
représentation peut relancer l'invention au lieu de simplement terminer la recherche.

## Liens

- Généralise `idea_0109`, du couplage sampling-contraintes vers une architecture de résolution et d'invention.
- `idea_0100` rappelle que la difficulté dépend du couple représentation-forme, non de la seule contrainte.
- `idea_0085` situe l'invention dans la reconstruction du problème dont l'objet devient la solution.
- `idea_0098` montre pourquoi une solution seulement légale ou vérifiée peut rester inintéressante.
- `idea_0018` permet de traiter cette construction comme un laboratoire philosophique sans en faire une preuve psychologique.
