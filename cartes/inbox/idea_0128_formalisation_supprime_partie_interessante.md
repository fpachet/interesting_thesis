---
id: idea_0128
title: "Toute formalisation risque de substituer son indicateur à la cible"
kind: objection
level: articulation
status: inbox
architecture: core
sources:
  - "input/Russell_Rationality_and_Intelligence_IJCAI95.pdf"
  - "input/Pachet_Representation_connaissances_langages_objets_1997.pdf"
  - "input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf"
  - "input/Tonal_Parsimony_in_Chord_Sequence_Analysis.pdf"
references:
  - russell1995awardlecture
  - russell1995rationality
  - pachet1997representation
  - pachet2026biases
  - pachet2026tonalparsimony
source_notes:
  - "Russell, Rationality and Intelligence, IJCAI-95, p. 950 : danger de premature mathematization, lorsque des résultats de plus en plus techniques s'éloignent du problème initial."
  - "Russell, allocution Rationality and Intelligence pour le Computers and Thought Award, IJCAI-95 : source intellectuelle de l'avertissement oral sur les parties intéressantes définies hors du problème."
  - "Pachet, Représentation de connaissances et langages à objets, HDR 1997, PDF p. 10 : source écrite qui conserve la transcription de cette allocution."
  - "L'allocution, l'article des actes et le mémoire d'HDR sont cités séparément : la citation longue est attestée par le mémoire et ne figure pas textuellement dans l'article."
  - "L'écart entre la transcription orale et l'article publié est mobilisé comme exemple réflexif de normalisation ; il ne permet pas à lui seul d'établir les intentions de Russell ni l'histoire éditoriale du texte."
  - "Hidden Biases : version longue de 16 pages soumise à NeurIPS, p. 1-14 ; distinction entre la distribution conditionnelle visée et la distribution effectivement produite par une procédure tractable. La version publique arXiv:2604.07855v1 compte 9 pages."
  - "Tonal Parsimony, arXiv:2606.03459v1, section 8.3 : deux cas d'anti-compression où la minimisation de C puis K efface une distinction tonale attendue ; le papier identifie explicitement ces échecs comme limites de l'objectif ou du modèle local."
tags:
  - formalisation
  - ia
  - generation
  - syntaxe
  - objectif
  - russell
  - methode
  - substitution-de-cible
---
## Idée

Il faut prendre au sérieux le **risque structurel de substitution de cible**. Ce risque
n'est ni une intention des chercheurs, ni une impossibilité de principe. Pour rendre un
problème testable et cumulatif, la science doit le traduire en objets définis,
variables contrôlables et critères calculables. La difficulté apparaît lorsque cette
traduction est traitée comme la définition complète du phénomène : l'indicateur peut
alors remplacer la cible et éliminer son caractère relationnel, historique, singulier et
transformateur.

La réussite sur le problème formel ne garantit donc plus un progrès sur le problème
initial. Elle peut au contraire rendre invisible le fait que l'objet de recherche a
changé pendant sa formalisation.

Russell nomme **mathématisation prématurée** la production de résultats toujours plus
techniques et toujours moins liés au problème original de l'intelligence. Dans
l'allocution conservée par Pachet, il décrit plus brutalement le risque qu'un problème
formel remplace le problème informel et que « the interesting parts have been defined
away ». La formalisation n'a pas seulement simplifié le problème : elle a déclaré hors
du problème ce qui résistait à sa définition.

## Un exemple réflexif : de l'oral à l'écrit

La différence entre l'allocution retranscrite par Pachet et l'article publié est
elle-même un exemple possible de cette substitution. À l'oral, Russell nomme directement
le danger : un problème formel remplace un problème informel, ses parties intéressantes
sont définies hors du champ et les solutions deviennent inintéressantes. Dans les actes,
la mise en garde subsiste, mais sous la catégorie plus abstraite de **mathématisation
prématurée** : des résultats toujours plus techniques s'éloignent du problème original.

Le passage à l'écrit conserve donc la structure logique de l'avertissement tout en
faisant disparaître son vocabulaire le plus incisif : l'intéressant, l'inintéressant et
les problèmes réels. La transformation d'une parole située en texte scientifique
publiable semble ainsi filtrer précisément la dimension que cette parole cherchait à
protéger.

Cet écart ne prouve ni une autocensure de Russell, ni une intervention éditoriale
déterminée. Il constitue un objet d'analyse : les exigences de définition, de
précision et de recevabilité propres au genre scientifique peuvent neutraliser une
formulation sans réfuter ce qu'elle désignait. La rédaction de cette thèse devra
elle-même surveiller ce risque.

Ce risque est particulièrement fort pour les systèmes génératifs. L'objectif initial,
« produire une forme intéressante », tend à être remplacé par des objectifs mieux
définis :

- produire une forme syntaxiquement correcte ;
- produire une forme sémantiquement interprétable ou cohérente ;
- imiter la distribution d'un corpus ;
- satisfaire un ensemble explicite de contraintes ;
- maximiser une préférence, une vraisemblance ou un score disponible.

Ces propriétés sont utiles et parfois nécessaires. Aucune n'implique cependant que la
forme produite déclenche une construction, déplace l'attention ou acquière une
singularité pour un sujet. Un système peut donc résoudre brillamment le substitut
formel tout en produisant des résultats fluides, corrects et dépourvus d'intérêt.

## Une panoplie redoutable

La science dispose d'une **panoplie redoutable pour lutter contre cet objectif**, alors
même que chacun de ses instruments est légitime et fécond dans d'autres enquêtes :

