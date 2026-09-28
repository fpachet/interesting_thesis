# Site de suivi de la thèse

Ce dossier contient l'interface publique du projet. Le site est entièrement généré
depuis les documents canoniques du dépôt : cartes Markdown, index argumentatifs,
relations typées, bibliographie BibTeX, corpus documentaire et registre de traitement.
La définition et la question directrice viennent de la
[Défense](../docs/defense-concept-interessant.md), les questions de travail du
[plan d'action](../projet-these/PLAN_ACTION_DEMONSTRATION.md), et le numéro de version
du projet français. Le site ne dépend plus du but ou de l'organisation conservés en référence.

Les cartes et ces extraits sont actualisés au prochain build, sans seconde saisie.
Les autres textes de présentation codés dans le générateur et le PDF court ne sont
pas automatiquement réécrits. Le catalogue HTML des cartes reste actif, distinct
du catalogue PDF désormais archivé.

La règle des trois documents actifs et des vues dérivées est décrite dans le
[`pipeline de synchronisation`](../docs/pipeline-synchronisation-cartes-documents.md).

## Génération

Depuis la racine du dépôt :

```bash
python3 scripts/generate_thesis_site.py
```

Le résultat est écrit dans `site/dist/`. Pour le consulter localement :

```bash
python3 -m http.server 8040 -d site/dist
```

Puis ouvrir <http://127.0.0.1:8040/>.

Un autre dossier de sortie peut être indiqué :

```bash
python3 scripts/generate_thesis_site.py --output /tmp/interesting-thesis-site
```

## Vues proposées

- une page d'accueil destinée aux personnes qui suivent la thèse ;
- une présentation de l'objet, de l'hypothèse centrale et de sa méthode ;
- un lien vers la version française courte du projet de thèse en PDF ;
- un programme de lecture en dix séances avec questions de travail, statut des
  sources et liens d'accès public vérifiés ;
- un catalogue des 164 cartes avec recherche et filtres ;
- une fiche complète pour chaque carte, avec provenance et relations ;
- une bibliographie recherchable, avec notices détaillées, documents publics et
  navigation bidirectionnelle entre références et propositions ;
- un graphe interactif limité aux relations fortes ;
- un tableau de suivi avec couverture du corpus, couverture bibliographique,
  questions ouvertes et historique Git.

## Publication

Le site est statique et ne requiert ni base de données ni serveur applicatif. Le dossier
`site/dist/` peut être publié tel quel par GitHub Pages, Netlify ou tout hébergeur de
fichiers statiques.

Sur ce dépôt, `.github/workflows/deploy-site.yml` automatise la publication : chaque
push sur `main` régénère `site/dist/`, prépare l'artefact GitHub Pages puis le déploie.
Le workflow peut aussi être lancé manuellement avec `workflow_dispatch`. Il n'est donc
pas nécessaire de versionner `site/dist/`.

Les fichiers disponibles dans `input/` sont copiés sous `documents/input/` pendant la
génération. Lorsqu'un fichier local n'est pas versionné, le générateur utilise l'URL
publique de sa notice bibliographique. Une provenance sans fichier ni URL reste
affichée comme telle, sans bloquer la publication du site.
