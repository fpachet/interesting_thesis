# L'émergence de l'intéressant

Ce dépôt est l'atelier documentaire et conceptuel d'un projet de thèse en
philosophie consacré à **l'émergence de l'intéressant** : naissance des idées,
compréhension et singularité des formes.

La question directrice est : **sous quelles conditions quelque chose apparaît-il
à un sujet comme intéressant ?** Le projet cherche à comprendre ensemble des
phénomènes habituellement séparés : le surgissement d'une idée, l'impression de
comprendre, l'attention soutenue par une œuvre et la nécessité rétrospective de
certaines formes.

Le point de départ est une pratique de recherche en intelligence artificielle,
notamment en génération musicale et textuelle. L'objectif n'est toutefois pas de
transformer automatiquement ces travaux en théorie philosophique. Il faut
distinguer les constructions et résultats scientifiques, les propositions
conceptuelles, puis argumenter explicitement les passages entre les deux.

## Travail actuel

Le travail se concentre maintenant sur quatre activités :

1. constituer un corpus fiable de sources actuelles et d'archives ;
2. distiller ces documents en propositions substantielles et sourcées ;
3. organiser progressivement ces propositions en familles et en arguments ;
4. maintenir un projet de thèse vivant, versionné et compilable.

Le projet antérieur d'orchestration de dialogues entre rôles philosophiques reste
disponible comme outil expérimental. Il n'est plus le centre du dépôt et pourra
être réactivé plus tard pour mettre à l'épreuve une question délimitée, formuler
des objections ou comparer plusieurs architectures argumentatives.

## Points d'entrée

- [`site/`](site/) : site statique de présentation et de suivi, généré dynamiquement
  depuis les cartes et les documents d'organisation ;
- [`projet-these/projet-these-fr.tex`](projet-these/projet-these-fr.tex) et
  [`projet-these/projet-these-en.tex`](projet-these/projet-these-en.tex) :
  versions courantes française et anglaise du projet de thèse ;
- [`projet-these/versions/`](projet-these/versions/) : instantanés historiques
  immuables ;
- [`projet-these/CHANGELOG.md`](projet-these/CHANGELOG.md) : évolution explicite
  du projet ;
- [`projet-these/BUT_DE_LA_THESE.md`](projet-these/BUT_DE_LA_THESE.md) : objet,
  tâches philosophiques et résultat attendu de la thèse ;
- [`cartes/inbox/`](cartes/inbox/) : propositions extraites du corpus ;
- [`cartes/ORGANISATION.md`](cartes/ORGANISATION.md) : lignes argumentatives,
  pivots, recouvrements et questions ouvertes ;
- [`cartes/indexes/by_argument.md`](cartes/indexes/by_argument.md) : affectation
  exhaustive des cartes à sept familles argumentatives ;
- [`cartes/relations.tsv`](cartes/relations.tsv) : premier graphe de relations
  fortes et typées entre propositions ;
- [`cartes/indexes/by_theme.md`](cartes/indexes/by_theme.md) : regroupement
  thématique provisoire ;
- [`cartes/indexes/by_level.md`](cartes/indexes/by_level.md) : distinction entre
  propositions conceptuelles, scientifiques et articulations ;
- [`cartes/REGISTRE_TRAITEMENT.md`](cartes/REGISTRE_TRAITEMENT.md) : état de
  lecture de chaque source ;
- [`cartes/COUVERTURE_EXTRACTION.md`](cartes/COUVERTURE_EXTRACTION.md) : contrôle détaillé de la couverture propositionnelle ;
- [`bibliographie/references.bib`](bibliographie/references.bib) : bibliographie
  canonique ;
- [`input/`](input/) : corpus documentaire, avec les archives dans
  `input/old_docs/`.

## Principe des cartes

Une carte n'est ni un thème général ni le résumé d'un document. Elle formule une
affirmation, une hypothèse, une distinction, une objection ou une méthode que la
thèse pourrait soutenir, discuter ou mettre à l'épreuve.

Avant de créer une carte, une source nouvelle est confrontée aux propositions
existantes. Une carte n'est ajoutée que si l'idée peut être contestée ou mobilisée
indépendamment ; les exemples, mécanismes et limites qui servent une même
proposition restent regroupés. Chaque provenance connue est indiquée avec son
chemin local et, lorsque c'est possible, ses pages et sa clé bibliographique.

Le format et le cycle de travail sont documentés dans
[`cartes/README.md`](cartes/README.md).

## Projet de thèse versionné

Les PDF initiaux français et anglais, respectivement
[`input/projet thèse philo.pdf`](input/projet%20thèse%20philo.pdf) et
[`input/Project philosophy thesis.pdf`](input/Project%20philosophy%20thesis.pdf),
constituent la version 1 du projet. Ils sont conservés dans
`projet-these/versions/`. Les deux fichiers de travail bilingues portent
actuellement la version 2 et partagent la bibliographie canonique.

Lorsqu'une nouvelle étape intellectuelle est stabilisée :

1. mettre à jour les deux fichiers courants en maintenant leurs sections
   synchronisées ;
2. compiler et relire les deux rendus ;
3. décrire les changements dans `projet-these/CHANGELOG.md` ;
4. copier l'état valide dans `projet-these/versions/projet-these-vN.tex`.

Le dossier contient les commandes exactes de compilation et les règles de
versionnement.

## Structure

```text
bibliographie/       références et règles bibliographiques
cartes/              propositions, index et suivi de couverture
input/               sources actuelles et archives
projet-these/        projet courant, versions et journal des changements
interesting_thesis/  moteur Python d'ingestion et de dialogue
config/              configurations de l'orchestrateur
prompts/             rôles et prompts de dialogue
output/              anciens runs et sorties générées
memory/              état des runs
tests/               contrôles du moteur et des métadonnées
```

## Orchestrateur expérimental

Le pipeline Python peut encore ingérer un corpus, produire un digest et organiser
un dialogue en plusieurs manches entre des rôles configurables. Les runs sont
conservés dans `output/runs/<run_id>/` et leur mémoire dans
`memory/runs/<run_id>.json`.

Installation :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Vérification locale sans appel réseau :

```bash
python -m interesting_thesis --dry-run
```

Lancement explicite d'un dialogue :

```bash
python -m interesting_thesis \
  --theme "Question philosophique délimitée" \
  --rounds 4 \
  --output-length long \
  --run-id question_01
```

Les fonctions de reprise et de fork restent disponibles avec `--resume-run`,
`--fork-run`, `--from-checkpoint` et `--user-note`. Leur architecture et leurs
extensions possibles sont décrites dans
[`docs/v2_orchestration.md`](docs/v2_orchestration.md).

## Vérification

```bash
python -m unittest discover -s tests
```
