---
id: idea_0109
title: "Produire de l'intéressant exige souvent d'articuler sampling et résolution de contraintes"
kind: hypothesis
level: articulation
status: inbox
sources:
  - "input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf"
  - "input/Notes thèse.pdf"
  - "input/ERCGrantPachetInterestingness.pdf"
  - "input/old_docs/interestingness/fp perso/fdp/Papiers/Future of Music book/interestingness/Dan Gang/aaai99A.pdf"
  - "input/old_docs/interestingness/fp perso/fdp/Papiers/Future of Music book/interestingness/Dan Gang/netneg.pdf"
  - "input/publications-francois-pachet/pachet-09c.pdf"
  - "input/publications-francois-pachet/barbieri-12a.pdf"
  - "input/publications-francois-pachet/roy-16b.pdf"
  - "input/publications-francois-pachet/pachet12b.pdf"
references:
  - pachet2026biases
  - goldman1999netneg
  - pachet2011markov
  - barbieri2012lyrics
  - papadopoulos2016flowcomposer
  - pachet2012virtuosity
source_notes:
  - "Hidden Biases : version longue de 16 pages soumise à NeurIPS ; la version publique arXiv:2604.07855v1 compte 9 pages."
  - "Hidden Biases, insuffisance du sampling local pour les propriétés globales, PDF p. 1-3 et 10-14"
  - "Notes thèse, doodling comme échantillonnage peu contraint, PDF p. 1"
  - "ERC Grant, objet comme solution rare, harmonisations légales et exploration combinatoire, PDF p. 4-6"
  - "NetNeg, prédictions du réseau négociées avec les contraintes de contrepoint, PDF p. 3-6"
  - "NetNeg développe, architecture et comparaison des modules, PDF p. 9-18"
  - "Markov Constraints, PDF p. 1-8 et 21-23 : inversion de generate-and-test, recherche globale de séquences à faible probabilité et contrôle arbitraire."
  - "Markov Constraints for Lyrics, PDF p. 1-5 : comparaison empirique entre Markov pur, contraintes pures et processus markovien contraint."
  - "Assisted Lead Sheet Composition, PDF p. 1-8 et 13-15 : échantillonnage de chaînes markoviennes sous contraintes métriques, harmoniques et utilisateur dans un outil de composition."
  - "Bebop Virtuosity Explained, PDF p. 13-14 et 25-33 : texture markovienne, transformations, contraintes globales et partition intentionnelle au niveau du temps musical."
tags:
  - interessant
  - sampling
  - contraintes
  - resolution_de_problemes
  - generation
---
## Idée

Produire un objet intéressant demande souvent deux opérations hétérogènes. Le sampling
en marche avant ouvre des possibles en prolongeant localement un matériau, sans exiger
qu'un but complet soit connu. La résolution de contraintes traite au contraire chaque
choix comme une étape d'un problème global : elle vérifie les continuations, revient en
arrière, répare ou sélectionne les chemins encore compatibles avec une forme à
atteindre.

Chacune échoue seule d'une manière caractéristique. Le sampling pur peut produire une
suite d'événements localement plausibles mais incapable d'aboutir à une fin, un mètre ou
une organisation globale. Le solveur pur peut énumérer toutes les solutions légales sans
savoir lesquelles sont singulières ou intéressantes. La génération de l'intéressant
exige alors leur articulation : proposer du matériau, faire apparaître ou imposer un
problème, tester les contraintes, puis relancer la génération depuis ce que la
résolution a rendu possible.

Cette articulation n'impose pas toujours un plan antérieur à la production. Dans le
doodling, le sampling peut faire apparaître après coup la forme ou le problème qui
orientera les étapes suivantes. Ailleurs, une contrainte explicite précède le premier
geste. L'hypothèse porte sur la coopération des deux régimes, pas sur leur ordre fixe ni
sur tous les cas possibles de l'intéressant.

NetNeg fournit un précédent scientifique concret : chaque réseau neuronal émet une
distribution de prochains sons et les agents cherchent ensuite une paire qui maximise
les préférences apprises tout en respectant les contraintes du contrepoint. Le résultat
retenu est réinjecté comme nouveau contexte. Le système ne démontre pas une théorie
générale de l'intéressant, mais il réalise déjà la boucle proposition, négociation,
contrainte et relance décrite ici.

Les travaux ultérieurs sur les contraintes de Markov rendent ce couplage systématique.
Ils inversent le generate-and-test : l'espace des contraintes est exploré globalement,
tandis que la probabilité stylistique ordonne ou échantillonne les solutions. Les
expériences sur les paroles puis FlowComposer montrent que le couplage vaut comme
architecture générale — style local plus forme globale — sans que sa réussite technique
garantisse à elle seule l'intérêt du résultat.

Le chapitre sur la virtuosité bebop donne à cette architecture une interprétation
musicale plus fine. Le processus markovien y produit une texture locale plutôt que des
idées ; les décisions de haut niveau forment une « partition intentionnelle » qui
pilote contour, chromatisme, continuité et ruptures. Ce cas montre comment le sampling
et les contraintes peuvent aussi distribuer l'intention entre plusieurs échelles.

## Statut de la source

Cette carte est une synthèse pour la thèse, non une conclusion explicite de `Hidden
Biases`. Ce papier établit la tension computationnelle entre sampling autoregressif
local et contraintes globales. Les notes sur le doodling et le grant ERC fournissent le
lien proprement dit avec la production de formes intéressantes. NetNeg constitue une
construction scientifique antécédente que la thèse peut réinterpréter, sans lui
attribuer cette généralisation philosophique.

## Intérêt pour la thèse

La proposition donne un mécanisme commun à l'exploration sans but, au sens de la
direction et à l'objet perçu comme solution rare. Elle suggère aussi une architecture
expérimentale : comparer sampling seul, résolution seule et boucle hybride, puis mesurer
la diversité, la légalité et l'intérêt des objets obtenus.

## Liens

- Articule l'échantillonnage de `idea_0012` avec la résolution implicite de `idea_0096`.
- `idea_0017` explique pourquoi un simple sampling conditionne ne réalise pas cette articulation exactement.
- `idea_0098` montre l'échec symétrique d'un solveur qui ne produit que des solutions légales.
- `idea_0100` précise quand le couplage modèle-contrainte peut être calcule exactement.
