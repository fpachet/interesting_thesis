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

Les chemins abreges par `...` dans ce tableau sont seulement destines a la lecture.
Les champs `file` de `references.bib` contiennent les chemins complets.
