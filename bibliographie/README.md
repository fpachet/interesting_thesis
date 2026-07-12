# Bibliographie

`references.bib` est la source canonique des références bibliographiques de la
thèse. Les chemins locaux restent dans les cartes pour garantir la traçabilité ;
le champ YAML optionnel `references` relie une proposition aux clés BibTeX.

## Règles de maintenance

1. Ajouter une entrée BibTeX lorsqu'une source devient effectivement utile à une
   carte ou au manuscrit, pas pour chaque titre mentionne dans une bibliographie.
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

| Clé | Source locale principale | Statut |
| --- | --- | --- |
| `schmidhuber1997interesting` | `input/old_docs/interestingness.pdf` | rapport technique publié |
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
| `meyer1956emotion` | pas encore dans le corpus | référence fondatrice sur attente, apprentissage et affect musical ; lecture directe à faire |
| `narmour1990basic` | pas encore dans le corpus | premier volume du modèle implication-réalisation ; lecture directe à faire |
| `narmour1992complexity` | pas encore dans le corpus | extension du modèle implication-réalisation aux structures complexes ; lecture directe à faire |
| `pachet2018oreille` | `input/PACHET_HISTOIRE_OREILLE_BAT.pdf` | livre publié ; lecture intégrale et extraction propositionnelle effectuées |

Les chemins abrégés par `...` dans ce tableau sont seulement destines à la lecture.
Les champs `file` de `references.bib` contiennent les chemins complets.
