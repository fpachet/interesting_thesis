# Projet de thèse bilingue et versionné

Ce dossier contient les versions française et anglaise du projet de thèse, ainsi
que leurs instantanés historiques.

## Documents actifs et adaptations

Les trois documents actifs du projet sont :

1. [Définition et défense](../docs/defense-concept-interessant.md) : contenu
   conceptuel courant et arguments, y compris les développements post-V15.
2. [Plan d'action](PLAN_ACTION_DEMONSTRATION.md) : décisions, architecture,
   avancement et étapes à franchir.
3. [Projet français](projet-these-fr.tex) : présentation pour un lecteur,
   actualisée par étapes significatives ; actuellement V15.

L'anglais (`projet-these-en.tex`) est une adaptation du français lors de la préparation
d'une version bilingue. La version courte (`projet-these-court-fr.tex`) est adaptée
pour les besoins de présentation et les dossiers administratifs. Ce ne sont pas
deux sources conceptuelles supplémentaires à synchroniser après chaque échange.

[BUT_DE_LA_THESE.md](BUT_DE_LA_THESE.md) et
[STRUCTURE_PROVISOIRE.md](STRUCTURE_PROVISOIRE.md) sont des références conservées
en l'état, sans maintenance systématique. Les décisions d'architecture vont désormais
dans le plan, les formulations conceptuelles dans la Défense.

`versions/` conserve les instantanés immuables ; `CHANGELOG.md` décrit les différences
entre versions ; `Makefile` compile les trois rendus de présentation.
Les versions longues française et anglaise diffusées doivent rester homologues :
mêmes sections, hypothèses, citations et numéro de version.

Le manuscrit **« thèse dans l'état présent »** demandé par l'auteur est un livrable
distinct, différé et inscrit au plan. Il n'est pas encore rédigé.

## Versions historiques

La V1 française est une transcription LaTeX de
`input/projet thèse philo.pdf`. La V1 anglaise a été fournie sous forme de PDF ;
son wrapper LaTeX inclut exactement `input/Project philosophy thesis.pdf` afin de
préserver ce document sans correction silencieuse.

La V2 est la première version réécrite à partir du corpus et des cartes. Ses deux
sources LaTeX sont entièrement éditables et sa bibliographie complète provient de
`bibliographie/references.bib`.

La V3 réorganise le projet en trois mouvements : constituer le problème,
construire le concept et le mettre au travail. Elle intègre l'état de l'art, la
définition constructive, les quatorze propriétés candidates, la récursivité et
les cinq terrains d'épreuve.

La V4 intègre la lecture directe de Garve comme antécédent du mécanisme
constructif. Elle déplace l'originalité vers sa systématisation et ajoute la
difficultuosité ainsi que la chalépodoxie à partir de *La virtuosité à la portée
des caniches*, à paraître chez Hermann en 2027.

La V5 explique pourquoi ce programme garvien n'a pas fondé de tradition
cumulative : défaite de la *Popularphilosophie*, captures kantienne, romantique
et morale, puis dispersion disciplinaire. Elle déplace l'intéressant hors de la
seule esthétique vers une fonction générale de mobilisation du psychisme, mise
en relation avec Maslow, l'ennui et l'avertissement de Russell contre la
formalisation prématurée.

La V6 examine Pierre Pachet comme indice possible d'une survie de la philosophie
du particulier dans l'essai, sans postuler de filiation avec Garve. Elle formule
la méthode de la thèse comme boucle entre fidélité au phénomène et extraction de
structure, sous la maxime : « Conceptualiser l'intéressant sans désintéresser le
concept de l'expérience qui lui donne naissance. »

La V7 remplace l'idée trop globale d'une hostilité de la formalisation par le
risque plus précis de substitution de cible. Elle distingue cible, indicateur et
procédure effective à partir de *Hidden Biases in Conditioning Autoregressive
Models*, puis utilise la parcimonie tonale et ses cas d'anti-compression comme
exemple positif de formalisation réflexive. Elle ajoute au laboratoire IA le test
d'une boucle entre exploration en largeur, résolution en profondeur et révision de
la représentation, tout en maintenant l'hypothèse statistique sur la rareté de
l'intéressant dans la réserve spéculative.

La V8 intègre l'article de Juliette Vazard sur l'intérêt comme valeur d'une
attention soutenue. Elle distingue la curiosité dirigée vers une question de
l'intérêt dirigé vers un objet avant que les questions pertinentes soient
disponibles. La définition constructive est corrigée en conséquence : une phase
d'attention exploratoire ouverte peut précéder la construction orientée vers une
prise, et faire apparaître la question peut constituer la première prise.

La V9 précise le statut ontologique de ce mécanisme. L'intéressant n'est pas un état
mental placé à côté de l'attention, de la curiosité ou des émotions, mais la relation
sujet-objet qui peut les actualiser, organiser leurs transitions et transformer les
possibilités ultérieures du sujet. La formule de « moteur de la vie psychique » est
retenue au sens limité de moteur de l'activité exploratoire et auto-transformatrice.

La V10 introduit l'analyse intérescentielle de la littérature. Elle distingue ce qui
motive un personnage de ce qui devient pour lui une source de prises nouvelles, puis
compare Proust, *Bartleby* et le *Livre de Job*. Job devient le cas négatif d'une
motivation morale et affective extrême sans intérescence interne identifiable, tandis
que l'énigme produit une intérescence externe chez le lecteur. Cette différence ouvre
une hypothèse généalogique prudente sur le déplacement d'un moteur moral ou religieux
vers des relations immanentes d'intérescence.

La V11 demande si l'on peut rendre tout intéressant. Elle décrit l'enseignement comme
l'accompagnement du travail mental par lequel une matière devient intéressante, et
l'ingéniosité pédagogique comme construction des conditions d'une construction que
l'élève doit accomplir. L'anecdote de Gilles de La Ménardière sur le droit administratif
sert de cas, non de preuve universelle. L'autonomie acquise permet de distinguer cet
accompagnement d'une simple séduction par le médiateur.

La V12 resserre le cœur conceptuel : « Est intéressant, pour un sujet, ce qui déclenche
chez lui un processus de construction. » Elle définit concrètement la construction et
présente *intérescence* comme le nom proposé pour la dynamique déclenchée. Elle mentionne
la traduction intégrale de Garve menée avec Christian Berner pour les éditions Vrin. Le
développement sur Pierre Pachet ainsi que la section sur l'intéressant, le vrai et
l'anecdote de Heinz Wismann sont retirés du projet courant.

La V13 reprend l'ensemble dans une langue plus simple et plus directe. Elle remplace
les formules abstraites qui masquaient l'argument, parle de terrains d'étude plutôt
que de laboratoires et présente positivement le rôle des textes philosophiques.

La V14 ajoute l'hypothèse selon laquelle l'intéressant peut être à la racine de la
réification. Ce qui devient intéressant se détache du fond et devient un objet pour un
sujet ; la réification commence lorsque cette naissance relationnelle est oubliée. La
version distingue ce cas vécu des réifications administratives, marchandes ou
automatiques qui peuvent s'imposer sans intérêt préalable.

La V15 intègre l'essai court *Honey Pie : une note qui fait question* dans la partie
musicale et sa traduction anglaise. Elle relie l'accroche, la question « comment ça
marche ? », la reconstruction et la réécoute à la définition constructive, sans
présenter les variantes proposées comme des observations déjà réalisées.
Le [dossier musical](../docs/notes/honey-pie-jotney.md) conserve les sources,
la réduction notée et les vérifications restant à faire.

## Cycle d'une nouvelle version

1. Réviser `projet-these-fr.tex` à partir d'un lot argumenté, puis adapter
   `projet-these-en.tex` pour cette version bilingue.
2. Incrémenter `\projectversion` dans les deux fichiers.
3. Compiler avec `make` et relire les deux PDF.
4. Décrire dans `CHANGELOG.md` les changements de question, d'hypothèses, de
   méthode, de corpus et de structure.
5. Copier l'état validé vers les deux fichiers `versions/projet-these-vN-*.tex`.
6. Archiver avec eux une copie `versions/references-vN.bib` de la bibliographie
   utilisée.
7. Committer ensemble les deux langues, les instantanés et le changelog.

Une version est un état intellectuel identifiable, pas chaque correction
typographique. Git conserve l'historique fin entre deux versions nommées.

## Synchronisation avec les cartes

Le mode de travail à trois documents actifs et les adaptations à la demande sont décrits
dans [`../docs/pipeline-synchronisation-cartes-documents.md`](../docs/pipeline-synchronisation-cartes-documents.md).
L'[`audit du 23 août 2026`](../docs/audit-rattrapage-v6-cartes-2026-08-23.md)
prend le commit `302cfa2` comme état éditorial terminal de fait de la V6.
L'[`audit V10 du 24 août 2026`](../docs/audit-interescence-litterature-v10-2026-08-24.md)
consigne la séparation entre motivation, morale et intérescence dans le cas de Job.

Les instantanés `versions/projet-these-v6-{fr,en}.tex` ont été créés avant les derniers
enrichissements demeurés sous le numéro 6. Ils sont conservés comme traces historiques
et ne doivent pas être corrigés silencieusement. La V7 rétablit la correspondance
stricte entre numéro, sources courantes, instantanés, bibliographie et changelog.
La V8 conserve cette correspondance et ajoute son propre triplet d'instantanés
`projet-these-v8-{fr,en}.tex` et `references-v8.bib`. La V9 fait de même avec
`projet-these-v9-{fr,en}.tex` et `references-v9.bib`. La V10 est archivée dans
`projet-these-v10-{fr,en}.tex` et `references-v10.bib`. La V11 est archivée dans
`projet-these-v11-{fr,en}.tex` et `references-v11.bib`. La V12 est archivée dans
`projet-these-v12-{fr,en}.tex` et `references-v12.bib`. La V13 est archivée dans
`projet-these-v13-{fr,en}.tex` et `references-v13.bib`. La V14 est archivée dans
`projet-these-v14-{fr,en}.tex` et `references-v14.bib`. La V15 est archivée dans
`projet-these-v15-{fr,en}.tex` et `references-v15.bib` ; son
[audit](../docs/audit-honey-pie-v15-2026-09-08.md) consigne l'intégration de l'essai.

## Compilation

```bash
cd projet-these
make
```

Les rendus sont écrits dans `projet-these/build/` :

- `projet-these-fr.pdf` ;
- `projet-these-en.pdf` ;
- `projet-these-court-fr.pdf`.

Pour nettoyer les artefacts :

```bash
make clean
```
