# Cartes d'idees

Ce dossier sert de boite de reception pour les idees extraites du corpus.

Le principe est volontairement simple :

- une carte = une idee manipulable ;
- les cartes commencent dans `inbox/` avec le statut `inbox` ;
- le registre indique quels documents ont ete lus, partiellement lus, ou seulement inventories ;
- l'organisation fine vient plus tard, dans les index et dans un futur plan de these.

## Cycle de travail

1. Lire ou relire un document source.
2. Extraire les idees principales sous forme de cartes courtes.
3. Noter dans `REGISTRE_TRAITEMENT.md` le niveau de traitement du document.
4. Ajouter les cartes aux index thematiques si un regroupement devient evident.
5. Ne pas forcer trop tot un plan lineaire : laisser les familles emerger.

## Format d'une carte

Chaque carte utilise un en-tete YAML minimal :

```md
---
id: idea_0001
title: "Titre court"
kind: argument
status: inbox
sources:
  - "chemin/document.pdf"
tags:
  - interessant
---
```

Les champs `kind` possibles pour l'instant : `definition`, `argument`, `objection`, `example`, `distinction`, `method`, `question`, `hypothesis`, `bibliographic_note`.
