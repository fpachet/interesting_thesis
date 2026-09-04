# Revue systématique des publications de François Pachet

Source du corpus : [page personnelle des publications](https://www.francoispachet.fr/publications/)

## État au 8 août 2026

La page fournit 336 notices ou versions. Le périmètre scientifique retenu comprend
302 notices (chapitres, articles, conférences, arXiv, autres actes, inédits, thèses et
rapports techniques). Parmi elles, 247 versions disposent d'un PDF direct. Après
téléchargement, validation et dédoublonnage, le corpus directement lisible comprend
243 PDF scientifiques uniques, soit 3 228 pages. Les 243 textes ont été extraits sans
échec.

Deux ensembles restent distincts :

- les 243 PDF directs, qui reçoivent une lecture et une décision de pertinence ;
- les notices sans PDF direct, conservées dans l'inventaire jusqu'à résolution de la
  page d'éditeur, du dépôt ou de l'absence de fichier.

Le fichier `publications-francois-pachet-inventaire.tsv` conserve toutes les notices et
leurs liens. `publications-francois-pachet-triage.tsv` fournit l'ordre de lecture des
PDF directs. Le triage lexical n'est jamais utilisé comme décision automatique.

## Protocole de décision

Chaque publication passe par les mêmes questions :

1. Quel résultat ou argument le texte établit-il effectivement ?
2. Porte-t-il sur l'attention, l'ennui, les attentes, la surprise, la relation
   sujet-forme, la création, l'exploration ou les conditions d'une prise ?
3. Apporte-t-il une proposition indépendante, renforce-t-il une carte existante ou
   fournit-il seulement un contexte historique/technique ?
4. Quelle inférence philosophique est légitime, et laquelle serait une projection
   rétrospective abusive ?
5. Faut-il créer une carte, renforcer une carte ou ne rien intégrer ?

Les décisions possibles sont `fort`, `moyen`, `contexte` et `non pertinent`. Un texte
`fort` peut produire une articulation nouvelle ; un texte `moyen` renforce une carte
existante ; `contexte` signifie qu'il éclaire la trajectoire sans étayer directement la
thèse ; `non pertinent` signifie qu'aucun usage précis n'est identifié. Les textes
pertinents cités reçoivent le mot-clé bibliographique `francois-pachet`.

## Décisions validées dans la première grappe

| Publication | Décision | Apport précis | Intégration |
|---|---|---|---|
| Pachet, *Qu'est-ce qu'une mélodie intéressante ?* (2000), 9 p. | **fort** | Compare patterns, solutions combinatoires et propriétés globales, mais montre aussi leurs insuffisances et exclut méthodologiquement l'auditeur. Le passage au modèle relationnel actuel devient une correction explicite du programme ancien. | Nouvelle `idea_0146` ; `idea_0096` et `idea_0098` renforcées ; clé `pachet2000melodie`. |
| Pachet, *Surprising Harmonies* (1999), 20 p. | **fort** | Une surprise féconde dépend d'attentes acquises et peut être comprise par règles de substitution : elle est reconstructible ou « prouvable », pas seulement improbable ou inouïe. | `idea_0019` renforcée ; clé `pachet1999surprising`. |
| Pachet, *Active Listening: What Is in the Air?* (1999), 16 p. | **moyen à fort** | L'intéressant se déplace de l'item vers le parcours ; les contrôles utiles préservent des invariants sémantiques et les programmes musicaux ont des propriétés globales irréductibles aux titres. | `idea_0014`, `idea_0102`, `idea_0105` renforcées ; clé `pachet1999active`. |
| Pachet, *On the Design of Flow Machines* (2004), 22 p. | **fort** | Le Continuator documente l'attention soutenue, le rapport ennui/anxiété, le miroir dynamique et une séquence scepticisme → surprise/Aha → excitation → concentration/analyse. Le papier ne définit cependant pas l'intéressant en général. | `idea_0006`, `idea_0121`, `idea_0137` renforcées ; clé `pachet2004flowmachines`. |
| Pachet, *Les nouveaux enjeux de la réification* (2004), 29 p. | **fort, méthodologique** | Les modèles ne prennent sens que dans des usages situés ; les « exemples nourriciers » font résister le réel et permettent d'abstraire sans universalisation prématurée. C'est une méthode interne pour relire la trajectoire scientifique. | `idea_0110` renforcée ; clé `pachet2004reification`. |
| Montecchio, Roy et Pachet, *The Skipping Behavior…* (2020), 16 p. | **fort, déjà traité** | Les profils temporels de skip sont stables et liés à la structure musicale, mais ne mesurent pas directement l'ennui. | `idea_0011`, `idea_0145` ; clé `montecchio2020skipping`. |

## Décisions validées dans la deuxième grappe

| Publication | Décision | Apport précis | Intégration |
|---|---|---|---|
| Pachet, *Creativity Studies and Musical Interaction* (2006), 10 p. | **fort** | Définit la créativité depuis le sentiment personnel de produire quelque chose de nouveau et d'intéressant dans un contexte situé. L'unité de recherche devient le couple humain--machine, évalué par sa production et par son effet sur le sujet relativement à une condition sans système. | Nouvelle `idea_0147` ; `idea_0006` et `idea_0125` articulées ; clé `pachet2006creativity`. |
| Pachet, *Enhancing Individual Creativity with Interactive Musical Reflective Systems* (2006), 15 p. | **fort** | Le miroir doit être reconnaissable sans être répétitif ; l'apprentissage incrémental échafaude la complexité, soutient l'intérêt et déplace l'attention du produit vers la découverte du sujet par lui-même. | `idea_0006`, `idea_0007`, `idea_0137` et `idea_0147` ; clé `pachet2006reflective`. |
| Pachet, *Interacting with a Musical Learning System: The Continuator* (2002), 8 p. | **moyen à fort** | Décrit l'effet Aha lorsque les musiciens reconnaissent soudain leur propre style, ainsi que le contrôle intime permettant de conserver ou quitter une région musicale jugée intéressante. | `idea_0006` et `idea_0137` ; clé `pachet2002continuatorinteraction`. |
| Martín, Pachet et Frantz, *The Creative Process in Lead Sheet Composition* (2016), 23 p. | **fort** | Sépare auto-évaluation et consensus, montre l'amélioration sélective produite par le feedback et observe que les juges préfèrent les compositions issues d'un niveau d'expérience voisin du leur. | Nouvelle `idea_0148` ; `idea_0046` et `idea_0084` renforcées ; clé `martin2016creativeprocess`. |
| Jones et al., *Stimulating Creative Flow through Computational Feedback* (2009), 10 p. | **moyen à fort** | Situe le feedback utile entre imitation et étrangeté, relie flow et incertitude sur ce qui doit venir, et décrit les « bonnes erreurs » comme ouvertures d'un terrain créatif imprévu. | `idea_0006` et `idea_0121` ; clé `jones2009stimulating`. |

## Décisions validées dans la troisième grappe

| Publication | Décision | Apport précis | Intégration |
|---|---|---|---|
| Addessi et Pachet, *Experiments with a Musical Machine* (2005), 26 p. | **fort** | Les états de l'engagement ne suivent pas nécessairement un ordre linéaire. Des temps morts peuvent réajuster la relation ; la disparition du miroir provoque une perte d'intérêt, tandis qu'une erreur encore appropriable peut devenir matériau musical. L'étude repose sur 27 enfants, neuf protocoles complets et deux études de cas détaillées : elle fournit des mécanismes, non une preuve causale générale. | Nouvelle `idea_0149` ; `idea_0006`, `idea_0011`, `idea_0137` et `idea_0147` renforcées ; clé `addessi2005experiments`. |
| Pachet et Addessi, *When Children Reflect on Their Playing Style* (2004), 19 p. | **moyen à fort** | Précurseur moins contrôlé de l'étude de 2005 : attention prolongée, apprentissage implicite du tour de rôle, interprétation par le flow et déplacement de l'attention du produit vers le sujet. | `idea_0006`, `idea_0121`, `idea_0147` ; clé `pachet2004childrenreflect`. |
| Pachet, *Beyond the Cybernetic Jam Fantasy* (2004), 5 p. | **fort conceptuel** | Formule explicitement le changement de critère : l'objectif d'un système interactif apprenant n'est pas seulement un matériau cohérent, mais la production d'interactions intéressantes. | `idea_0006`, `idea_0147` ; clé `pachet2004cybernetic`. |
| Pachet, *Interactions réflexives : du « C'est marrant » aux machines à Flow* (2006), 12 p. | **fort conceptuel** | Pose directement la question du système intéressant ou addictif et soutient que, dans une activité autotélique, la qualité de l'interaction peut compter davantage que son produit. | `idea_0006`, `idea_0147` ; clé `pachet2006interactionsreflexives`. |
| Addessi et al., *Young Children's Musical Experiences with a Flow Machine* (2006), 8 p. | **moyen méthodologique** | Construit une grille de neuf variables, obtient 80,55 % d'accord moyen entre observateurs et code davantage de flow avec le système (54 %) que sans lui (42 %) sur neuf enfants. La petite taille et l'inférence des états affectifs depuis les conduites limitent la portée. | `idea_0011`, `idea_0121`, `idea_0149` ; clé `addessi2006flowmachine`. |
| Addessi, Ferrari et Pachet, *Touched by Musical Discovery* / *Without Touch, Without Seeing* (2006), deux PDF de 12 p. | **contexte redondant** | Les deux fichiers sont des versions éditoriales substantiellement identiques d'une pratique en classe avec 18 enfants. Ils confirment autonomie, règles implicites, exploration et attention conjointe, sans proposition distincte de la grappe. | Aucun nouvel identifiant ni nouvelle entrée bibliographique. |

Cette grappe impose une correction méthodologique importante : une interruption locale
ne signifie pas nécessairement une perte d'intérêt. Comme pour le skipping, il faut
reconstruire ce qui se passe avant et après la coupure. Un temps mort peut annoncer
l'abandon, mais aussi permettre un réajustement ou la reprise créative d'une erreur.
Inversement, une longue durée d'attention reste insuffisante sans analyse des conduites
qui la composent.

## Décisions validées dans la quatrième grappe

| Publication | Décision | Apport précis | Intégration |
|---|---|---|---|
| Pachet et Roy, *Markov Constraints* (2011), 25 p. | **fort, scientifique** | Reformule la génération comme recherche globale : des contraintes utilisateur arbitraires deviennent compatibles avec un modèle stylistique, y compris pour atteindre des séquences de très faible probabilité qu'une marche gloutonne ne rencontrerait pratiquement pas. | `idea_0096`, `idea_0109` ; clé `pachet2011markov`. |
| Ghedini, Pachet et Roy, *Creating Music and Texts with Flow Machines* (2015), 21 p. | **fort, conceptuel** | Définit le style comme texture et la contrainte comme structure, mais précise que leur combinaison ne garantit pas la qualité intrinsèque : l'utilisateur explore jusqu'à trouver un objet intéressant. Le style est en outre pensé comme un développement diachronique, pas comme un artefact isolé. | `idea_0054`, `idea_0080`, `idea_0109` ; clé `ghedini2015flowmachines`. |
| Papadopoulos, Roy et Pachet, *Assisted Lead Sheet Composition using FlowComposer* (2016), 16 p. | **moyen à fort** | L'outil articule chaînes de Markov, mètre, harmonie et contraintes utilisateur. Il documente deux limites décisives : la génération autonome reste sans direction à longue portée ; une réharmonisation peut être nouvelle, valide et stylistiquement juste tout en étant moins intéressante que l'originale. | `idea_0016`, `idea_0098`, `idea_0109` ; clé `papadopoulos2016flowcomposer`. |
| Papadopoulos, Pachet et Roy, *Generating Non-Plagiaristic Markov Sequences* (2016), 19 p. | **fort, scientifique** | Une séquence statistiquement nouvelle peut contenir de longues copies ; l'ordre de Markov ne borne pas leur taille. Un automate de fragments interdits et la propagation de croyance fournissent une garantie de non-copie et un échantillonnage exact, sans pour autant garantir l'intérêt. | Nouvelle `idea_0150` ; `idea_0017`, `idea_0054`, `idea_0080` ; clé `papadopoulos2016nonplagiaristic`. |
| Papadopoulos, Roy et Pachet, *Avoiding Plagiarism in Markov Sequence Generation* (2014), 7 p. | **moyen, précurseur** | Première formulation de la contrainte `MAXORDER` et démonstration empirique de l'écart entre ordre d'apprentissage et longueur recopiée. Le chapitre de 2016 complète ce résultat par l'échantillonnage probabiliste exact. | `idea_0150` ; clé `papadopoulos2014avoiding`. |
| Pachet, Papadopoulos et Roy, *Sampling Variations of Sequences for Structured Music Generation* (2017), 7 p. | **fort** | Les répétitions et variations contrôlées rendent une pièce longue cohérente et lui donnent l'impression d'une intention. La structure reste cependant empruntée à une œuvre cible : le papier qualifie lui-même cette stratégie de *templagiarism*. | `idea_0016`, `idea_0080` ; clé `pachet2017variations`. |
| Barbieri et al., *Markov Constraints for Generating Lyrics with Style* (2012), 6 p. | **moyen à fort** | La comparaison entre Markov pur, contraintes pures et modèle hybride confirme l'intérêt du couplage style local--forme globale. La réécriture de *Yesterday* dans le style de Dylan demeure semi-automatique : l'humain choisit une proposition parmi cinq à chaque vers. | `idea_0080`, `idea_0109` ; clé `barbieri2012lyrics`. |

Cette grappe produit une ligne argumentative continue mais non une doctrine unique.
Une probabilité stylistique ne donne ni direction, ni non-plagiat, ni intérêt. Les
contraintes peuvent garantir une forme, une métrique ou l'absence de fragments copiés,
mais chaque garantie reste locale à la cible qu'elle formalise. Le cas Flow Machines
confirme donc à la fois la puissance de la formalisation et le risque de substitution de
cible : rendre une propriété calculable permet de la contrôler, sans autoriser à
substituer son indicateur ou sa procédure effective au jugement relationnel
d'intéressant.

## Décision validée dans la cinquième grappe

| Publication | Décision | Apport précis | Intégration |
|---|---|---|---|
| Pachet et Roy, *Automatic Generation of Music Programs* (1999), 15 p. | **fort, généalogique et formel** | Formule le choix musical comme compromis entre deux désirs contradictoires, répétition et surprise. RecitalComposer porte le problème à l'échelle d'une séquence : similarité pour la continuité locale, différence et cardinalité pour la variété globale. Un titre peut ainsi devenir approprié par sa position dans le parcours plutôt que par sa seule valeur isolée. | Nouvelle `idea_0151` ; `idea_0014` et `idea_0103` renforcées ; clé `pachet1999programs`. |

Cette lecture confirme l'intuition proposée par François Pachet, sous une réserve de
vocabulaire. Le papier formalise littéralement la continuité et la variété, non une
contrainte de rupture. La thèse peut interpréter la variété comme possibilité de rompre
une continuité devenue prévisible, à condition de signaler cette extension. Elle ajoute
aussi le sujet et son histoire : la même séquence contrainte peut être trop familière
pour l'un et trop discontinue pour l'autre.

À la demande de l'auteur, cette grappe a été resserrée sur ce seul texte. Les articles
sur le Sony Music Browser, le Cuidado Music Browser et les playlists n'ont pas été lus
dans cette passe et ne reçoivent donc aucune décision de pertinence par simple analogie
de titre.

## Décisions validées dans la sixième grappe

| Publication | Décision | Apport précis | Intégration |
|---|---|---|---|
| Pachet, *Des machines à sortir de soi* (2008), 15 p. | **fort, réflexif** | Les objets intéressants émergent comme effets secondaires d'une interaction avec une image imparfaite et révisable du sujet. Les sessions lentes du Continuator produisent rétrospectivement des pièces jugées plus intéressantes sans maximiser l'imitation immédiate. | `idea_0006`, `idea_0007`, `idea_0147` ; clé canonique `pachet2008machines`. |
| Pachet, *The Future of Content Is in Ourselves* (2008 et 2010), deux PDF de 20 p. | **contexte redondant** | Les versions anglaises développent le même argument et les mêmes cas que le chapitre français, avec des variations éditoriales mineures. Elles confirment la distinction entre réflexivité, imitation et intérêt sans proposition indépendante. | Aucun nouvel identifiant ni doublon bibliographique ; rattachement à `pachet2008machines`. |
| Pachet et Roy, *Hit Song Science Is Not Yet a Science* (2008), 6 p. | **fort, résultat négatif** | Sur 32 978 titres, 98 traits génériques, 98 traits spécifiques et 629 étiquettes humaines ne prédisent pas trois classes de popularité au-delà du hasard, alors que d'autres catégories subjectives sont apprenables. L'échec est donc propre à la cible, sans prouver l'impossibilité de toute prédiction. | `idea_0013`, `idea_0069` ; clé `pachetroy2008hitsong`. |
| Pachet, *Hit Song Science* (2011), 22 p. | **fort, synthèse relationnelle** | L'exposition répétée, l'influence sociale cumulative et la boucle diffuseur-public rendent la popularité dynamique et contaminent le *ground truth*. Le chapitre rapporte aussi l'expérience de Draganoiu et al. sur la préférence des femelles canaris pour des trilles artificiellement au-delà des limites ordinaires de production. | `idea_0013`, `idea_0053`, `idea_0070`, `idea_0078` ; clé `pachet2011hitsong`. |
| Aucouturier et Pachet, *Music Similarity Measures: What's the Use?* (2002), 7 p. | **fort, généalogique et conceptuel** | Une mesure de timbre peut être valide tout en produisant des rapprochements triviaux. L'effet Aha est recherché dans la contradiction entre similarité timbrale et attente textuelle. L'étude exploratoire à dix utilisateurs et les paramètres manuels limitent la portée empirique. | Nouvelle `idea_0152` ; `idea_0128`, `idea_0151`, `idea_0106` ; clé `aucouturier2002similarity`. |
| Lerch et al., *Closed-loop Bird--Computer Interactions* (2011), 11 p. | **moyen à fort, méthodologique** | Des femelles canaris vocalisent davantage dans une interaction contingente que pendant le playback des mêmes appels (8,9 contre 3,13 vocalisations/minute, $n=7$, $p=0{,}016$). Le résultat porte sur la contingence sociale et non sur la virtuosité du chant. | `idea_0011`, `idea_0070` ; clé `lerch2011closedloop`. |

Cette grappe précise trois corrections utiles. Une métrique valide peut manquer
l'intéressant tout en devenant féconde lorsqu'elle est confrontée à une autre attente.
Une cible comme la popularité n'est pas seulement bruyante : elle est partiellement
produite par l'histoire de l'exposition et de la diffusion. Enfin, les deux dossiers
animaux doivent rester distincts. La préférence pour des trilles artificiellement
difficiles étaye le versant virtuosité ; le protocole en boucle fermée établit que la
contingence de la relation modifie la conduite vocale.

## Décisions validées dans la septième et dernière grappe

| Publication | Décision | Apport précis | Intégration |
|---|---|---|---|
| Pachet, *Musical Virtuosity and Creativity* (PDF de travail titré *Bebop Virtuosity Explained*, 2012), 34 p. | **fort, généalogique et constructif** | Distingue une texture markovienne, qui produit le flux local, d'une « partition intentionnelle » portant les décisions au niveau du temps musical. L'ennui markovien apparaît lorsque les règles deviennent prévisibles sans espoir d'un événement saillant. Le modèle construit une architecture plausible de la virtuosité, sans constituer une preuve cognitive générale. | Nouvelle `idea_0154` ; `idea_0010`, `idea_0078`, `idea_0109` et `idea_0122` renforcées ; clé `pachet2012virtuosity`. |
| Mili et Pachet, *Regularity, Document Generation, and Cyc* (1995), PDF de 33 p. | **fort, généalogique et formel** | Distingue régularité parfaite et peu informative, irrégularité arbitraire sans prise, et irrégularité structurée par des règles, seule féconde pour la textualisation d'une trace de preuve. L'écart peut révéler une propriété du monde ou un concept manquant dans la base. | Nouvelle `idea_0153` ; clés et cartes connexes rattachées à `milipachet1995regularity`. |
| Pachet, *Exploiting Regularity in Cyc for Text Generation* (version courte), 11 p. | **contexte redondant, formulation concentrée** | Reformule la même hypothèse et son usage opérationnel local. La version longue sert de référence canonique. | Source secondaire de `idea_0153`, sans doublon bibliographique. |

Cette grappe rend visibles deux antécédents personnels particulièrement proches de la
thèse actuelle. Leur reprise reste contrôlée : la régularité de Cyc est un critère
local de génération documentaire, et Virtuoso un modèle computationnel soutenu par une
évaluation experte partiellement subjective. La thèse peut reconstruire leur parenté
avec l'intéressant, mais non leur attribuer rétroactivement sa théorie générale.

## Premier résultat transversal

La première grappe fait apparaître une généalogie interne plus précise que prévu. Les
travaux passés occupent plusieurs positions complémentaires : propriétés de la forme
(*mélodie intéressante*), attentes apprises (*Surprising Harmonies*), parcours et
contrôle de l'auditeur (*Active Listening*), boucle sujet-système (*Flow Machines*) et
conduite effectivement observée (*skipping*). Aucun texte ne suffit seul ; leur
distribution motive justement le passage à `I(F, S | H, t)`.

L'article sur la réification ajoute une règle de méthode : la thèse ne doit pas extraire
des slogans de toute la bibliographie personnelle. Elle doit identifier des exemples
nourriciers, vérifier ce qu'ils font réellement résister et limiter la généralisation à
ce que leurs usages permettent.

La deuxième grappe donne en outre un précédent explicite au choix relationnel : en
2006, le couple sujet--système était déjà proposé comme unité d'analyse et le « nouveau
et intéressant » comme expérience située. Elle montre aussi pourquoi le paramètre
d'horizon ne peut pas être éliminé par une moyenne : dans l'expérience sur les lead
sheets, les préférences croisent le niveau d'expérience des producteurs et des juges.

## Addendum du 23 août 2026

Deux prépublications postérieures à la campagne ont été traitées à la demande de
l'auteur, sans rouvrir le tri général des 208 PDF restants.

| Publication | Décision | Apport précis | Intégration |
|---|---|---|---|
| Pachet et Roy, *Hidden Biases in Conditioning Autoregressive Models* (2026), version longue de 16 p. soumise à NeurIPS | **fort, scientifique** | Distingue la distribution conditionnelle exacte de la loi produite par une procédure tractable ; établit des résultats de difficulté et documente distorsion des poids et perte de support. | `idea_0016`, `idea_0017`, `idea_0100`, `idea_0109`, `idea_0128`, `idea_0158` ; clé `pachet2026biases`. |
| Pachet, *Tonal Parsimony in Chord-Sequence Analysis* (2026) | **fort, articulation** | Ordonne continuité locale et compacité globale ; les cas d'anti-compression distinguent prise explicative, compression statique et progrès temporel d'un observateur. | `idea_0071`, `idea_0086`, `idea_0128`, `idea_0151`, nouvelle `idea_0159` ; clé `pachet2026tonalparsimony`. |

## Clôture de la campagne

Trente-cinq PDF ont reçu une décision argumentée. Les 208 PDF restants n'ont pas reçu
de décision individuelle de pertinence. À la demande de l'auteur, la revue systématique
est arrêtée après le traitement des deux priorités finales ci-dessus ; les autres
candidats précédemment envisagés sont abandonnés et ne sont plus programmés.

Le statut `à examiner` doit donc être compris comme « non décidé si la campagne était
rouverte », et non comme `non pertinent`. Aucun rejet scientifique n'est inféré d'un
titre, d'un score lexical ou de cette décision d'arrêt.
