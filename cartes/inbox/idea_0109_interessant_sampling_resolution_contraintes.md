---
id: idea_0109
title: "Produire de l'intéressant exige souvent d'articuler sampling et résolution de contraintes"
kind: hypothesis
level: articulation
status: inbox
sources:
  - "input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf"
  - "input/Notes thèse.pdf"
  - "input/ERCGrantPachetInterestingness.pdf"
  - "input/old_docs/interestingness/fp perso/fdp/Papiers/Future of Music book/interestingness/Dan Gang/aaai99A.pdf"
  - "input/old_docs/interestingness/fp perso/fdp/Papiers/Future of Music book/interestingness/Dan Gang/netneg.pdf"
  - "input/publications-francois-pachet/pachet-09c.pdf"
  - "input/publications-francois-pachet/barbieri-12a.pdf"
  - "input/publications-francois-pachet/roy-16b.pdf"
  - "input/publications-francois-pachet/pachet12b.pdf"
references:
  - pachet2026biases
  - goldman1999netneg
  - pachet2011markov
  - barbieri2012lyrics
  - papadopoulos2016flowcomposer
  - pachet2012virtuosity
source_notes:
  - "Discussion du 29 septembre 2026, prompt sur la solution en quête de son problème : distinction entre contraintes de production et reconstructibilité à la réception ; proposition d'évaluation séparée de la sélectivité, de la reconstruction et de l'intérêt."
  - "Discussion avec l'auteur du 28 septembre 2026 : précision sur les limites d'un critère d'intérêt fixé sur les propriétés finales et sur la détermination progressive du problème, de la solution et des critères."
  - "Hidden Biases : version longue de 16 pages soumise à NeurIPS ; la version publique arXiv:2604.07855v1 compte 9 pages."
  - "Hidden Biases, insuffisance du sampling local pour les propriétés globales, PDF p. 1-3 et 10-14"
  - "Notes thèse, doodling comme échantillonnage peu contraint, PDF p. 1"
  - "ERC Grant, objet comme solution rare, harmonisations légales et exploration combinatoire, PDF p. 4-6"
  - "NetNeg, prédictions du réseau négociées avec les contraintes de contrepoint, PDF p. 3-6"
  - "NetNeg développe, architecture et comparaison des modules, PDF p. 9-18"
  - "Markov Constraints, PDF p. 1-8 et 21-23 : inversion de generate-and-test, recherche globale de séquences à faible probabilité et contrôle arbitraire."
  - "Markov Constraints for Lyrics, PDF p. 1-5 : comparaison empirique entre Markov pur, contraintes pures et processus markovien contraint."
  - "Assisted Lead Sheet Composition, PDF p. 1-8 et 13-15 : échantillonnage de chaînes markoviennes sous contraintes métriques, harmoniques et utilisateur dans un outil de composition."
  - "Bebop Virtuosity Explained, PDF p. 13-14 et 25-33 : texture markovienne, transformations, contraintes globales et partition intentionnelle au niveau du temps musical."
tags:
  - interessant
  - sampling
  - contraintes
  - resolution_de_problemes
  - generation
---
## Idée

Produire un objet intéressant demande souvent deux opérations hétérogènes. Le sampling
en marche avant ouvre des possibles en prolongeant localement un matériau, sans exiger
qu'un but complet soit connu. La résolution de contraintes traite au contraire chaque
choix comme une étape d'un problème global : elle vérifie les continuations, revient en
arrière, répare ou sélectionne les chemins encore compatibles avec une forme à
atteindre.

Chacune échoue seule d'une manière caractéristique. Le sampling pur peut produire une
suite d'événements localement plausibles mais incapable d'aboutir à une fin, un mètre ou
une organisation globale. Le solveur pur peut énumérer toutes les solutions légales sans
savoir lesquelles sont singulières ou intéressantes. La génération de l'intéressant
exige alors leur articulation : proposer du matériau, faire apparaître ou imposer un
problème, tester les contraintes, puis relancer la génération depuis ce que la
résolution a rendu possible.

Cette articulation n'impose pas toujours un plan antérieur à la production. Dans le
doodling, le sampling peut faire apparaître après coup la forme ou le problème qui
orientera les étapes suivantes. Ailleurs, une contrainte explicite précède le premier
geste. L'hypothèse porte sur la coopération des deux régimes, pas sur leur ordre fixe ni
sur tous les cas possibles de l'intéressant.

