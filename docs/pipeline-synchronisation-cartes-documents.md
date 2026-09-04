# Pipeline de synchronisation des cartes et des documents

## Principe

Les cartes sont le laboratoire propositionnel du projet, mais elles ne constituent pas
automatiquement le plan de la thèse. Le pipeline doit propager immédiatement les faits
documentaires et les vues calculées, tout en maintenant une décision éditoriale entre
une carte et son entrée dans les synthèses ou le manuscrit.

La règle générale est donc : **synchronisation mécanique immédiate, synchronisation
conceptuelle par lots, versionnement du projet par états intellectuels stabilisés**.

## Sources canoniques et produits dérivés

| Élément | Statut | Règle d'édition |
| --- | --- | --- |
| `cartes/inbox/*.md` | Source canonique des propositions | Éditer directement ; conserver proposition, niveau, provenance, références et limites. |
| `bibliographie/references.bib` | Bibliographie canonique | Éditer directement ; une carte cite une clé existante et conserve séparément le fichier réellement lu. |
| `cartes/indexes/*.md` | Vues éditoriales canoniques | Mettre à jour lorsqu'une carte est créée, reclassée ou change de fonction argumentative. |
| `cartes/relations.tsv` | Graphe canonique des relations fortes | Ajouter seulement les relations directionnelles expliquées qui servent la démonstration. |
| `cartes/REGISTRE_TRAITEMENT.md` et `cartes/COUVERTURE_EXTRACTION.md` | État canonique du corpus | Mettre à jour lorsque la lecture, la version d'une source ou la couverture change. |
| `cartes/ORGANISATION.md` | Synthèse argumentative des cartes | Modifier quand un pivot, une famille ou une question ouverte change réellement. |
| `projet-these/BUT_DE_LA_THESE.md` | Synthèse conceptuelle vivante | Propager les changements du noyau et les distinctions qui modifient la contribution. |
| `projet-these/STRUCTURE_PROVISOIRE.md` | Architecture éditoriale vivante | Propager les changements de fonction des parties, laboratoires et cas. |
| `projet-these/PLAN_ACTION_DEMONSTRATION.md` | Plan de travail vivant | Propager les nouveaux tests, objections et décisions encore nécessaires. |
| `projet-these/projet-these-fr.tex` et `projet-these-en.tex` | Projet bilingue courant | Mettre à jour ensemble lors d'un lot stabilisé, jamais par copie automatique d'une carte. |
| `projet-these/versions/*` | Instantanés immuables | Créer à la fin d'un cycle ; ne pas corriger rétrospectivement sans note explicite. |
| `cartes/catalogue-idees.tex` | Produit généré | Ne pas éditer directement ; régénérer depuis les cartes et l'index argumentatif. |
| `output/pdf/catalogue-idees.pdf` | Produit compilé | Régénérer après le catalogue ; ne pas traiter comme source. |
| `site/dist/` | Produit généré et non versionné | Régénérer localement pour vérifier ; GitHub Pages le reconstruit sur `main`. |

## Déclencheur : ajout ou modification d'une carte

### 1. Stabiliser la carte

Vérifier :

- une proposition contestable et mobilisable indépendamment ;
- `kind`, `level`, `status` et, si la fonction est décidée, `architecture` ;
- les chemins `sources` correspondant aux versions effectivement lues ;
- les pages ou sections dans `source_notes` ;
- les clés `references` présentes dans la bibliographie ;
- les limites d'inférence entre résultat scientifique et proposition philosophique.

Une correction pure de provenance ne déclenche pas à elle seule une réécriture du
projet de thèse. Une modification de la thèse d'une carte `CORE`, en revanche, impose
un audit immédiat des synthèses.

### 2. Propager les dépendances canoniques

Pour une nouvelle carte :

1. ajouter ou corriger sa notice dans `bibliographie/references.bib` ;
2. mettre à jour le registre et la couverture si une source a été nouvellement lue ou
   si sa version a changé ;
3. affecter la carte à exactement une famille dans `indexes/by_argument.md` ;
4. l'ajouter aux index de niveau et de thème ;
5. déclarer son statut architectural lorsqu'il est décidé ;
6. ajouter les relations fortes utiles dans `relations.tsv` ;
7. mettre à jour `ORGANISATION.md` seulement si l'équilibre d'une famille, un pivot ou
   une question ouverte change.

Pour une carte modifiée, ne mettre à jour que les dépendances réellement touchées : une
nouvelle source change la bibliographie ou la couverture ; un changement de fonction
change les index et éventuellement l'organisation ; une simple reformulation locale ne
doit pas produire artificiellement une cascade documentaire.

### 3. Qualifier l'impact éditorial