- la définition opératoire remplace une notion ouverte par ce qui peut être mesuré ;
- la décomposition isole des facteurs et affaiblit les relations qui les constituent ;
- le contrôle des variables neutralise l'histoire propre du sujet et de l'objet ;
- la répétabilité privilégie les effets stables au détriment des transformations
  irréversibles ;
- la normalisation et les moyennes effacent les singularités et les trajectoires ;
- le benchmark fige une tâche, un corpus et une mesure de réussite ;
- l'optimisation exploite l'indicateur retenu, y compris lorsqu'il diverge de la cible.

Appliquée à l'intéressant, cette panoplie ne produit pas seulement une approximation
imparfaite. Elle exerce une pression convergente pour rabattre le phénomène sur ce qui
est déjà défini, comparable et optimisable. Autrement dit, elle risque de rendre
scientifique le substitut précisément en expulsant l'intéressant. Ce risque n'est pas
une propriété de toute formalisation : il naît de la clôture prématurée de la cible.

## Distinction

La difficulté ne vient pas de toute formalisation, mais de la **clôture prématurée du
critère**. Une formalisation féconde explicite ce qu'elle mesure, conserve la différence
entre la cible et son indicateur, et retourne vers les cas où les deux divergent. Une
formalisation liquidatrice rebaptise son indicateur comme s'il était la cible elle-même,
puis traite les dimensions restantes comme subjectives, anecdotiques ou extérieures au
problème.

*Hidden Biases* ajoute une distinction importante : la substitution peut intervenir
après que la cible a été correctement formalisée. La loi conditionnelle exacte demeure
explicite, mais son calcul étant difficile, une procédure locale ou heuristique produit
en pratique une autre loi, parfois même sur un support plus étroit. La chaîne causale
est alors : cible formelle, pression de tractabilité, procédure approchée, oubli de la
divergence. Le danger ne vient donc pas de la formalisation seule ; il vient aussi du
moment où l'approximation opératoire cesse d'être reconnue comme telle.

La parcimonie tonale fournit un contrepoint positif précis. Elle minimise d'abord les
modulations, puis le nombre de tonalités distinctes d'une analyse harmonique. Dans la
majorité des cas où elle change ce second critère, la compression résout utilement une
indétermination de l'analyse. Mais deux cas d'anti-compression sont conservés comme
échecs informatifs : l'optimum absorbe une région mineure dans sa relative majeure ou
fusionne des toniques locales intentionnellement distinctes. La fonction objectif n'est
donc pas rebaptisée « bonne analyse » ; ses divergences indiquent le besoin de preuves
fonctionnelles locales ou de pondérations supplémentaires. Cette pratique réalise la
formalisation réflexive demandée ici : optimiser un indicateur, puis retourner vers les
résidus où il cesse de préserver la cible.

L'intéressant résiste particulièrement à cette clôture parce qu'il est relationnel,
historique et transformateur : le sujet, ses compétences et l'espace des possibilités
changent pendant l'interaction. Fixer une fonction objectif peut donc immobiliser ce que
la théorie cherche précisément à décrire.

## Critère

On peut demander à toute formalisation de l'intéressant :

1. quels cas intéressants sa définition exclut-elle par construction ?
2. quels cas inintéressants son indicateur récompense-t-il ?
3. quelles dimensions de la relation sujet-objet ont été transformées en constantes ?
4. quel résultat empirique obligerait à réviser le problème formel plutôt que seulement
   l'algorithme qui tente de le résoudre ?

Si ces questions n'ont pas de réponse, le système risque de mesurer sa conformité à une
définition plutôt que sa capacité à produire ou expliquer de l'intéressant.

## Intérêt pour la thèse

Cette objection donne une fonction critique à la thèse. Étudier l'intéressant ne consiste
pas seulement à proposer un nouveau score pour les systèmes génératifs, mais à examiner
ce que les formalismes existants ont rendu invisible en remplaçant la valeur recherchée
par la correction, la cohérence, la probabilité ou la satisfaction de contraintes.

La thèse doit ainsi étudier cette substitution comme un problème positif de méthode :
comment construire des instruments scientifiques qui ne détruisent pas leur objet en le
rendant mesurable ? La réponse ne peut être un refus de la formalisation, mais une
formalisation réflexive, locale et révisable, capable de conserver ses résidus et ses
contre-exemples.

Elle impose aussi une méthode ascendante : partir des divergences entre résultats
formellement réussis et expériences effectivement intéressantes, puis construire des
modèles locaux et révisables. Le résidu n'est pas un échec provisoire à éliminer ; il
peut contenir le phénomène même que la formalisation devait préserver.

## Liens

- Radicalise `idea_0088` : le modèle peut non seulement ne pas épuiser son objet, mais remplacer celui-ci par un substitut plus commode.
- Généralise `idea_0098`, où la correction syntaxique ne distingue pas les solutions musicales intéressantes.
- Soutient la troisième couche de `idea_0003`, irréductible à la syntaxe et au sens.
- Complète `idea_0095` : un modèle peut échouer par excès de généralité ou par réduction excessive de sa cible.
- Fournit une objection interne aux programmes formels de `idea_0119` et `idea_0120`.
- Trouve dans `idea_0159` un cas positif de formalisation qui documente ses propres échecs d'anti-compression au lieu de les exclure du problème.
- Est précisée par `idea_0017`, où une procédure de génération tractable peut substituer sa loi effective à une cible conditionnelle pourtant bien définie.
