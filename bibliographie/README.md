# Bibliographie

- `kant1848moralepratique` — Immanuel Kant, *Fondements de la métaphysique des
  mœurs et Critique de la raison pratique*, trad. Jules Barni (Ladrange, 1848) ;
  édition ancienne vérifiée pour le problème de l'intérêt moral, avec contrôle du
  texte allemand en Ak. 5:79-80.
- `jps1985tanakh` — *Tanakh: The Holy Scriptures* (Jewish Publication Society,
  1985) ; Job 1,8-9, 13,3, 23,3-5, 40,4-5 et 42,1-6 contrôlés pour distinguer
  motivation morale, intérescence interne du personnage et intérescence externe
  du lecteur.
- `girard1961mensonge` — René Girard, *Mensonge romantique et vérité romanesque*
  (Grasset, 1961) ; notice d'éditeur vérifiée, ouvrage à relire intégralement avant
  toute attribution doctrinale détaillée.

`references.bib` est la source canonique des références bibliographiques de la
thèse. Les chemins locaux restent dans les cartes pour garantir la traçabilité ;
le champ YAML optionnel `references` relie une proposition aux clés BibTeX.

Le programme de lecture consacré à l'histoire et aux théories de l'intéressant
est maintenu dans
[`docs/lectures/interessant-etat-art.md`](../docs/lectures/interessant-etat-art.md).
Il distingue les références déjà entrées dans BibTeX, les textes encore à lire et
les sources historiques dont l'édition précise doit être établie avant
intégration.

## Règles de maintenance

1. Ajouter une entrée BibTeX lorsqu'une source devient effectivement utile à une
   carte ou au manuscrit, pas pour chaque titre mentionné dans une bibliographie.
2. Utiliser une clé stable de la forme `auteurAnneeMot`, sans la renommer ensuite.
3. Vérifier le titre, les auteurs, l'année et le support sur la source primaire ou
   la page de l'éditeur.
4. Conserver dans `file` le chemin relatif du document local lorsqu'il existe.
5. Employer `@unpublished` ou `@techreport` quand le statut éditorial n'est pas
   établi ; ne pas déduire une publication de la seule présence d'un PDF.
6. Ajouter la clé dans `references` sur chaque carte qui mobilise directement la
   publication.

Les documents personnels, grants, notes, courriels et archives restent inventoriés
dans `cartes/REGISTRE_TRAITEMENT.md`. Ils ne deviennent des entrées bibliographiques
que s'ils doivent être cités dans le manuscrit.

## Travaux de François Pachet

Les publications dont François Pachet est auteur ou coauteur portent le mot-clé
BibLaTeX `francois-pachet`. Le projet de thèse et le catalogue des cartes utilisent ce
marquage pour produire une section bibliographique distincte, sans dupliquer les
références dans la bibliographie générale.

La section comprend actuellement :

- `milipachet1995regularity` ;
- `pachet1997representation` ;
- `pachet1999active`, `pachet1999programs`, `pachet1999surprising` et
  `pachet2000melodie` ;
- `aucouturier2002similarity`, `pachet2002continuatorinteraction`, `pachet2004flowmachines`,
  `pachet2004cybernetic`, `pachet2004childrenreflect`, `pachet2004reification`,
  `addessi2005experiments`, `pachet2006clefs`, `pachet2006creativity`,
  `pachet2006reflective`, `pachet2006interactionsreflexives`,
  `addessi2006flowmachine`, `pachet2008machines`, `pachetroy2008hitsong`,
  `jones2009stimulating`, `pachet2011hitsong`, `lerch2011closedloop`,
  `pachet2011markov`, `barbieri2012lyrics` et `pachet2012virtuosity` ;
- `papadopoulos2014avoiding`, `ghedini2015flowmachines`,
  `papadopoulos2016nonplagiaristic`, `papadopoulos2016flowcomposer`,
  `martin2016creativeprocess` et `pachet2017variations` ;
- `pachet2018oreille` et `montecchio2020skipping` ;
- `pachet2021assisted` ;
- `pachet2026biases`, `pachet2026generation`, `pachet2026impossibilite` et
  `pachet2026markov` ;
- `pachet2027virtuosite`.

