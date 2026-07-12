---
id: idea_0072
title: "La curiosité aide surtout lorsque la récompense externe est rare"
kind: hypothesis
level: scientific
status: inbox
sources:
  - "input/old_docs/interestingness.pdf"
references:
  - schmidhuber1997interesting
source_notes:
  - "Schmidhuber, What's Interesting?, PDF p. 3 et 13-17 ; limites p. 20-21"
tags:
  - schmidhuber
  - curiosite
  - exploration
  - apprentissage
  - recompense
---
## Idée

Une récompense interne pour la découverte de régularités peut accélérer l'apprentissage
orienté vers un but lorsque les récompenses externes sont trop rares pour guider
efficacement l'exploration. Mais cet avantage n'est pas universel : lorsque le but
externe fournit déjà beaucoup de signal, la curiosité peut détourner du perfectionnement
de la politique utile et devenir coûteuse.

Les simulations de Schmidhuber soutiennent cette hypothèse de façon nuancée : le système
curieux trouve d'abord plus vite la récompense externe, puis son avantage disparaît avec
l'accumulation des exemples orientés vers le but. La curiosité n'est donc pas posée
comme une vertu absolue, mais comme une stratégie dont la valeur dépend du régime de
rareté du signal externe.

Dans l'expérience 2a, les résultats moyens du système curieux dépassent fortement ceux
du système sans récompense interne, mais un essai curieux ne trouve jamais le but. Dans
l'expérience 2b, l'avantage initial disparaît après un apprentissage plus long et le
système non curieux finit même légèrement devant. Le papier présente ces résultats comme
exploratoires et ne prétend pas établir une loi générale.

## Intérêt pour la thèse

Cette proposition relie une théorie de l'intéressant à une fonction pratique :
l'intéressant peut servir de guide provisoire lorsqu'aucun objectif externe ne donne
encore de direction suffisante. Elle fournit aussi une limite testable aux discours qui
identifient curiosité et performance.

## Liens

- `idea_0027` fournit le signal interne qui rend cette exploration possible.
- à rapprocher de `idea_0012` sur le doodling comme exploration peu dirigée.
