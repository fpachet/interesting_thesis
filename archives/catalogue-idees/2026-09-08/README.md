# Catalogue des idées — archive du 8 septembre 2026

**Instantané figé, retiré du cycle de mise à jour courant.** Le catalogue contient
162 cartes en huit familles, dans un PDF de 102 pages. Il conserve notamment la
consolidation de la définition et les développements sur *Honey Pie* disponibles
à cette date. Ce n'est pas un manuscrit de thèse.

## Contenu conservé

- [Catalogue PDF](catalogue-idees.pdf) : copie exacte du rendu local du 8 septembre.
- [Source LaTeX](catalogue-idees.tex) : ancien fichier `cartes/catalogue-idees.tex`,
  conservé sans modification.
- [Bibliographie](bibliographie/references.bib) : copie de la bibliographie utilisée.

Les cartes de [l'atelier](../../../cartes/README.md) restent actives. Le générateur
est conservé pour des exports facultatifs vers `output/`, sans réécrire cette archive.
Le PDF garde son titre original « Catalogue provisoire des idées » : son statut
d'archive est porté par ce dossier, sans retouche du document historique.

## Vérification d'intégrité

Les trois fichiers ont été comparés octet par octet aux originaux lors de l'archivage.
Empreintes SHA-256 :

```text
4fd17ef8ad15d48dc384ced4ed4bfad3e4d9ba6f203d3f32fd822e42eb847227  catalogue-idees.tex
fba1dc48de4419fcb9f10e36055704e2b8e56f63e67f83a9844b16006c310d81  catalogue-idees.pdf
d1f9d44f23ebdaf81ff99071ee8ff7dc78f47a8919079486796e049ed23f180c  bibliographie/references.bib
```

Pour recompiler sans écraser le PDF archivé, depuis ce dossier et avec une
distribution LaTeX comprenant latexmk et biber :

```bash
catalogue_build_dir=$(mktemp -d /tmp/catalogue-archive.XXXXXX)
latexmk -pdf -interaction=nonstopmode -halt-on-error -output-directory="$catalogue_build_dir" catalogue-idees.tex
```

Une recompilation peut différer au niveau binaire selon la distribution et ses
métadonnées ; le PDF conservé ci-dessus reste l'instantané de référence.
