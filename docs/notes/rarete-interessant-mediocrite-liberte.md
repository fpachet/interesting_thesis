# Rareté de l'intéressant, médiocrité et liberté

## Proposition de départ

François Pachet propose d'étudier l'idée suivante : **l'intéressant est rare**.
Cette rareté permettrait de retourner une famille de critiques de la culture de masse
au XXe siècle. Là où ces critiques expliquent volontiers l'abondance de productions
médiocres par un système d'aliénation, de spectacle, de festivisme ou de captation, on
peut faire l'hypothèse qu'une faible proportion de réussites est aussi le régime normal
d'une société où beaucoup de personnes sont libres d'essayer, de publier et de juger.

La thèse ne serait pas que la médiocrité est bonne, ni que les industries culturelles
sont innocentes. Elle serait plus précisément que **la possibilité de produire des
essais médiocres est une condition de l'exploration libre, tandis que leur domination
de l'espace d'exposition est un problème distinct**.

## Éviter une cible trop homogène

Les trois auteurs envisagés ne forment pas une école « technophobe » homogène.

- Chez Guy Debord, le spectacle n'est pas un simple ensemble de mauvaises images ou de
  contenus trompeurs : c'est un rapport social médiatisé par les images. La cible est
  la séparation organisée par la forme marchande de la vie sociale.
- Philippe Muray construit avec *Homo festivus*, puis *Festivus festivus*, une figure
  satirique de l'individu posthistorique qui célèbre et administre sa propre fête. Son
  registre est celui de la caricature critique plus que celui d'une théorie causale
  testable des médias.
- Bernard Stiegler ne récuse pas la technique comme telle. Sa pharmacologie la pense
  simultanément comme poison et remède ; sa critique vise le contrôle industriel du
  *pharmakon*, la prolétarisation et la destruction des circuits longs de l'attention.

La cible défendable est donc une **forme de diagnostic systémique unilatéral** : le
passage trop rapide de « beaucoup de productions sont médiocres » à « un système les a
rendues médiocres pour aliéner ou manipuler les sujets ». Cette critique conserve ce
que les diagnostics de Debord et Stiegler rendent visible — médiation, asymétrie de
pouvoir, formation de l'attention — tout en contestant leur emploi comme explication
exhaustive de la distribution de la qualité.

## Hypothèse principale

Pour un horizon `H`, une population de sujets `S`, un moment `t`, une règle
d'échantillonnage explicite et un seuil de prise `tau`, posons :

`p = P(I(F, S | H, t) >= tau)`.

Dire que l'intéressant est rare signifie que `p` est faible dans un ensemble de
productions non sélectionné rétrospectivement. La rareté n'est donc ni une essence de
l'objet ni une simple impression élitiste : elle est une propriété mesurable d'une
distribution située de rencontres.

Dans ce raisonnement, « médiocre » doit recevoir un sens minimal : une rencontre qui
n'atteint pas le seuil de prise retenu. La rareté de l'intéressant n'implique pas que la
forme soit intrinsèquement mauvaise, techniquement incompétente ou moralement indigne.
Si « médiocre » conserve l'un de ces sens forts, l'argument ne suit plus et exige une
preuve indépendante.

L'hypothèse politique qui s'y articule est la suivante :

> Lorsque les formes intéressantes sont des réussites à faible fréquence et qu'on ne
> peut pas les identifier sûrement avant leur production, une société qui garantit à
> beaucoup de sujets la liberté d'essayer doit tolérer un grand nombre de productions
> sans intérêt. Éliminer toute médiocrité en amont exige soit un prédicteur que
> l'hypothèse tient pour indisponible, soit un filtrage centralisé qui supprime aussi
> des réussites imprévisibles.

La médiocrité n'est pas ici une cause positive de l'intéressant. Elle est le **coût
d'exploration** rendu visible par la rareté des réussites et par l'incertitude ex ante.
Pour `n` essais indépendants et de probabilité `p`, le nombre attendu d'échecs vaut
`n(1-p)` et la probabilité d'au moins une réussite `1-(1-p)^n`. Si `p < 1/2`, les
échecs sont majoritaires en espérance et leur proportion converge vers `1-p`. Pour des
essais corrélés ou auto-similaires, il faut estimer un nombre effectif de directions
réellement explorées : le volume seul ne suffit pas.

Un filtre ex ante introduit un second terme. Si son taux de faux négatifs est
`beta = P(rejet | réussite future)`, il élimine en moyenne `np beta` réussites. Tant que
les distributions prédictives des essais futurs intéressants et sans intérêt se
recouvrent, diminuer les faux positifs en renforçant le filtre se paie donc par des
réussites rares perdues. La liberté ne produit pas la rareté ; elle interdit de masquer
celle-ci en ne laissant apparaître que les essais déjà certifiés par un filtre.

