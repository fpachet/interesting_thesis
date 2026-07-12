# Projet de thèse bilingue et versionné

Ce dossier contient les versions française et anglaise du projet de thèse, ainsi
que leurs instantanés historiques.

## Fichiers courants

- `projet-these-fr.tex` : version française courante ;
- `projet-these-en.tex` : version anglaise courante ;
- `versions/projet-these-vN-fr.tex` et `versions/projet-these-vN-en.tex` :
  versions stabilisées et immuables ;
- `CHANGELOG.md` : différences intellectuelles et documentaires entre versions ;
- `Makefile` : compilation et nettoyage des deux rendus.

Les deux fichiers courants doivent rester homologues : mêmes sections, mêmes
hypothèses, mêmes citations et même numéro de version. Une modification de fond
n'est terminée que lorsque sa traduction a été relue.

## Versions historiques

La V1 française est une transcription LaTeX de
`input/projet thèse philo.pdf`. La V1 anglaise a été fournie sous forme de PDF ;
son wrapper LaTeX inclut exactement `input/Project philosophy thesis.pdf` afin de
préserver ce document sans correction silencieuse.

La V2 est la première version réécrite à partir du corpus et des cartes. Ses deux
sources LaTeX sont entièrement éditables et sa bibliographie complète provient de
`bibliographie/references.bib`.

## Cycle d'une nouvelle version

1. Modifier `projet-these-fr.tex` et `projet-these-en.tex`.
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

## Compilation

```bash
cd projet-these
make
```

Les rendus sont écrits dans `projet-these/build/` :

- `projet-these-fr.pdf` ;
- `projet-these-en.pdf`.

Pour nettoyer les artefacts :

```bash
make clean
```
