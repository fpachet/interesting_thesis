# interesting-thesis

Pipeline Python pour ingerer un corpus personnel et produire un debat philosophique multi-agents autour d'une these configurable.

Sujet par defaut :
`L'objet interessant comme solution relativement rare d'un probleme d'echantillonnage sous contrainte.`

## Ce que fait le pipeline

Le pipeline :

- lit les fichiers `.md`, `.txt`, `.pdf` et `.docx` dans `input/`
- produit un digest du corpus
- lance un debat en plusieurs manches entre des roles configurables
- conserve une memoire structuree dans `memory/state.json`
- ecrit dans `output/` un fichier Markdown par manche, une synthese finale et une liste de paragraphes reutilisables

Les trois roles par defaut sont :

- `Constructeur`
- `Critique`
- `Synthetiseur`

L'orchestrateur reste generique : on peut ajouter plus tard un role supplementaire, par exemple `musicologue`, via `config/default_roles.json` et un prompt dans `prompts/`, a condition de conserver un role final de type `synthesizer`.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Pour un vrai run avec l'API OpenAI :

```bash
export OPENAI_API_KEY="sk-..."
```

Ou bien creer un fichier `.env` a la racine du projet :

```bash
OPENAI_API_KEY="sk-..."
```

Le fichier `.env` est charge automatiquement au demarrage et n'est pas versionne.

## Utilisation

Lancer le pipeline avec les valeurs par defaut :

```bash
python -m interesting_thesis
```

Mode hors-ligne pour verifier le pipeline sans appel API :

```bash
python -m interesting_thesis --dry-run
```

Exemple plus explicite :

```bash
python -m interesting_thesis \
  --theme "L'objet interessant comme solution relativement rare d'un probleme d'echantillonnage sous contrainte." \
  --rounds 4 \
  --output-length long \
  --model gpt-5.4-mini
```

## Options principales

- `--theme` : theme exact du debat
- `--rounds` : nombre de manches
- `--output-length` : `short`, `medium`, `long`
- `--model` : modele OpenAI utilise
- `--roles-file` : fichier JSON de roles
- `--prompts-dir` : dossier des prompts externes
- `--input-dir` : dossier d'entree
- `--output-dir` : dossier de sortie
- `--memory-file` : fichier de memoire JSON
- `--dry-run` : mode local sans reseau pour valider la chaine

## Structure du projet

```text
interesting_thesis/
  __init__.py
  __main__.py
  cli.py
  config.py
  debate.py
  digest.py
  errors.py
  ingestion.py
  llm.py
  memory.py
  models.py
  pipeline.py
  prompts.py
  schemas.py
  text_utils.py
config/
  default_roles.json
prompts/
  critique.md
  constructeur.md
  digest.md
  final_synthesis.md
  synthetiseur.md
input/
output/
memory/
```

## Fichiers generes

Un run ecrit typiquement :

- `output/corpus_digest.md`
- `output/round_01.md`, `output/round_02.md`, etc.
- `output/final_synthesis.md`
- `output/thesis_paragraphs.md`
- `memory/state.json`

## Format des roles

Le fichier `config/default_roles.json` contient une liste ordonnee de roles.
Chaque role declare :

- `key` : identifiant stable
- `name` : nom affiche dans les sorties
- `kind` : `builder`, `critic`, `analyst` ou `synthesizer`
- `prompt_file` : prompt a charger depuis `prompts/`

Le dernier role doit etre de type `synthesizer`.

## Notes d'architecture

- Python 3.11+
- code type et modulaire
- prompts externes dans `prompts/`
- dependencies limitees au SDK OpenAI officiel et aux lecteurs PDF/DOCX
- imports OpenAI paresseux pour ne pas casser `--help` ni le `--dry-run`

## Developpement rapide

Verifier le pipeline sans reseau :

```bash
python -m unittest discover -s tests
```
