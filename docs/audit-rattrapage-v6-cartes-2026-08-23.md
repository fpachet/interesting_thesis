# Audit de rattrapage entre la V6 et les cartes

Date de l'audit : 23 août 2026.

Statut : appliqué aux synthèses et au projet bilingue V7 le 23 août 2026.

## Objet et point de comparaison

Cet audit détermine ce qui a changé dans les cartes depuis le dernier état éditorial
du projet de thèse et ce qui doit être répercuté dans les documents de synthèse. Il ne
suppose pas que chaque carte doive entrer dans le manuscrit : le rôle architectural de
la proposition, son degré de stabilisation et sa fonction dans la démonstration restent
décisifs.

Le point de comparaison retenu est le commit `302cfa2` du 8 août 2026,
`Documente les ambiguïtés du mot intéressant`. C'est la dernière modification des
fichiers courants `projet-these-fr.tex` et `projet-these-en.tex`. Elle intègre déjà
`idea_0155` et constitue donc l'état éditorial terminal de fait de la V6.

### Anomalie de versionnement

Les instantanés `versions/projet-these-v6-fr.tex` et
`versions/projet-these-v6-en.tex` ont été créés au commit `6464c98` du 7 août, avant
les derniers enrichissements restés sous le numéro 6. Ils diffèrent aujourd'hui des
sources courantes de respectivement 272 et 260 lignes de diff. Ils ne doivent donc pas
servir seuls de référence complète pour reconstruire la V6 effectivement décrite dans
le changelog.

Décision : ne pas réécrire silencieusement ces instantanés historiques. Pour le présent
audit, `302cfa2` est l'ancre de synchronisation. La prochaine version stabilisée devra
repartir des sources courantes, porter un nouveau numéro et produire simultanément ses
deux instantanés et sa bibliographie archivée.

## Delta des cartes

Quatre propositions autonomes ont été ajoutées depuis l'ancre :

- `idea_0156` — rareté de l'intéressant et coût statistique d'une exploration libre ;
- `idea_0157` — distinction entre médiocrité exploratoire et médiocrité
  d'exploitation ;
- `idea_0158` — articulation entre exploration neuronale en largeur et résolution
  symbolique en profondeur ;
- `idea_0159` — parcimonie tonale, prise compacte et test d'anti-compression.

Douze cartes antérieures ont été précisées par ces propositions ou par les deux papiers
récents : `idea_0016`, `idea_0017`, `idea_0071`, `idea_0074`, `idea_0086`,
`idea_0093`, `idea_0100`, `idea_0105`, `idea_0109`, `idea_0128`, `idea_0140` et
`idea_0151`. Ces modifications induites ne constituent pas douze nouveaux chantiers :
elles se regroupent dans les quatre dossiers ci-dessous.

## Dossiers de rattrapage

| Priorité | Dossier | Cartes principales | Apport depuis la V6 | Destination éditoriale | Décision |
| --- | --- | --- | --- | --- | --- |
| P0 | Intégrité de version | — | Les instantanés V6 ne coïncident pas avec l'état terminal de fait de la V6. | `projet-these/README.md`, changelog, prochain cycle de version | Documenter l'anomalie maintenant ; rétablir la discipline à la prochaine version. |
| P1 | Formalisation réflexive | `0017`, `0128`, `0159` | La substitution de cible peut survenir après une formalisation correcte, lorsqu'une procédure tractable remplace la loi visée ; l'anti-compression fournit un cas positif où cette divergence reste visible. | `BUT_DE_LA_THESE.md`, `STRUCTURE_PROVISOIRE.md`, puis sections formalisation, musique et IA des deux projets | Intégrer dans les synthèses ; réserver la rédaction bilingue à la prochaine version. |
| P1 | Laboratoire musical | `0071`, `0086`, `0151`, `0159` | Distinction entre compacité statique d'une analyse et progrès temporel de compression ; articulation des échelles locale et globale ; cas d'échec informatif. | Section musique de la structure, puis section musique des projets FR/EN | Retenir `0159` comme `CASE`, sans transformer `K` en mesure de l'intéressant. |
| P1 | Laboratoire IA | `0016`, `0017`, `0100`, `0109`, `0158` | Passage d'un simple couplage sampling–contraintes à une boucle où génération, résolution, conflits et reformulation coopèrent. | Section IA de la structure et chantier expérimental, puis section IA des projets FR/EN | Retenir comme hypothèse de laboratoire ; `0158` est classée `TEST`. |
| P2 | Rareté et politique de l'exploration | `0074`, `0093`, `0105`, `0140`, `0156`, `0157` | La faible qualité moyenne peut être un coût de l'exploration ; elle ne doit pas être confondue avec répétition optimisée, concentration de l'exposition ou manipulation causalement établie. | Dossier d'objections et épreuves différentielles ; éventuellement neutralité axiologique | Conserver `0156` en `SPECULATIVE`. Tester ses prémisses avant toute intégration centrale ; `0157` peut entrer comme distinction protectrice si le dossier politique est maintenu. |