Cette hypothèse ne réfute donc pas par principe les critiques systémiques. Elle leur
oppose une hypothèse nulle : avant d'attribuer la faible qualité moyenne à l'aliénation
ou à la manipulation, il faut montrer qu'elle excède ce que produiraient déjà la rareté
des réussites et l'incertitude d'une exploration libre.

## Distinction décisive

Deux régimes de médiocrité ne doivent pas être confondus.

1. **Médiocrité exploratoire** : résultat d'un essai dont l'issue était incertaine,
   qui explore éventuellement une région nouvelle, reste abandonnable et n'impose pas
   son exposition. Elle est le déchet normal d'un processus de recherche distribué.
2. **Médiocrité d'exploitation** : production répétitive volontairement optimisée pour
   occuper l'attention, minimiser le risque, reproduire une formule ou verrouiller la
   distribution. Elle peut être abondante sans explorer davantage et réduire la
   probabilité que des formes rares soient rencontrées.

Cette distinction réconcilie partiellement la proposition avec *De l'impossibilité de
créer*. La surabondance y devient pathologique lorsqu'elle homogénéise les manières de
faire et monopolise l'attention, non du seul fait que beaucoup d'essais échouent.

## Que peut vouloir dire « manipulation » ?

Le terme est trop fort s'il désigne toute influence d'un dispositif sur un sujet :
toute médiation ordonne les possibilités et transforme l'attention. Il devient
opératoire si l'on exige au moins trois éléments :

1. une architecture ou une intervention identifiable ;
2. un effet causal sur l'action ou le jugement, établi par comparaison
   contrefactuelle ;
3. une asymétrie pertinente — dissimulation, contournement des raisons du sujet ou
   poursuite d'une fin contraire à ses préférences réfléchies.

Un contenu médiocre n'est donc pas, par lui-même, manipulateur. Une plateforme peut
manipuler avec un contenu excellent ; une production médiocre peut circuler sans plan
de manipulation. Le concept doit qualifier une relation causale et normative entre un
dispositif, une conduite et des intérêts, non une propriété esthétique du contenu.

## Prédictions et tests

### Distribution de base

Échantillonner sans filtre rétrospectif des chansons, textes, vidéos ou propositions,
puis recueillir des jugements situés et des indices de prise durable. L'hypothèse
prévoit une distribution à longue traîne : médiane faible, petit nombre de rencontres
fortes, désaccord partiel entre horizons. Un corpus canonique seul ne convient pas,
car il conditionne déjà l'observation sur la survie.

### Filtrage ex ante

Faire présélectionner des projets ou esquisses, réaliser aussi un échantillon de ce qui
a été refusé, puis évaluer les œuvres obtenues à l'aveugle. La thèse prédit que le
filtrage augmente éventuellement la qualité moyenne, mais produit des faux négatifs
dans la queue supérieure et peut réduire la diversité des solutions. Elle est affaiblie
si un filtrage fort supprime durablement la médiocrité sans réduire ni la diversité ni
le nombre de réussites rares.

### Volume contre diversité

Comparer, à budget constant, plusieurs régimes de génération : beaucoup de variantes
proches, moins d'essais plus divers, et exploration distribuée entre plusieurs sujets.
La seule quantité ne devrait pas augmenter mécaniquement l'intéressant ; la diversité
des directions et la pluralité des juges devraient mieux prédire la queue supérieure.

### Production et exposition

Séparer expérimentalement la liberté de produire de l'obligation de recevoir. Un
système peut autoriser beaucoup d'essais tout en utilisant des parcours, filtres
pluralistes et archives pour protéger l'attention. Le meilleur régime attendu n'est ni
la rareté imposée par la censure ni le flux intégral, mais **exploration ouverte et
exposition sélective révisable**.

### Test de manipulation

Maintenir les contenus constants et randomiser l'ordre, les notifications, les
valeurs par défaut ou l'information disponible. Mesurer non seulement le clic, mais le
jugement ultérieur du sujet sur la conduite induite. Ce protocole sépare l'effet du
dispositif de la qualité du contenu et rend réfutable l'attribution de manipulation.

## Sources contrôlées

- Guy Debord, *La Société du spectacle*, 1967, notamment les thèses 4 à 6 ; texte de
  la troisième édition reproduit par les Classiques des sciences sociales :
  <https://classiques.uqam.ca/contemporains/debord_guy/societe_du_spectacle/spectacle.html>.
- Philippe Muray et Élisabeth Lévy, *Festivus festivus*, Fayard, 2005 ; notice de
  l'éditeur : <https://www.hachette.fr/livre/festivus-festivus-9782213621296>.
- Bernard Stiegler, *Ce qui fait que la vie vaut la peine d'être vécue. De la
  pharmacologie*, Flammarion, 2010 ; présentation d'Ars Industrialis :
  <https://arsindustrialis.org/ce-qui-fait-que-la-vie-vaut-le-peine-d%C3%AAtre-v%C3%A9cue>.
- François Pachet, *De l'impossibilité de créer*, PDF p. 2-7 sur création,
  « contenus », surabondance et crise de la qualité.