Toute nouvelle publication personnelle citée doit recevoir ce mot-clé. Les œuvres de
Pierre Pachet restent classées avec les autres références.

## Projet de thèse V2

La réécriture bilingue du projet de thèse utilise directement ce fichier avec
BibLaTeX. Les références philosophiques seulement esquissées dans la V1 ont été
complétées à partir de la bibliographie détaillée du PDF anglais. Les entrées de
Petitot, Berlyne, Schmidhuber, Kaplan, Oudeyer, Abdallah et Plumbley ont été contrôlées sur les
pages d'éditeur, dépôts institutionnels ou notices primaires disponibles.

Les deux fichiers `projet-these/projet-these-fr.tex` et
`projet-these/projet-these-en.tex` doivent employer les mêmes clés. Chaque version
stabilisée archive une copie de ce fichier dans `projet-these/versions/` afin que
son rendu bibliographique reste reproductible.

## Correspondance initiale

| Clé | Source locale principale | Statut |
| --- | --- | --- |
| `schmidhuber1997interesting` | `input/old_docs/interestingness.pdf` | rapport technique publié |
| `schmidhuber2009compression` | pas encore dans le corpus | chapitre de synthèse sur le progrès de compression |
| `vygotsky1978mind` | pas encore dans le corpus | recueil édité ; définition de la zone de développement proximal, p. 86-90 |
| `lenat2008turtle` | pas encore dans le corpus | article d'AI Magazine ; formule de l'apprentissage à la frange du savoir, p. 17-18 |
| `lenat1991thresholds` | pas encore dans le corpus | article de Lenat et Feigenbaum sur le principe de connaissance et l'hypothèse de largeur |
| `koestler1989act` | pas encore dans le corpus | réédition de `The Act of Creation` (1964) ; bisociation et filiation explicitement invoquée par Lenat pour l'apprentissage à la frange |
| `russell1995rationality` | `input/Russell_Rationality_and_Intelligence_IJCAI95.pdf` | article associé au Computers and Thought Award ; avertissement contre la mathématisation prématurée, p. 950 |
| `russell1995awardlecture` | transcription dans `input/Pachet_Representation_connaissances_langages_objets_1997.pdf` | allocution pour le Computers and Thought Award à IJCAI-95 ; source intellectuelle de la formulation orale sur les parties intéressantes définies hors du problème |
| `milipachet1995regularity` | `input/publications-francois-pachet/mili-95a-Regularity_Document_Generation_and_Cyc.pdf` | chapitre relu ; situe l'information utile entre régularité tautologique et irrégularité arbitraire, dans le cadre local de la textualisation des traces de preuve |
| `pachet1997representation` | `input/Pachet_Representation_connaissances_langages_objets_1997.pdf` | mémoire d'HDR ; conserve la formulation orale longue de Russell sur les parties intéressantes définies hors du problème, PDF p. 10 |
| `pachet1999surprising` | `input/publications-francois-pachet/pachet-99-Casys.pdf` | article relu ; distingue la surprise brute de la surprise compréhensible ou « prouvable » depuis des régularités et règles acquises |
| `pachet1999active` | `input/publications-francois-pachet/pachet-99a.pdf` | chapitre relu ; déplace l'accès musical de la sélection d'items vers des parcours et espaces d'exploration sémantiquement contraints |
| `pachet1999programs` | `input/publications-francois-pachet/pachet-99m.pdf` | article relu ; compromis entre répétition et surprise, continuité par similarité et variété par différence et cardinalité à l'échelle d'une séquence |
| `pachet2012virtuosity` | `input/publications-francois-pachet/pachet12b.pdf` | chapitre publié sous le titre *Musical Virtuosity and Creativity* ; le PDF de travail porte le titre interne *Bebop Virtuosity Explained* ; partition intentionnelle, texture markovienne, ennui et limites de la validation cognitive |
| `aucouturier2002similarity` | `input/publications-francois-pachet/pachet-02g.pdf` | article relu ; une mesure valide peut rester triviale et devenir intéressante par contradiction entre proximité timbrale et attente textuelle |
| `pachet2000melodie` | `input/publications-francois-pachet/pachet-06c.pdf` | article relu intégralement ; trois modèles objectifs de la mélodie intéressante et limite explicitement assumée de l'exclusion de l'auditeur |
| `pachet2004flowmachines` | `input/publications-francois-pachet/pachet-04-designflowmachines.pdf` | chapitre relu ; observations du cycle surprise--excitation--concentration, de l'attention et de la réflexivité dans le Continuator |
| `pachet2004cybernetic` | `input/publications-francois-pachet/pachet-03g.pdf` | article relu ; déplacement explicite du critère de conception, du matériau cohérent vers l'interaction intéressante |
| `pachet2004childrenreflect` | `input/publications-francois-pachet/pachet-04-When.pdf` | article relu ; attention, règles implicites, tour de rôle et découverte de soi dans les premières expériences avec les enfants |
| `pachet2004reification` | `input/publications-francois-pachet/pachet-04f.pdf` | article relu ; rôle des exemples nourriciers, de la résistance des terrains et du contexte d'usage dans la fécondité des modèles |
| `pachet2002continuatorinteraction` | `input/publications-francois-pachet/pachet-02-icmai-final.pdf` | article relu ; effet Aha, contrôle intime et conservation de régions musicales jugées intéressantes |
| `addessi2005experiments` | `input/publications-francois-pachet/pachet-04j.pdf` | article relu intégralement ; états non linéaires de l'engagement, temps morts de réajustement, règles implicites et réemploi créatif d'une erreur |
| `pachet2006creativity` | `input/publications-francois-pachet/Pachet-06-Creativity_Studies.pdf` | chapitre relu ; créativité comme sentiment situé de produire quelque chose de nouveau et d'intéressant, étudié dans le couple humain-machine |
| `pachet2006reflective` | `input/publications-francois-pachet/pachet-06-Enhancing_Individual_Creativity.pdf` | chapitre relu ; systèmes réflexifs, échafaudage de complexité et déplacement de l'attention du produit vers le sujet |
| `pachet2006interactionsreflexives` | `input/publications-francois-pachet/pachet-06a.pdf` | communication relue ; système « marrant », activité autotélique et primat de la qualité de l'interaction sur son produit |
| `addessi2006flowmachine` | `input/publications-francois-pachet/addessi-06c.pdf` | communication relue ; grille comportementale du flow sur neuf enfants et comparaison des tâches avec et sans Continuator |
| `jones2009stimulating` | `input/publications-francois-pachet/jones-09a.pdf` | rapport relu ; niveau optimal de distorsion, indétermination productive et feedback continu |
| `pachet2008machines` | `input/publications-francois-pachet/Pachet-08-Stiegler.pdf` | chapitre français relu ; création d'objets intéressants comme effet secondaire d'une interaction réflexive et distinction entre imitation immédiate et intérêt rétrospectif |
| `pachetroy2008hitsong` | `input/publications-francois-pachet/pachet-08c.pdf` | article relu ; échec de traits audio et humains à prédire la popularité au-delà du hasard, malgré l'apprentissage d'autres étiquettes subjectives |
| `pachet2011hitsong` | `input/publications-francois-pachet/pachet-11a.pdf` | chapitre relu ; cible popularité produite par l'exposition, l'influence sociale et la boucle diffuseur-auditeur ; discussion du cas de virtuosité des canaris |
| `lerch2011closedloop` | `input/publications-francois-pachet/lerch-10a.pdf` | article relu ; davantage de vocalisations de femelles canaris en interaction contingente qu'en playback, sur un petit échantillon comparatif |
| `pachet2026impossibilite` | `input/De l'impossibilité de créer.pdf` | manuscrit à paraître chez Matériologiques ; p. 50-53 du PDF, le cas des canaris relie préférence pour les chants impossibles, compétence vocale latente et hypothèse de résonance motrice ; cette dernière est une interprétation conceptuelle, non un résultat direct de l'expérience |
| `pachet2011markov` | `input/publications-francois-pachet/pachet-09c.pdf` | article relu ; génération markovienne pilotable, recherche globale et séquences à faible probabilité sous contraintes arbitraires |
| `barbieri2012lyrics` | `input/publications-francois-pachet/barbieri-12a.pdf` | article relu ; style local et contraintes globales de rime, mètre, syntaxe et sémantique dans la génération de paroles |
| `papadopoulos2014avoiding` | `input/publications-francois-pachet/papadopoulos-14a.pdf` | article relu ; l'ordre de Markov ne borne pas la longueur copiée et la contrainte MAXORDER garantit une limite explicite |
| `ghedini2015flowmachines` | `input/publications-francois-pachet/ghedini-15b.pdf` | chapitre relu ; style comme texture, contrainte comme structure et développement diachronique d'un style propre |
| `papadopoulos2016nonplagiaristic` | `input/publications-francois-pachet/max_order.pdf` | chapitre relu ; généralisation par fragments interdits et échantillonnage exact des séquences non plagiaires |
| `papadopoulos2016flowcomposer` | `input/publications-francois-pachet/roy-16b.pdf` | article relu ; composition assistée, contraintes métriques et harmoniques, et différence explicite entre sortie valide et sortie intéressante |
| `martin2016creativeprocess` | `input/publications-francois-pachet/martin-16a.pdf` | chapitre relu ; distinction jugement propre/consensus, effet sélectif du feedback et dépendance des préférences à l'expérience des juges |
| `pachet2017variations` | `input/publications-francois-pachet/pachet-17d.pdf` | article relu ; variations contrôlées et structure répétitive à longue portée, avec limite assumée du templagiarism |
| `bachimont1996hermeneutique` | `docs/Bachimont.pdf` | thèse d'épistémologie ; lecture ciblée des PDF p. 322-323 sur la reconstruction de la question, la fusion des horizons et l'innovation interprétative |
| `anselin2021attention` | `input/theses-comparaison/anselin-2021-accorder-son-attention.pdf` | thèse de philosophie ; lecture ciblée de l'introduction, des chapitres 1-3, des objections et de la conclusion comme étalon d'architecture argumentative |
| `thalabard2012attention` | `input/theses-comparaison/thalabard-2012-attention-et-conscience.pdf` | thèse de philosophie ; lecture ciblée de l'introduction, de la défense de la thèse dépendantiste et de la conclusion comme étalon de falsifiabilité et de réponse aux contre-exemples |
| `stace1944interestingness` | notice Cambridge Core | article directement consacré à l'intéressant ; métadonnées vérifiées, lecture directe à faire |
| `kolnai1964concept` | notice Oxford Academic | article directement consacré au concept ; métadonnées vérifiées, lecture directe à faire |
| `ngai2008merely` | numéro de *Critical Inquiry* et DOI | article sur l'intéressant comme catégorie esthétique mineure ; métadonnées vérifiées, lecture directe à faire |
| `ngai2012categories` | notice Harvard University Press/Google Books | monographie comprenant l'intéressant parmi trois catégories esthétiques contemporaines ; lecture directe à faire |
| `epstein2009interesting` | Project MUSE et DOI | article transdisciplinaire directement consacré à l'intéressant ; métadonnées vérifiées, lecture directe à faire |
| `grimm2011interesting` | site ouvert de *Logos & Episteme* | article d'épistémologie sur ce qui mérite l'attention intellectuelle ; texte intégral disponible, lecture directe à faire |
| `vazard2026inquiry` | texte intégral HTML sur Oxford Academic ; fiche `docs/lectures/vazard-interet-attention.md` | article lu intégralement ; distingue intérêt dirigé vers un objet et curiosité dirigée vers une question, attention exploratoire et enquête orientée, intérêt ajusté et mal ajusté |
| `nannini2018interesting` | texte intégral de l'*International Lexicon of Aesthetics* | notice généalogique ouverte, lue pour vérifier la tradition et les références prioritaires |
| `oudeyer2007intrinsic` | pas encore dans le corpus | article IEEE sur la curiosité adaptative et les niches de progrès |
| `oudeyer2007typology` | pas encore dans le corpus | typologie computationnelle des motivations intrinsèques |
| `colton2000interestingness` | `input/old_docs/interestingness-ijhcs.pdf` | article de revue |
| `silberschatz1995subjective` | `input/old_docs/kdd95.pdf` | article de conférence |
| `silberschatz1996patterns` | `input/old_docs/interestingness/.../tkde.pdf` | article de revue |
| `spiliopoulou1999rules` | `input/old_docs/interestingness/.../C_PKDD99.pdf` | article de conférence |
| `allouche1999thueMorse` | `input/old_docs/interestingness/.../ubiq.pdf` | chapitre d'actes |
| `gang1999unified` | `input/old_docs/interestingness/.../Dan Gang/aaai99B.pdf` | article de symposium |
| `goldman1999netneg` | `input/old_docs/interestingness/.../Dan Gang/netneg.pdf` | article de revue |
| `berger1999expectations` | `input/old_docs/interestingness/.../Dan Gang/Expectationfinal-paper.pdf` | manuscrit, support éditorial à compléter |
| `kelly2002music` | `input/old_docs/interestingness/.../WhereMusicWillBeComingFromNYTArticle.txt` | article de presse |
| `pachet2026biases` | `input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf` | version longue de 16 pages soumise à NeurIPS, distincte de la v1 arXiv de 9 pages ; MAP exact NP-difficile, normalisation conditionnelle exacte #P-difficile et pertes possibles de support |
| `pachet2026tonalparsimony` | `input/Tonal_Parsimony_in_Chord_Sequence_Analysis.pdf` | prépublication arXiv:2606.03459v1 de 20 pages relue intégralement ; continuité locale, vocabulaire tonal global et cas d'anti-compression mobilisés comme formalisation réflexive, non comme mesure de l'intéressant |
| `norton2012ikea` | notice de l'éditeur et DOI | étude primaire de l'effet IKEA ; l'effet porte sur la valorisation après une construction réussie et ne démontre pas un gain d'apprentissage ou de compréhension |
| `pachet2026generation` | `input/publications-francois-pachet/pachet-2026-generation-musicale-ia.pdf` | article publié ; lecture ciblée des p. 152-154 sur l'effet IKEA, l'appropriation créative et le déplacement de la qualité du résultat vers celle de l'interaction |
| `montecchio2020skipping` | `input/Montecchio_Roy_Pachet_2020_skipping_behavior.pdf` | article PLOS ONE relu intégralement ; résultat scientifique et cas réflexif reliant les recherches menées à Spotify à l'enquête philosophique sur l'intéressant |
| `meyer1956emotion` | pas encore dans le corpus | référence fondatrice sur attente, apprentissage et affect musical ; lecture directe à faire |
| `kubovy1999pleasures` | `docs/On_the_pleasures_of_the_mind.pdf` | chapitre relu intégralement ; séquences émotionnelles, attentes tacites, recherche d'interprétation, critique de la complexité intrinsèque et relecture du flow |
| `narmour1990basic` | pas encore dans le corpus | premier volume du modèle implication-réalisation ; lecture directe à faire |
| `narmour1992complexity` | pas encore dans le corpus | extension du modèle implication-réalisation aux structures complexes ; lecture directe à faire |
| `pachet1999oeuvre` | passages consignés dans `docs/lectures/pachet-oeuvre-des-jours-excitation-idees.md` | livre publié ; lecture ciblée indirecte de l'ouverture et des p. 40-41, lecture intégrale à faire |
| `pachet2018oreille` | `input/PACHET_HISTOIRE_OREILLE_BAT.pdf` | livre publié ; lecture intégrale et extraction propositionnelle effectuées |
| `spinoza1966ethique` | pas encore dans le corpus | traduction Pautrat, Seuil, 1988 ; clé historique conservée pour stabilité ; préface et définition III de la partie III mobilisées |
| `spinoza1861oeuvres` | édition numérique consultée sur Wikisource ; notice BnF liée dans la bibliographie | traduction Saisset, Charpentier, 1861, tome III ; citations vérifiables de la préface et de la proposition XXVII de la partie III |
| `macherey1995vieaffective` | pas encore dans le corpus | étude secondaire de référence sur la partie III et la causalité de la vie affective ; lecture directe à faire |
| `feynman1999pleasure` | pas encore dans le corpus | recueil édité par Jeffrey Robbins ; le titre formule le plaisir épistémique de découvrir et comprendre |
| `florman1996existential` | pas encore dans le corpus | deuxième édition ; philosophie vécue du plaisir de construire propre à l'ingénierie |

Les chemins abrégés par `...` dans ce tableau sont seulement destinés à la lecture.
Les champs `file` de `references.bib` contiennent les chemins complets.
