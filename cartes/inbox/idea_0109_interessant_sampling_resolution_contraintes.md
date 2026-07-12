---
id: idea_0109
title: "Produire de l'interessant exige souvent d'articuler sampling et resolution de contraintes"
kind: hypothesis
level: articulation
status: inbox
sources:
  - "input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf"
  - "input/Notes thèse.pdf"
  - "input/ERCGrantPachetInterestingness.pdf"
source_notes:
  - "Hidden Biases, insuffisance du sampling local pour les proprietes globales, PDF p. 1-3 et 10-14"
  - "Notes these, doodling comme echantillonnage peu contraint, PDF p. 1"
  - "ERC Grant, objet comme solution rare, harmonisations legales et exploration combinatoire, PDF p. 4-6"
tags:
  - interessant
  - sampling
  - contraintes
  - resolution_de_problemes
  - generation
---

## Idee

Produire un objet interessant demande souvent deux operations heterogenes. Le
sampling en marche avant ouvre des possibles en prolongeant localement un materiau,
sans exiger qu'un but complet soit connu. La resolution de contraintes traite au
contraire chaque choix comme une etape d'un probleme global : elle verifie les
continuations, revient en arriere, repare ou selectionne les chemins encore
compatibles avec une forme a atteindre.

Chacune echoue seule d'une maniere caracteristique. Le sampling pur peut produire
une suite d'evenements localement plausibles mais incapable d'aboutir a une fin, un
metre ou une organisation globale. Le solveur pur peut enumerer toutes les
solutions legales sans savoir lesquelles sont singulieres ou interessantes. La
generation de l'interessant exige alors leur articulation : proposer du materiau,
faire apparaitre ou imposer un probleme, tester les contraintes, puis relancer la
generation depuis ce que la resolution a rendu possible.

Cette articulation n'impose pas toujours un plan anterieur a la production. Dans
le doodling, le sampling peut faire apparaitre apres coup la forme ou le probleme
qui orientera les etapes suivantes. Ailleurs, une contrainte explicite precede le
premier geste. L'hypothese porte sur la cooperation des deux regimes, pas sur leur
ordre fixe ni sur tous les cas possibles de l'interessant.

## Statut de la source

Cette carte est une synthese pour la these, non une conclusion explicite de
`Hidden Biases`. Ce papier etablit la tension computationnelle entre sampling
autoregressif local et contraintes globales. Les notes sur le doodling et le grant
ERC fournissent le lien proprement dit avec la production de formes interessantes.

## Interet pour la these

La proposition donne un mecanisme commun a l'exploration sans but, au sens de la
direction et a l'objet percu comme solution rare. Elle suggere aussi une architecture
experimentale : comparer sampling seul, resolution seule et boucle hybride, puis
mesurer la diversite, la legalite et l'interet des objets obtenus.

## Liens

- Articule l'echantillonnage de `idea_0012` avec la resolution implicite de `idea_0096`.
- `idea_0017` explique pourquoi un simple sampling conditionne ne realise pas cette articulation exactement.
- `idea_0098` montre l'echec symetrique d'un solveur qui ne produit que des solutions legales.
- `idea_0100` precise quand le couplage modele-contrainte peut etre calcule exactement.
