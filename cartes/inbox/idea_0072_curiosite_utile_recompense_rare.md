---
id: idea_0072
title: "La curiosite aide surtout lorsque la recompense externe est rare"
kind: hypothesis
level: scientific
status: inbox
sources:
  - "input/old_docs/interestingness.pdf"
source_notes:
  - "Schmidhuber, What's Interesting?, PDF p. 3 et 13-17 ; limites p. 20-21"
tags:
  - schmidhuber
  - curiosite
  - exploration
  - apprentissage
  - recompense
---

## Idee

Une recompense interne pour la decouverte de regularites peut accelerer
l'apprentissage oriente vers un but lorsque les recompenses externes sont trop
rares pour guider efficacement l'exploration. Mais cet avantage n'est pas
universel : lorsque le but externe fournit deja beaucoup de signal, la curiosite
peut detourner du perfectionnement de la politique utile et devenir couteuse.

Les simulations de Schmidhuber soutiennent cette hypothese de facon nuancee : le
systeme curieux trouve d'abord plus vite la recompense externe, puis son avantage
disparait avec l'accumulation des exemples orientes vers le but. La curiosite n'est
donc pas posee comme une vertu absolue, mais comme une strategie dont la valeur
depend du regime de rarete du signal externe.

Dans l'experience 2a, les resultats moyens du systeme curieux depassent fortement
ceux du systeme sans recompense interne, mais un essai curieux ne trouve jamais le
but. Dans l'experience 2b, l'avantage initial disparait apres un apprentissage plus
long et le systeme non curieux finit meme legerement devant. Le papier presente ces
resultats comme exploratoires et ne pretend pas etablir une loi generale.

## Interet pour la these

Cette proposition relie une theorie de l'interessant a une fonction pratique :
l'interessant peut servir de guide provisoire lorsqu'aucun objectif externe ne
donne encore de direction suffisante. Elle fournit aussi une limite testable aux
discours qui identifient curiosite et performance.

## Liens

- `idea_0027` fournit le signal interne qui rend cette exploration possible.
- A rapprocher de `idea_0012` sur le doodling comme exploration peu dirigee.
