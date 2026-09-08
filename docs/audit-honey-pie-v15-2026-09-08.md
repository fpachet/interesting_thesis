# Audit V15 : intégrer Honey Pie sans confondre essai et preuve

## Ancrage et périmètre

État de comparaison : V14 archivée dans le commit `80e1f8b`. La V15 reprend
l'essai court approuvé le 8 septembre 2026 et l'explicitation « comment ça marche ? »
nécessaire à son articulation avec le noyau. Les instantanés antérieurs ne sont pas
modifiés. La présente intégration est locale ; aucun envoi ni déploiement n'est inclus.
Les instantanés V15 constituent l'ancrage documentaire du lot ; son identifiant de
commit pourra être relevé lors de l'enregistrement Git, sans inventer de référence.

## Décisions éditoriales

| Matériau | Impact | Décision et destination |
| --- | --- | --- |
| Essai approuvé dans `docs/notes/honey-pie-jotney.md` | D2 | Intégrer dans la section musicale, sous-section « Honey Pie : une note qui fait question », avec traduction homologue. |
| `idea_0111` : régime Jotney constructif | D1 | Relier au cas concret, sans confondre organisation de l'objet et intérêt éprouvé. |
| `idea_0118` et `idea_0123` : appréciation / « comment ça marche ? » | D1 | Intégrer à la définition un paragraphe bilingue et un renvoi au cas ; conserver la possibilité d'une question tacite. |
| Réduction notée | D0 | Conserver dans le dossier ; ne pas la présenter comme la transcription exacte du morceau ni comme une partition publiée. |
| Références de Blick et Pollack | D0 | Ajouter à la bibliographie canonique et aux deux textes ; conserver les limites de vérification dans la note. |
| Revue générale et plan de rédaction | Organisation | Maintenir les documents de travail, sans présenter les difficultés conceptuelles comme résolues par l'essai. |

## Ce qui est acquis et ce qui reste ouvert

L'essai français est conservé, avec seulement les adaptations typographiques et
les références nécessaires à son insertion. La version anglaise reprend les mêmes
étapes, réserves et sources. Une brève clôture dans les deux langues précise le
rapport au livre antérieur et le statut non expérimental du parcours.

Il reste à fixer l'audio de référence, vérifier une transcription fidèle, décrire
les opérations effectivement accomplies et comparer les variantes. La question
de savoir si une construction sans intérêt met en défaut la définition n'est pas
réglée par l'affirmation plus faible qu'un savoir analytique ne suffit pas.
La révision générale du flow, les autres objections et le changement éventuel
du plan public demeurent hors du présent lot.

## Contrôles du lot

- Compilation des projets français et anglais et contrôle visuel des pages touchées.
- Vérification des citations, des renvois et de l'homologie des sections ajoutées.
- Régénération du catalogue et contrôle du site généré localement.
- Comparaison exacte des deux sources et de la bibliographie avec leurs instantanés V15.
- Pas de modification des archives V1 à V14 ni de la version courte administrative.
