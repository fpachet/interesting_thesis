# L'emergence de l'interessant

Ce depot est l'atelier documentaire et conceptuel d'un projet de these en
philosophie consacre a **l'emergence de l'interessant** : naissance des idees,
comprehension et singularite des formes.

La question directrice est : **sous quelles conditions quelque chose apparait-il
a un sujet comme interessant ?** Le projet cherche a comprendre ensemble des
phenomenes habituellement separes : le surgissement d'une idee, l'impression de
comprendre, l'attention soutenue par une oeuvre et la necessite retrospective de
certaines formes.

Le point de depart est une pratique de recherche en intelligence artificielle,
notamment en generation musicale et textuelle. L'objectif n'est toutefois pas de
transformer automatiquement ces travaux en theorie philosophique. Il faut
distinguer les constructions et resultats scientifiques, les propositions
conceptuelles, puis argumenter explicitement les passages entre les deux.

## Travail actuel

Le travail se concentre maintenant sur quatre activites :

1. constituer un corpus fiable de sources actuelles et d'archives ;
2. distiller ces documents en propositions substantielles et sourcees ;
3. organiser progressivement ces propositions en familles et en arguments ;
4. maintenir un projet de these vivant, versionne et compilable.

Le projet anterieur d'orchestration de dialogues entre roles philosophiques reste
disponible comme outil experimental. Il n'est plus le centre du depot et pourra
etre reactive plus tard pour mettre a l'epreuve une question delimitee, formuler
des objections ou comparer plusieurs architectures argumentatives.

## Points d'entree

- [`projet-these/projet-these-fr.tex`](projet-these/projet-these-fr.tex) et
  [`projet-these/projet-these-en.tex`](projet-these/projet-these-en.tex) :
  versions courantes française et anglaise du projet de thèse ;
- [`projet-these/versions/`](projet-these/versions/) : instantanes historiques
  immuables ;
- [`projet-these/CHANGELOG.md`](projet-these/CHANGELOG.md) : evolution explicite
  du projet ;
- [`cartes/inbox/`](cartes/inbox/) : propositions extraites du corpus ;
- [`cartes/indexes/by_theme.md`](cartes/indexes/by_theme.md) : regroupement
  thematique provisoire ;
- [`cartes/indexes/by_level.md`](cartes/indexes/by_level.md) : distinction entre
  propositions conceptuelles, scientifiques et articulations ;
- [`cartes/REGISTRE_TRAITEMENT.md`](cartes/REGISTRE_TRAITEMENT.md) : etat de
  lecture de chaque source ;
- [`cartes/COUVERTURE_EXTRACTION.md`](cartes/COUVERTURE_EXTRACTION.md) : controle
  detaille de la couverture propositionnelle ;
- [`bibliographie/references.bib`](bibliographie/references.bib) : bibliographie
  canonique ;
- [`input/`](input/) : corpus documentaire, avec les archives dans
  `input/old_docs/`.

## Principe des cartes

Une carte n'est ni un theme general ni le resume d'un document. Elle formule une
affirmation, une hypothese, une distinction, une objection ou une methode que la
these pourrait soutenir, discuter ou mettre a l'epreuve.

Avant de creer une carte, une source nouvelle est confrontee aux propositions
existantes. Une carte n'est ajoutee que si l'idee peut etre contestee ou mobilisee
independamment ; les exemples, mecanismes et limites qui servent une meme
proposition restent regroupes. Chaque provenance connue est indiquee avec son
chemin local et, lorsque c'est possible, ses pages et sa cle bibliographique.

Le format et le cycle de travail sont documentes dans
[`cartes/README.md`](cartes/README.md).

## Projet de these versionne

Les PDF initiaux français et anglais, respectivement
[`input/projet thèse philo.pdf`](input/projet%20thèse%20philo.pdf) et
[`input/Project philosophy thesis.pdf`](input/Project%20philosophy%20thesis.pdf),
constituent la version 1 du projet. Ils sont conservés dans
`projet-these/versions/`. Les deux fichiers de travail bilingues portent
actuellement la version 2 et partagent la bibliographie canonique.

Lorsqu'une nouvelle etape intellectuelle est stabilisee :

1. mettre a jour les deux fichiers courants en maintenant leurs sections
   synchronisées ;
2. compiler et relire les deux rendus ;
3. decrire les changements dans `projet-these/CHANGELOG.md` ;
4. copier l'etat valide dans `projet-these/versions/projet-these-vN.tex`.

Le dossier contient les commandes exactes de compilation et les regles de
versionnement.

## Structure

```text
bibliographie/       references et regles bibliographiques
cartes/              propositions, index et suivi de couverture
input/               sources actuelles et archives
projet-these/        projet courant, versions et journal des changements
interesting_thesis/  moteur Python d'ingestion et de dialogue
config/              configurations de l'orchestrateur
prompts/             roles et prompts de dialogue
output/              anciens runs et sorties generees
memory/              etat des runs
tests/               controles du moteur et des metadonnees
```

## Orchestrateur experimental

Le pipeline Python peut encore ingerer un corpus, produire un digest et organiser
un dialogue en plusieurs manches entre des roles configurables. Les runs sont
conserves dans `output/runs/<run_id>/` et leur memoire dans
`memory/runs/<run_id>.json`.

Installation :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Verification locale sans appel reseau :

```bash
python -m interesting_thesis --dry-run
```

Lancement explicite d'un dialogue :

```bash
python -m interesting_thesis \
  --theme "Question philosophique delimitee" \
  --rounds 4 \
  --output-length long \
  --run-id question_01
```

Les fonctions de reprise et de fork restent disponibles avec `--resume-run`,
`--fork-run`, `--from-checkpoint` et `--user-note`. Leur architecture et leurs
extensions possibles sont decrites dans
[`docs/v2_orchestration.md`](docs/v2_orchestration.md).

## Verification

```bash
python -m unittest discover -s tests
```
