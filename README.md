# L'émergence de l'intéressant

Ce dépôt est l'atelier documentaire et conceptuel d'un projet de thèse en
philosophie consacré à **l'émergence de l'intéressant** : naissance des idées,
compréhension et singularité des formes.

**[Consulter le site public de suivi de la thèse](https://fpachet.github.io/interesting_thesis/)**

La question directrice est : **dans quelles conditions un objet déclenche-t-il
chez un sujet un processus de construction ? Comment ce processus se poursuit-il,
s'épuise-t-il ou se transforme-t-il ?** Le projet cherche à comprendre ensemble
des phénomènes habituellement séparés : le surgissement d'une idée, l'impression de
comprendre, l'attention soutenue par une œuvre et la nécessité rétrospective de
certaines formes.

Le point de départ est une pratique de recherche en intelligence artificielle,
notamment en génération musicale et textuelle. L'objectif n'est toutefois pas de
transformer automatiquement ces travaux en théorie philosophique. Il faut
distinguer les constructions et résultats scientifiques, les propositions
conceptuelles, puis argumenter explicitement les passages entre les deux.

## Trois documents de travail

Depuis le 8 septembre 2026, l'entretien éditorial courant repose sur trois documents,
en plus des cartes et de leurs données :

1. [Définition et défense](docs/defense-concept-interessant.md) : ce que nous
   soutenons, les arguments, les cas développés et les objections encore ouvertes.
2. [Plan d'action](projet-these/PLAN_ACTION_DEMONSTRATION.md) : les décisions,
   l'architecture envisagée, l'avancement et le prochain travail.
3. [Projet de thèse français](projet-these/projet-these-fr.tex) : la présentation
   destinée à un lecteur, actualisée par étapes intellectuelles significatives.

**Prochain travail :** mettre à l'épreuve la définition avec O12, une construction
réellement inventive mais sans intérêt éprouvé. Le futur manuscrit « thèse dans
l'état présent » est demandé et inscrit au plan, mais sa rédaction est différée.

Une idée nouvelle n'entraîne plus une mise à jour de tous les documents. La
[Défense](docs/defense-concept-interessant.md) porte l'état conceptuel post-V15 ;
le projet français et sa traduction anglaise restent pour l'instant en V15.
Le [mode de travail](docs/pipeline-synchronisation-cartes-documents.md) précise
quand intervenir dans chaque fichier.

## Références, adaptations et vues

- [Cartes](cartes/README.md), [index argumentatif](cartes/indexes/by_argument.md)
  et [relations](cartes/relations.tsv) : propositions et navigation dans le corpus.
- [Bibliographie](bibliographie/references.bib) et [sources](input/) : appuis
  documentaires ; le [registre](cartes/REGISTRE_TRAITEMENT.md) et la
  [couverture](cartes/COUVERTURE_EXTRACTION.md) suivent les lectures effectives.
- [But de la thèse](projet-these/BUT_DE_LA_THESE.md),
  [structure provisoire](projet-these/STRUCTURE_PROVISOIRE.md),
  [organisation des cartes](cartes/ORGANISATION.md) et
  [matrice comparative](docs/matrice-tests-interessant.md) : références conservées
  en l'état, sans synchronisation systématique.
- [Version anglaise](projet-these/projet-these-en.tex) et
  [version courte](projet-these/projet-these-court-fr.tex) : adaptations, à reprendre
  lors d'une diffusion ou d'un besoin précis.
- [Catalogue des idées archivé au 8 septembre 2026](archives/catalogue-idees/2026-09-08/README.md) :
  instantané conservant le PDF, sa source et sa bibliographie ; les cartes restent vivantes.
- [Site](site/README.md) : vue générée des cartes et des documents actifs, sans
  deuxième saisie de la définition ni des questions courantes.
- [Versions historiques](projet-these/versions/) et
  [journal des versions](projet-these/CHANGELOG.md) : mémoire des étapes achevées.

L'orchestrateur de dialogues reste un outil expérimental disponible, et non le
centre du travail de thèse.

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
actuellement la version 15 et partagent la bibliographie canonique. Cette version
intègre l'essai court sur *Honey Pie*. Les développements ultérieurs sont conservés
dans la Défense et signalés dans le plan jusqu'à leur intégration à une prochaine version.

Lorsqu'une nouvelle étape intellectuelle est prête à être archivée :

1. réviser le projet français à partir du lot argumenté, puis adapter l'anglais
   pour obtenir deux versions homologues ;
2. compiler et relire les deux rendus ;
3. décrire les changements dans `projet-these/CHANGELOG.md` ;
4. copier l'état valide dans les deux instantanés
   `projet-these/versions/projet-these-vN-{fr,en}.tex` et archiver la bibliographie.

Le dossier contient les commandes exactes de compilation et les règles de
versionnement.

## Structure

```text
archives/            instantanés documentaires retirés du travail courant
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
