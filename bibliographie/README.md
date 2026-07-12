# Bibliographie

`references.bib` est la source canonique des references bibliographiques de la
these. Les chemins locaux restent dans les cartes pour garantir la tracabilite ;
le champ YAML optionnel `references` relie une proposition aux cles BibTeX.

## Regles de maintenance

1. Ajouter une entree BibTeX lorsqu'une source devient effectivement utile a une
   carte ou au manuscrit, pas pour chaque titre mentionne dans une bibliographie.
2. Utiliser une cle stable de la forme `auteurAnneeMot`, sans la renommer ensuite.
3. Verifier le titre, les auteurs, l'annee et le support sur la source primaire ou
   la page de l'editeur.
4. Conserver dans `file` le chemin relatif du document local lorsqu'il existe.
5. Employer `@unpublished` ou `@techreport` quand le statut editorial n'est pas
   etabli ; ne pas deduire une publication de la seule presence d'un PDF.
6. Ajouter la cle dans `references` sur chaque carte qui mobilise directement la
   publication.

Les documents personnels, grants, notes, courriels et archives restent inventories
dans `cartes/REGISTRE_TRAITEMENT.md`. Ils ne deviennent des entrees bibliographiques
que s'ils doivent etre cites dans le manuscrit.

## Projet de thèse V2

La réécriture bilingue du projet de thèse utilise directement ce fichier avec
BibLaTeX. Les références philosophiques seulement esquissées dans la V1 ont été
complétées à partir de la bibliographie détaillée du PDF anglais. Les entrées de
Petitot, Berlyne, Schmidhuber, Abdallah et Plumbley ont été contrôlées sur les
pages d'éditeur, dépôts institutionnels ou notices primaires disponibles.

Les deux fichiers `projet-these/projet-these-fr.tex` et
`projet-these/projet-these-en.tex` doivent employer les mêmes clés. Chaque version
stabilisée archive une copie de ce fichier dans `projet-these/versions/` afin que
son rendu bibliographique reste reproductible.

## Correspondance initiale

| Cle | Source locale principale | Statut |
| --- | --- | --- |
| `schmidhuber1997interesting` | `input/old_docs/interestingness.pdf` | rapport technique publie |
| `colton2000interestingness` | `input/old_docs/interestingness-ijhcs.pdf` | article de revue |
| `silberschatz1995subjective` | `input/old_docs/kdd95.pdf` | article de conference |
| `silberschatz1996patterns` | `input/old_docs/interestingness/.../tkde.pdf` | article de revue |
| `spiliopoulou1999rules` | `input/old_docs/interestingness/.../C_PKDD99.pdf` | article de conference |
| `allouche1999thueMorse` | `input/old_docs/interestingness/.../ubiq.pdf` | chapitre d'actes |
| `gang1999unified` | `input/old_docs/interestingness/.../Dan Gang/aaai99B.pdf` | article de symposium |
| `goldman1999netneg` | `input/old_docs/interestingness/.../Dan Gang/netneg.pdf` | article de revue |
| `berger1999expectations` | `input/old_docs/interestingness/.../Dan Gang/Expectationfinal-paper.pdf` | manuscrit, support editorial a completer |
| `kelly2002music` | `input/old_docs/interestingness/.../WhereMusicWillBeComingFromNYTArticle.txt` | article de presse |
| `pachet2026biases` | `input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf` | manuscrit non publie |
| `meyer1956emotion` | pas encore dans le corpus | reference fondatrice sur attente, apprentissage et affect musical ; lecture directe a faire |
| `narmour1990basic` | pas encore dans le corpus | premier volume du modele implication-realisation ; lecture directe a faire |
| `narmour1992complexity` | pas encore dans le corpus | extension du modele implication-realisation aux structures complexes ; lecture directe a faire |
| `pachet2018oreille` | `input/PACHET_HISTOIRE_OREILLE_BAT.pdf` | livre publie ; lecture integrale et extraction propositionnelle effectuees |

Les chemins abreges par `...` dans ce tableau sont seulement destines a la lecture.
Les champs `file` de `references.bib` contiennent les chemins complets.
