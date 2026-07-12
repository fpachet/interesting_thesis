# Projet de these versionne

Ce dossier contient le texte vivant du projet de these et ses instantanes
historiques.

## Fichiers

- `projet-these.tex` : version courante, seule version a modifier pendant le
  travail ordinaire ;
- `versions/projet-these-vN.tex` : versions stabilisees et immuables ;
- `CHANGELOG.md` : differences intellectuelles et documentaires entre versions ;
- `Makefile` : compilation et nettoyage du rendu courant.

Le PDF source `input/projet thèse philo.pdf` est la reference documentaire de la
V1. `versions/projet-these-v1.tex` en est la transcription LaTeX. Le fichier
courant est initialise avec ce meme contenu : aucune idee posterieure n'a ete
retroactivement attribuee a la V1.

## Cycle d'une nouvelle version

1. Modifier `projet-these.tex` et incrementer `\projectversion`.
2. Compiler avec `make` et relire `build/projet-these.pdf`.
3. Decrire dans `CHANGELOG.md` les changements de question, d'hypotheses, de
   methode, de corpus et de structure.
4. Lorsque l'etat est valide, le copier vers
   `versions/projet-these-vN.tex` et ne plus modifier cet instantane.
5. Committer ensemble le fichier courant, l'instantane et le changelog.

Une version est un etat intellectuel identifiable, pas chaque correction
typographique. Git conserve deja l'historique fin entre deux versions nommees.

## Compilation

```bash
cd projet-these
make
```

Le rendu est ecrit dans `projet-these/build/`, qui n'est pas versionne.

Pour nettoyer les artefacts :

```bash
make clean
```

