---
id: idea_0156
title: "La rareté de l'intéressant rend la médiocrité inévitable dans une exploration libre"
kind: hypothesis
level: conceptual
status: inbox
architecture: speculative
sources:
  - "docs/notes/rarete-interessant-mediocrite-liberte.md"
  - "input/De l'impossibilité de créer.pdf"
references:
  - debord1967spectacle
  - muray2005festivus
  - stiegler2010pharmacologie
  - pachet2026impossibilite
source_notes:
  - "Note de travail du 16 août 2026 : formulation, distinctions, prédictions et protocoles proposés par la thèse."
  - "De l'impossibilité de créer, PDF p. 2-7 : rareté des œuvres transformatrices, liquéfaction des contenus, surabondance et crise de la qualité. La thèse du coût d'exploration est une correction proposée ici, non la conclusion du manuscrit."
tags:
  - interessant
  - rarete
  - mediocrite
  - liberte
  - exploration
  - pluralisme
  - culture
---
## Idée

Si les rencontres intéressantes sont des réussites à faible fréquence et si leur
qualité ne peut pas être prédite sûrement avant que les formes soient produites et
rencontrées, une société qui laisse beaucoup de sujets essayer doit tolérer beaucoup
de résultats sans intérêt. La médiocrité n'est pas la cause féconde de l'intéressant ni
une valeur à célébrer : elle est le coût observable d'une exploration dont les réussites
sont rares et partiellement imprévisibles.

Cette hypothèse retourne un diagnostic fréquent de la critique culturelle. La faible
qualité moyenne d'une production abondante ne prouve pas à elle seule qu'un système
aliène les producteurs ou manipule les récepteurs. Elle peut aussi résulter de trois
conditions compatibles avec la liberté : beaucoup d'essais sont permis, l'intéressant
est rare, et les échecs ne peuvent pas tous être éliminés ex ante sans éliminer aussi
des réussites imprévues.

## Formulation située de la rareté

La rareté ne doit pas réifier l'intéressant dans l'objet. Pour un horizon `H`, une
population de sujets `S`, un moment `t`, une règle d'échantillonnage et un seuil `tau`,
on peut poser :

`p = P(I(F, S | H, t) >= tau)`.

L'hypothèse affirme que `p` est faible dans une population de formes non sélectionnée
rétrospectivement. Elle ne dit ni que les mêmes formes intéressent tout le monde, ni que
l'intéressant appartient intrinsèquement à une élite. Plusieurs minorités peuvent
rencontrer des formes différentes dans la queue supérieure de la distribution.

Dans cet argument, « médiocre » signifie seulement que la rencontre n'atteint pas le
seuil de prise retenu. La rareté de l'intéressant ne permet pas de conclure que la forme
est intrinsèquement mauvaise, techniquement incompétente ou moralement indigne. Ces sens
forts exigeraient des critères et une démonstration indépendants.

Il faut aussi définir le seuil par la thèse centrale : une rencontre forte ne se réduit
pas à une préférence ou à un clic ; elle ouvre et soutient une exploration qui paraît
valoir la peine et dans laquelle une prise nouvelle peut devenir crédible. La rareté porte donc sur un effet relationnel et
temporel, non sur une étiquette sociale de prestige.

## Argument statistique du filtre imparfait

La conséquence ne vient pas de la liberté seule. Elle repose sur quatre prémisses
distinctes :

1. **rareté** : sous une règle d'échantillonnage donnée, la probabilité `p` qu'un essai
   ouvre une prise intéressante est inférieure à `1/2` ;
2. **incertitude ex ante** : les distributions des futurs essais intéressants et sans
   intérêt se recouvrent, de sorte qu'aucun filtre disponible ne les sépare parfaitement
   avant leur réalisation ;
3. **liberté productive** : les sujets peuvent essayer sans devoir prouver à ce filtre
   unique la valeur future de leur essai ;
4. **pluralité** : les essais et les horizons de jugement ne sont pas tous des copies
   parfaitement corrélées.

Notons `Y_i = 1` si l'essai `i` franchit le seuil de prise et `Y_i = 0` sinon. Pour `n`
essais indépendants et de même probabilité `p`, le nombre attendu de réussites est `np`
et celui des essais sous le seuil `n(1-p)`. Si `p < 1/2`, les seconds sont majoritaires
en espérance ; lorsque `n` augmente, leur proportion converge vers `1-p`. Dans le même
temps, la probabilité d'obtenir au moins une réussite vaut :

`P(au moins une réussite) = 1-(1-p)^n`.

La même ouverture qui rend visibles beaucoup d'échecs accroît donc la chance de faire
apparaître au moins une réussite rare. Si les essais sont corrélés ou auto-similaires,
la formule d'indépendance ne s'applique plus directement : il faut estimer un nombre
effectif de directions explorées. Cette limite est substantielle, car une augmentation
du volume sans augmentation de la diversité peut multiplier le médiocre sans accroître
la probabilité de l'intéressant.

