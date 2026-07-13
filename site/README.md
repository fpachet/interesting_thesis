# Site de suivi de la thèse

Ce dossier contient l'interface publique du projet. Le site est entièrement généré
depuis les documents canoniques du dépôt : cartes Markdown, index argumentatifs,
relations typées, bibliographie BibTeX, corpus documentaire, but de la thèse,
questions ouvertes et registre de traitement.

Il ne constitue donc pas une seconde source éditoriale. Toute modification d'une carte
ou de l'organisation apparaît au prochain build.

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
- un catalogue des 121 cartes avec recherche et filtres ;
- une fiche complète pour chaque carte, avec provenance et relations ;
- une bibliographie recherchable, avec notices détaillées, documents publics et
  navigation bidirectionnelle entre références et propositions ;
- un graphe interactif limité aux relations fortes ;
- un tableau de suivi avec couverture du corpus, couverture bibliographique,
  questions ouvertes et historique Git.

## Publication

Le site est statique et ne requiert ni base de données ni serveur applicatif. Le dossier
`site/dist/` peut être publié tel quel par GitHub Pages, Netlify ou tout hébergeur de
fichiers statiques. En production, la commande de génération doit être exécutée après
chaque modification du corpus. Les fichiers de `input/` sont copiés sous
`documents/input/` afin que les provenances indiquées sur les cartes soient
directement consultables.