NetNeg fournit un précédent scientifique concret : chaque réseau neuronal émet une
distribution de prochains sons et les agents cherchent ensuite une paire qui maximise
les préférences apprises tout en respectant les contraintes du contrepoint. Le résultat
retenu est réinjecté comme nouveau contexte. Le système ne démontre pas une théorie
générale de l'intéressant, mais il réalise déjà la boucle proposition, négociation,
contrainte et relance décrite ici.

Les travaux ultérieurs sur les contraintes de Markov rendent ce couplage systématique.
Ils inversent le generate-and-test : l'espace des contraintes est exploré globalement,
tandis que la probabilité stylistique ordonne ou échantillonne les solutions. Les
expériences sur les paroles puis FlowComposer montrent que le couplage vaut comme
architecture générale — style local plus forme globale — sans que sa réussite technique
garantisse à elle seule l'intérêt du résultat.

Le chapitre sur la virtuosité bebop donne à cette architecture une interprétation
musicale plus fine. Le processus markovien y produit une texture locale plutôt que des
idées ; les décisions de haut niveau forment une « partition intentionnelle » qui
pilote contour, chromatisme, continuité et ruptures. Ce cas montre comment le sampling
et les contraintes peuvent aussi distribuer l'intention entre plusieurs échelles.

## L'intéressant comme critère de conditionnement ?

Lorsque l'intérêt d'un objet tient au problème qu'il fait émerger, à la rareté de sa
solution et à la difficulté perceptible de son élaboration, un critère fixé sur ses
seules propriétés finales ne suffit pas à en rendre compte. La carte `idea_0085`
situe une part de l'invention dans l'apparition du problème ; `idea_0096` précise que
la rareté pertinente est relative à ce problème, et non à la seule probabilité de
l'objet sous un modèle. Cette reconstruction doit rester contestable : choisir des
contraintes sur mesure pour rendre un objet unique ne suffit pas à établir son intérêt.

Le parcours peut aussi modifier les critères du créateur (`idea_0099`). Les essais
font apparaître des contraintes, des possibilités et des raisons de préférer une
solution qui n'étaient pas disponibles au départ. L'hypothèse à explorer est donc
celle d'une génération où problème, solution et critères d'appréciation se déterminent
progressivement. Le couplage entre sampling et contraintes prédéfinies fournit un
premier dispositif ; l'invention et la révision de ces contraintes en constituent un
prolongement, développé dans `idea_0158`.

La difficultuosité (`idea_0010`) oblige ici à distinguer trois dimensions :

- la **genèse effective**, faite des essais, bifurcations et choix de production ;
- la **genèse perçue**, c'est-à-dire la démarche et la difficulté que le sujet attribue
  à cette production ;
- le **problème reconstruit**, soit les contraintes que le sujet découvre dans sa
  rencontre avec l'objet, sans nécessairement retrouver celles du créateur.

Ces dimensions peuvent diverger. Une production laborieuse ne garantit pas l'intérêt ;
une apparence de difficulté ne prouve pas la genèse qu'elle suggère. La carte
`idea_0087` maintient ouverte la question des traces perceptibles de la facture, tandis
que `idea_0068` propose de documenter le parcours effectif. Un objet peut ainsi engager
une reconstruction intéressante sans que son histoire réelle soit connue.

Cette proposition ne démontre pas l'impossibilité de guider un modèle par un score
d'intérêt. Elle en limite la portée : optimiser un indicateur fixé sur les sorties ne
garantit pas de préserver la relation entre forme, genèse, problème et sujet. La
critique relève de `idea_0128`, sur la substitution de l'indicateur à la cible. Elle
reste distincte de la difficulté technique étudiée dans `idea_0017`, qui concerne
l'échantillonnage fidèle d'une loi conditionnelle déjà définie.

## Des contraintes de production à leur reconstruction

Produire une séquence sous contraintes ne garantit pas que ces contraintes soient
perceptibles ou reconstructibles pour celui qui la reçoit. La séquence peut satisfaire
un problème très sélectif et ne fournir à l'auditeur aucune prise pour le découvrir.
À l'inverse, celui-ci peut construire un problème pertinent que le système ou le
compositeur n'avait pas formulé (`idea_0085`).

