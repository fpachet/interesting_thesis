# Bibliographie

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

- `pachet1997representation` ;
- `pachet2006clefs`, `pachet2008machines` et `pachet2012virtuosity` ;
- `pachet2018oreille` et `montecchio2020skipping` ;
- `pachet2021assisted` ;
- `pachet2026biases`, `pachet2026impossibilite` et `pachet2026markov` ;
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
| `pachet1997representation` | `input/Pachet_Representation_connaissances_langages_objets_1997.pdf` | mémoire d'HDR ; conserve la formulation orale longue de Russell sur les parties intéressantes définies hors du problème, PDF p. 10 |
| `bachimont1996hermeneutique` | `docs/Bachimont.pdf` | thèse d'épistémologie ; lecture ciblée des PDF p. 322-323 sur la reconstruction de la question, la fusion des horizons et l'innovation interprétative |
| `anselin2021attention` | `input/theses-comparaison/anselin-2021-accorder-son-attention.pdf` | thèse de philosophie ; lecture ciblée de l'introduction, des chapitres 1-3, des objections et de la conclusion comme étalon d'architecture argumentative |
| `thalabard2012attention` | `input/theses-comparaison/thalabard-2012-attention-et-conscience.pdf` | thèse de philosophie ; lecture ciblée de l'introduction, de la défense de la thèse dépendantiste et de la conclusion comme étalon de falsifiabilité et de réponse aux contre-exemples |
| `stace1944interestingness` | notice Cambridge Core | article directement consacré à l'intéressant ; métadonnées vérifiées, lecture directe à faire |
| `kolnai1964concept` | notice Oxford Academic | article directement consacré au concept ; métadonnées vérifiées, lecture directe à faire |
| `ngai2008merely` | numéro de *Critical Inquiry* et DOI | article sur l'intéressant comme catégorie esthétique mineure ; métadonnées vérifiées, lecture directe à faire |
| `ngai2012categories` | notice Harvard University Press/Google Books | monographie comprenant l'intéressant parmi trois catégories esthétiques contemporaines ; lecture directe à faire |
| `epstein2009interesting` | Project MUSE et DOI | article transdisciplinaire directement consacré à l'intéressant ; métadonnées vérifiées, lecture directe à faire |
| `grimm2011interesting` | site ouvert de *Logos & Episteme* | article d'épistémologie sur ce qui mérite l'attention intellectuelle ; texte intégral disponible, lecture directe à faire |
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
| `pachet2026biases` | `input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf` | manuscrit non publié |
| `montecchio2020skipping` | `input/Montecchio_Roy_Pachet_2020_skipping_behavior.pdf` | article PLOS ONE relu intégralement ; résultat scientifique et cas réflexif reliant les recherches menées à Spotify à l'enquête philosophique sur l'intéressant |
| `meyer1956emotion` | pas encore dans le corpus | référence fondatrice sur attente, apprentissage et affect musical ; lecture directe à faire |
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