## Modifications éditoriales recommandées

### `BUT_DE_LA_THESE.md`

La section « Le risque structurel de substitution de cible » doit recevoir en priorité
deux précisions :

1. distinguer la cible, l'indicateur et la procédure effective ; une cible peut être
   bien définie alors qu'une approximation tractable change les poids ou le support ;
2. présenter la parcimonie tonale comme cas de formalisation réflexive : l'objectif
   fonctionne localement, mais les cas d'anti-compression empêchent de l'identifier à
   la bonne analyse en général.

Cette modification corrige la formulation trop globale d'une « hostilité de la
formalisation ». Le danger mieux identifié est la clôture prématurée de la cible et
l'oubli de la divergence entre cible, indicateur et procédure.

La partie « Neutralité axiologique provisoire » peut recevoir ultérieurement la
distinction exploration/exploitation de `idea_0157`. La thèse statistique plus forte de
`idea_0156` doit rester en réserve tant que la rareté, l'indépendance effective des
essais et les faux négatifs du filtrage n'ont pas été étayés.

### `STRUCTURE_PROVISOIRE.md`

Dans le laboratoire musical, ajouter une fonction argumentative précise pour la
parcimonie tonale : tester si une compression conserve les différences nécessaires aux
anticipations et aux interventions. Dans le laboratoire IA, distinguer deux questions :

- comment une procédure de génération déforme-t-elle la distribution conditionnelle
  qu'elle prétend réaliser ?
- une boucle générateur–solveur peut-elle inventer des représentations qui modifient la
  difficulté pratique du problème, plutôt que seulement choisir de meilleures branches ?

Les cartes `0156` et `0157` ne justifient pas un troisième laboratoire. Elles peuvent
servir d'épreuve courte sur le passage de la description statistique au jugement
politique.

### `PLAN_ACTION_DEMONSTRATION.md`

Le chantier 5 peut rendre les deux laboratoires plus discriminants :

- musique : prendre l'anti-compression comme échec possible d'une prise trop compacte ;
- IA : comparer cible conditionnelle, distribution effectivement générée et pertes de
  support ; comparer transformer seul, solveur seul et boucle hybride ;
- épreuve politique optionnelle : distinguer volume de production, diversité effective
  des directions et concentration de l'exposition.

### Projets français et anglais

Ils ne doivent pas être modifiés carte par carte. Lors de la prochaine version :

1. remplacer le titre « L'hostilité de la formalisation » par une formulation centrée
   sur le risque de substitution de cible ;
2. intégrer ensemble `0017`, `0128` et `0159` afin que l'objection et son cas positif
   restent solidaires ;
3. intégrer `0158` dans le laboratoire IA comme hypothèse expérimentale, sans en faire
   une théorie psychologique de l'intelligence ;
4. décider explicitement si `0156` et `0157` appartiennent à la démonstration principale
   ou à une réserve de recherche ;
5. maintenir l'homologie FR/EN, compiler les deux textes, incrémenter le numéro, écrire
   le changelog et créer les instantanés dans la même opération.

## État de synchronisation au 23 août 2026

- Cartes, index, relations, registre et bibliographie : à jour pour les dossiers
  examinés.
- Catalogue des cartes : régénéré et compilé avec 156 cartes.
- Site statique : régénéré localement avec 156 cartes, 253 relations et 135 références ;
  la publication reste assurée par le workflow GitHub Pages lors d'un push sur `main`.
- `BUT_DE_LA_THESE.md`, `STRUCTURE_PROVISOIRE.md` et `PLAN_ACTION_DEMONSTRATION.md` :
  rattrapage éditorial exécuté.
- Projets FR/EN : lot intégré dans la V7, avec l'hypothèse `0156` explicitement maintenue
  dans la réserve spéculative.
- Instantanés et bibliographie V7 : créés à partir de l'état compilé ; l'ancre Git sera
  le commit qui enregistrera ce lot.

La procédure générale à appliquer lors des prochains changements est décrite dans
[`pipeline-synchronisation-cartes-documents.md`](pipeline-synchronisation-cartes-documents.md).