Le schéma `P → x → P̂` distingue le problème de production de celui que reconstruit
le sujet. Il convient lorsque `P` guide effectivement la production ; la boucle
d'essais et de révisions décrite plus haut couvre les cas où problème et forme se
déterminent ensemble. L'écart entre `P` et `P̂` n'est donc pas automatiquement une
erreur : retrouver l'intention et produire une interprétation féconde sont deux
tâches différentes.

Le sampling et la résolution désignent ici des régimes de génération qui peuvent
coopérer : on peut échantillonner parmi des solutions admissibles. Leur comparaison
technique doit rester distincte de l'évaluation de la réception. Le pont avec la
thèse consiste à construire des objets dont on contrôle certaines contraintes,
puis à examiner ce que des sujets y découvrent.

## Statut de la source

La distinction entre construction et réception, ainsi que les critères expérimentaux
ajoutés le 29 septembre 2026, sont des propositions pour la thèse ; les publications
citées n'établissent pas leur validité psychologique.

Cette carte est une synthèse pour la thèse, non une conclusion explicite de `Hidden
Biases`. Ce papier établit la tension computationnelle entre sampling autoregressif
local et contraintes globales. Les notes sur le doodling et le grant ERC fournissent le
lien proprement dit avec la production de formes intéressantes. NetNeg constitue une
construction scientifique antécédente que la thèse peut réinterpréter, sans lui
attribuer cette généralisation philosophique.

La section sur le critère de conditionnement explicite la discussion avec l'auteur du
28 septembre 2026 à partir des cartes existantes. Elle formule une hypothèse
d'articulation pour la thèse, sans l'attribuer aux résultats techniques cités.

## Intérêt pour la thèse

La proposition donne un mécanisme commun à l'exploration sans but, au sens de la
direction et à l'objet perçu comme solution rare. Elle suggère aussi une architecture
expérimentale : comparer sampling seul, résolution seule et boucle hybride, puis mesurer
la diversité, la légalité et l'intérêt des objets obtenus.

Pour éprouver le prolongement proposé ici, distinguer une boucle à contraintes fixes
d'une boucle qui permet leur révision, et conserver la trace des changements de
problème et de critères. L'évaluation doit confronter ce parcours aux reconstructions
des sujets, sans déduire l'intérêt de la seule difficulté ou de la réussite du calcul.

Pour étudier la réception, distinguer trois observations : la sélectivité du problème
de production, la reconstructibilité pour des sujets d'expertises différentes et
l'intérêt effectivement éprouvé au cours de l'exploration. La faible probabilité sous
le modèle est une mesure supplémentaire, distincte du nombre de solutions.
Recueillir les premières réactions avant de demander une analyse permet de ne pas
confondre intérêt spontané et construction suscitée par la consigne. Confronter ensuite
les problèmes proposés par les sujets à des variantes contrôlées (`idea_0096`,
`idea_0113`), en autorisant plusieurs reconstructions et en documentant l'effet des
indices fournis. Une divergence entre réussite technique, reconstruction féconde et
intérêt constitue un résultat à expliquer, pas une anomalie à éliminer.

## Liens

- Articule l'échantillonnage de `idea_0012` avec la résolution implicite de `idea_0096`.
- `idea_0085` soutient l'émergence du problème pendant la génération.
- `idea_0099` précise que le parcours transforme aussi les critères de choix.
- `idea_0010` et `idea_0087` distinguent difficulté effective et difficulté perceptible.
- `idea_0068` propose de documenter la genèse effective sans la confondre avec sa reconstruction.
- `idea_0128` limite la portée du couplage technique : sa réussite ne garantit pas de préserver l'intéressant.
- `idea_0158` prolonge la boucle par l'invention et la révision des représentations et des contraintes.
- `idea_0017` distingue la satisfaction des contraintes de la fidélité à la loi conditionnelle visée.
- `idea_0098` montre l'échec symétrique d'un solveur qui ne produit que des solutions légales.
- `idea_0100` précise quand le couplage modèle-contrainte peut être calculé exactement.