| Niveau d'impact | Exemple | Propagation requise |
| --- | --- | --- |
| `D0` — documentaire | Pages, version lue, statut de publication | Bibliographie, provenance, registre, catalogue et site. |
| `D1` — local | Exemple, mécanisme ou limite sans changement du noyau | Index/relations si nécessaire ; inscrire dans le prochain audit. |
| `D2` — architectural | Nouveau cas discriminant, objection ou laboratoire | Mettre à jour `STRUCTURE_PROVISOIRE.md` ou `PLAN_ACTION_DEMONSTRATION.md`. |
| `D3` — central | Définition, proposition `CORE`, méthode ou contribution modifiée | Mettre à jour `BUT_DE_LA_THESE.md`, la structure et le plan ; préparer un lot bilingue. |

Cette qualification empêche deux erreurs opposées : laisser les synthèses dériver trop
loin des cartes, ou transformer le manuscrit en concaténation de toutes les cartes.

## Audit de rattrapage périodique

Chaque version du projet doit enregistrer un **commit d'ancrage** : le dernier commit
où les projets FR/EN ont été relus comme homologues. Pour trouver les cartes changées
depuis cette ancre, utiliser :

```bash
git diff --name-status <ancre> -- cartes/inbox
git ls-files --others --exclude-standard cartes/inbox
```

L'audit regroupe ensuite les cartes par dossier argumentatif et consigne pour chaque
dossier : nouveauté, niveau d'impact, documents cibles, décision `intégrer`, `différer`
ou `écarter`, et justification. Le fichier
[`audit-rattrapage-v6-cartes-2026-08-23.md`](audit-rattrapage-v6-cartes-2026-08-23.md)
constitue le premier exemple de ce format.

Un audit est requis :

- avant toute nouvelle version bilingue ;
- après une modification substantielle d'une carte `CORE` ;
- après l'ajout d'un groupe cohérent de cas ou d'objections ;
- lorsqu'un document de synthèse n'a pas été revu depuis plusieurs ajouts de cartes.

## Mise à jour des synthèses

La propagation éditoriale suit cet ordre :

1. `BUT_DE_LA_THESE.md` — ce que la thèse veut établir, avec quelles limites ;
2. `STRUCTURE_PROVISOIRE.md` — où et dans quelle fonction le nouvel élément intervient ;
3. `PLAN_ACTION_DEMONSTRATION.md` — ce qui doit encore être prouvé, comparé ou testé ;
4. projets FR/EN — rédaction publique d'un état stabilisé.

Une carte d'architecture `case` doit entrer dans une synthèse par sa fonction
argumentative, non par la richesse de son domaine. Une carte `speculative` reste
normalement dans l'audit et le programme de recherche. Une carte de niveau `scientific`
ne devient pas une conclusion philosophique sans une carte de niveau `articulation`
qui explicite et limite le passage.

## Cycle d'une nouvelle version bilingue

Une fois le lot conceptuel stabilisé :

1. choisir le nouveau numéro de version avant les modifications de fond ;
2. modifier la version française puis produire et relire la version anglaise homologue ;
3. vérifier mêmes sections, hypothèses, exemples, citations et numéro de version ;
4. compiler les deux projets ;
5. mettre à jour `projet-these/CHANGELOG.md` ;
6. copier exactement les deux sources validées dans
   `projet-these/versions/projet-these-vN-{fr,en}.tex` ;
7. archiver la bibliographie sous `projet-these/versions/references-vN.bib` ;
8. vérifier que les trois fichiers archivés correspondent aux sources compilées ;
9. enregistrer le commit final comme nouvelle ancre de synchronisation.

Les fichiers courants ne doivent pas conserver un ancien numéro après une modification
de fond postérieure à l'instantané portant ce numéro.

## Génération et contrôles locaux

Depuis la racine du dépôt :

```bash
python3 scripts/generate_card_catalog.py
mkdir -p output/pdf
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -output-directory=output/pdf cartes/catalogue-idees.tex
python3 scripts/generate_thesis_site.py
git diff --check
```

Le générateur du catalogue contrôle notamment que l'index argumentatif est exhaustif,
sans doublon ni identifiant inconnu. Le générateur du site relit les cartes, la
bibliographie, l'index argumentatif, l'index thématique, les relations, le but de la
thèse, l'organisation et le registre. Une génération réussie ne prouve toutefois pas
que les synthèses éditoriales sont conceptuellement à jour : c'est précisément la
fonction de l'audit.

Pour tester le site sans modifier la sortie locale habituelle :

```bash
python3 scripts/generate_thesis_site.py --output /tmp/interesting-thesis-site
```

Sur `main`, `.github/workflows/deploy-site.yml` reconstruit et publie automatiquement
`site/dist/`. Ce dossier ne doit pas être versionné ni corrigé manuellement.

## Critère de fin

Une modification est complètement propagée lorsque :

- la carte et ses sources canoniques sont cohérentes ;
- les index, relations et registres concernés sont à jour ;
- l'impact éditorial est décidé et consigné, même si la décision est de différer ;
- les synthèses requises par le niveau d'impact ont été mises à jour ;
- les produits générés compilent ;
- si un nouveau projet est publié, les versions FR/EN, le changelog, les instantanés et
  la bibliographie archivée correspondent exactement.
