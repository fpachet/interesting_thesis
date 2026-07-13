---
id: idea_0071
title: "L'intérêt suit le gradient de progrès d'un observateur, non son erreur actuelle"
kind: hypothesis
level: articulation
status: inbox
sources:
  - "input/old_docs/interestingness.pdf"
  - "input/The Mystery of Jotney Songs.pdf"
  - "input/PACHET_HISTOIRE_OREILLE_BAT.pdf"
references:
  - schmidhuber1997interesting
  - schmidhuber2009compression
  - oudeyer2007intrinsic
  - oudeyer2007typology
  - pachet2018oreille
source_notes:
  - "Schmidhuber, What's Interesting?, PDF p. 1-2 et 18-20"
  - "Kaplan, Oudeyer et Hafner, progrès d'apprentissage, niches de progrès et développement autonome, IEEE 2007, p. 265-286"
  - "Jotney, variation de la surprise avec la formation de l'oreille, PDF p. 3"
  - "Histoire d'une oreille, fascination, saturation puis usage parcimonieux de la neuveclamine, PDF p. 23-24 ; solutions devenues évidentes après réécoute, p. 285."
tags:
  - schmidhuber
  - compression
  - apprentissage
  - temporalite
  - subjectivite
  - curiosite-artificielle
  - gradient
  - niche-de-progres
---
## Idée

Si l'intérêt correspond à un progrès de compression, il ne peut pas être une propriété
stable de l'objet. Il dépend de ce que l'observateur sait déjà, de ce qu'il est capable
de calculer et du moment de son apprentissage. La régularité qui provoque aujourd'hui un
gain de compréhension devient demain une connaissance acquise et donc une source
d'ennui.

Cette proposition est plus précise que l'affirmation générale selon laquelle les goûts
sont subjectifs : elle indique quelle transformation interne fait varier l'intérêt.
Apprendre détruit progressivement la récompense qui a motivé l'apprentissage et force la
curiosité à changer d'objet.

Il n'existe donc pas de proportion universelle entre information attendue et inattendue.
La frontière entre trivial et aléatoire se déplace avec les savoirs et les capacités de
calcul de l'observateur.

Les travaux de Kaplan, Oudeyer et Hafner permettent de préciser cette transformation
comme un gradient. Si `E_t(o, S)` désigne l'erreur de prédiction du sujet `S` confronté
à l'objet ou à la situation `o`, un signal simple de progrès est `P_t(o, S) = E_{t-Δ}(o,
S) - E_t(o, S)`. L'intérêt ne suit donc pas le niveau actuel de l'erreur, mais sa
diminution. Une situation maîtrisée produit peu d'erreur mais aucun progrès ; une
situation aléatoire ou trop difficile produit beaucoup d'erreur mais aucun progrès ; une
situation intéressante est celle où la compétence est en train d'augmenter.

Cette mesure définit des **niches de progrès**, locales et temporaires dans l'espace des
situations accessibles. Un agent curieux choisit les régions où son modèle s'améliore le
plus vite, puis les quitte lorsque le progrès s'aplatit. Il construit ainsi sans
curriculum prédéfini une trajectoire allant vers des activités de difficulté croissante.
Le gradient n'est pas une propriété de l'objet seul : il naît de la rencontre entre ce
que l'objet permet de percevoir ou d'essayer et les compétences, biais, moyens d'action
et expériences déjà acquis par le sujet.

Schmidhuber formule un principe voisin en termes de progrès de compression : la
récompense de curiosité vient de l'amélioration du compresseur ou du prédicteur, non de
la surprise brute. Les deux familles de travaux convergent donc sur une dérivée
temporelle de l'apprentissage, même si leurs architectures et leurs mesures ne sont pas
identiques.

La neuveclamine en donne une micro-histoire concrète : découverte fascinante,
reproduction intensive, saturation, puis réapprentissage d'un usage rare et presque
indétectable. L'effet ne disparaît pas simplement ; sa valeur dépend de la manière dont
l'attente est de nouveau préparée après son assimilation.

## Intérêt pour la thèse

Elle permet de définir l'intéressant comme une relation dynamique entre une forme et
l'état d'un observateur. Elle donne aussi une mesure candidate du travail constructif :
une construction est en cours lorsque les erreurs diminuent ou que les prises
s'améliorent. Elle prédit enfin qu'une œuvre peut rester intéressante si elle offre
plusieurs régularités découvrables à des échelles ou des moments différents, plutôt
qu'une seule surprise rapidement épuisée.

## Liens

- Conséquence temporelle de `idea_0027`.
- Précise `idea_0001` et `idea_0002` par un mécanisme d'apprentissage.
- Éclaire `idea_0004` : l'ennui peut être l'effet normal d'une compréhension réussie.
- Le cas Jotney montre aussi que certaines formes survivent à l'épuisement de leur première surprise.
- Dynamise la zone de flow de `idea_0121` en y distinguant les régions où le sujet progresse réellement.
- Opérationnalise une partie du travail constructif de `idea_0123` sans réduire toute construction à la prédiction.
