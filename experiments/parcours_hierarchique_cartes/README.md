# Parcours hiérarchique des cartes

Cette activité est une expérience dérivée et isolée. Elle lit les sources canoniques
du catalogue, mais ne modifie ni les cartes, ni les index, ni le graphe existant.
Tous ses résultats sont écrits dans `generated/`, qui est ignoré par Git.

## Principe

Le calcul utilise les rubriques de cartes `CORE` dans
`cartes/indexes/by_architecture.md` comme chapitres provisoires. Il :

1. calcule quatre distances complètes entre les cartes : texte TF-IDF, tags, famille
   argumentative et proximité dans le graphe éditorial existant ;
2. combine ces distances avec les relations explicites du catalogue ;
3. trouve exactement le chemin de coût minimal entre les `CORE`, en conservant l'ordre
   des chapitres mais en optimisant l'ordre interne de chacun ;
4. rattache chaque autre carte à un `CORE` principal et à plusieurs ancrages secondaires ;
5. propose dans chaque chapitre un ordre local qui conserve l'ordre des `CORE` ;
6. signale sans les modifier les cartes dont le statut architectural reste à classer.

Le résultat est une proposition de lecture et un diagnostic, pas un plan éditorial
automatiquement validé. La composante textuelle est volontairement locale et
reproductible ; la composante de graphe réutilise seulement les liens déjà édités. Cet
ensemble constitue une ligne de base que l'on pourra comparer plus tard à des embeddings
ou à des jugements de transition argumentatifs.

## Relancer après une mise à jour du catalogue

Depuis la racine du dépôt :

```bash
python3 experiments/parcours_hierarchique_cartes/parcours.py
```

Le dossier `generated/` reçoit :

- `parcours.md` : rapport lisible, colonne vertébrale et chapitres ;
- `parcours.json` : résultat structuré pour une future interface ;
- `distances.tsv` : matrice complète sous forme de paires non orientées.

La question, la conclusion, les poids et les bonus sont réglables dans `config.json`.

## Vérifier l'activité

```bash
python3 -m unittest discover \
  -s experiments/parcours_hierarchique_cartes \
  -p 'test_*.py'
```

L'activité n'ajoute aucune dépendance au projet : elle utilise seulement la bibliothèque
standard de Python 3.11.