Considérons ensuite un filtre préalable dont le taux de faux négatifs est
`beta = P(rejet | réussite future)`. Parmi `n` essais, il élimine en moyenne `np beta`
réussites futures. Rendre le filtre plus sévère peut relever la qualité moyenne des
formes publiées, mais, tant que `beta > 0`, cette amélioration se paie par la perte de
formes intéressantes imprévisibles. Un filtre parfait ferait disparaître ce compromis ;
son existence est précisément ce que l'hypothèse d'incertitude refuse de présupposer.

La conclusion est donc conditionnelle mais forte : **si l'intéressant est rare et
imparfaitement prédictible, la liberté d'essayer rend normalement visible une majorité
d'essais sous le seuil ; supprimer cette majorité en amont impose un filtre qui produit
des faux négatifs ou privilégie un horizon particulier.** La liberté ne cause pas la
rareté : elle empêche de masquer statistiquement celle-ci par la seule sélection des
réussites.

## Conséquence politique

Supprimer en amont toutes les productions médiocres exigerait soit un prédicteur parfait
de l'intéressant, soit un centre de sélection autorisé à sacrifier certains horizons et
certaines réussites possibles. Une liberté productive a donc un prix statistique :
tolérer des essais sous le seuil afin de ne pas éliminer tous les vrais positifs
imprévisibles.

Cette défense de l'exploration ne justifie ni l'occupation illimitée de l'attention, ni
l'optimisation industrielle de la répétition. Le droit d'essayer n'est pas un droit à
être imposé à tous. Le régime institutionnel compatible avec l'hypothèse combine une
production ouverte avec des modes d'exposition sélectifs, pluralistes, révisables et
capables de préserver des archives où une forme peut être découverte plus tard.

La proposition fonctionne ainsi comme hypothèse nulle contre les diagnostics
systémiques : ceux-ci restent possibles, mais doivent montrer que la médiocrité observée
excède ce qu'expliquent déjà la rareté des réussites, la corrélation des essais et
l'incertitude ex ante.

## Mise à l'épreuve

L'hypothèse prédit :

1. dans un échantillon non canonique, une médiane faible et une queue rare de rencontres
   ouvrant des prises durables ;
2. quand le nombre et surtout la diversité des essais augmentent, la qualité moyenne ne
   s'élève pas nécessairement, mais le nombre de réussites rares peut croître ;
3. un filtrage centralisé ex ante peut relever la moyenne tout en supprimant des faux
   négatifs de grande valeur et en réduisant la diversité des directions ;
4. des filtres pluralistes et révisables à l'exposition peuvent protéger l'attention
   sans réduire la liberté d'explorer.

Elle serait directement affaiblie si `p` n'était pas faible dans les populations non
sélectionnées, ou si un filtre ex ante conservait une sensibilité proche de `1` dans des
horizons différents tout en supprimant presque tous les essais sous le seuil. Elle
serait également mal formulée si les désaccords entre sujets rendaient impossible
d'identifier une population majoritairement sous le seuil : il faudrait alors parler de
rareté par horizon plutôt que de médiocrité majoritaire en général.

Un protocole fort ferait réaliser à l'aveugle un échantillon de projets acceptés et
refusés par un filtre préalable, puis comparerait qualité moyenne, diversité et queue
supérieure. L'hypothèse serait affaiblie si une sélection forte éliminait durablement la
médiocrité sans diminuer la diversité ni perdre aucune réussite rare. Une comparaison à
budget constant entre nombreuses variantes proches et essais moins nombreux mais plus
divers permettrait en outre de séparer le simple volume de l'exploration effective.

## Intérêt pour la thèse

Cette proposition donne un contenu politique à la rareté de l'intéressant sans revenir
à une théorie élitiste de l'œuvre. Elle déplace l'évaluation d'une société libre : il ne
faut pas lui demander que toute production soit intéressante, mais qu'elle maintienne
les conditions d'une exploration diverse, d'une sélection plurielle et de rencontres
rares qui n'auraient pas pu être certifiées d'avance.

## Liens

- Précise la rareté relationnelle de `idea_0096` sans l'assigner à l'objet seul.
- Limite `idea_0074` : l'abondance ne ferme des possibles que lorsqu'elle homogénéise
  les directions ou monopolise l'attention, non parce qu'elle contient des échecs.
- Prolonge `idea_0105` : une société d'abondance doit construire des trajectoires de
  découverte plutôt que supprimer les essais en amont.
- Reçoit de `idea_0140` la distinction entre genèse descriptive et évaluation normative.
- `idea_0157` sépare le coût d'exploration de la médiocrité industrielle et précise le
  terme « manipulation ».
