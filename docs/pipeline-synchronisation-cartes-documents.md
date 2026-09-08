# Mode de travail : trois documents actifs

> **Règle adoptée le 8 septembre 2026.** Ce texte remplace l'ancien pipeline de
> propagation systématique. Il documente l'organisation ; ce n'est pas un quatrième
> document de contenu à mettre à jour après chaque échange.

## Où écrire ?

| Document actif | Responsabilité | Quand le modifier |
| --- | --- | --- |
| [Définition et défense](defense-concept-interessant.md) | Définition courante, arguments, objections et cas développés | Une idée ou une analyse fait progresser ou corrige le contenu de la thèse |
| [Plan d'action](../projet-these/PLAN_ACTION_DEMONSTRATION.md) | Décisions, architecture de travail, état des livrables, prochaine étape | Une décision change le travail à faire ou son état |
| [Projet français](../projet-these/projet-these-fr.tex) | Présentation synthétique destinée à un lecteur | Un lot argumenté mérite une nouvelle version de présentation |

Ces documents ont des fonctions distinctes : la Défense fait autorité sur le contenu
conceptuel courant ; le plan sur les décisions et le travail restant ; le projet
français sur la dernière présentation rédigée. Une différence de maturité ou de date
est signalée, pas masquée par une copie automatique. En septembre 2026, la Défense
contient des développements post-V15 que le projet bilingue n'intègre pas encore.

## Les cartes restent l'atelier

Les cartes conservent les propositions indépendantes et leurs provenances. Un exemple,
une précision ou une objection locale enrichit d'abord la carte concernée ; il n'impose
pas une nouvelle carte. Si la proposition centrale évolue, son relais `idea_0123`
doit rester cohérent avec la Défense.

Les index et `relations.tsv` ne changent que si les titres, les affectations ou les
relations changent. La bibliographie ne change que pour une référence ajoutée ou corrigée.
Ce sont des données de soutien, pas des synthèses concurrentes.

Le registre de traitement et la couverture sont mis à jour lorsqu'une lecture ou une
extraction a réellement eu lieu. L'audit des propositions conserve les fusions,
retraits et décisions de classement qui demandent une trace. Une simple reformulation
ne justifie pas un nouvel audit narratif.

## Documents conservés comme références

Le [but](../projet-these/BUT_DE_LA_THESE.md), la
[structure provisoire](../projet-these/STRUCTURE_PROVISOIRE.md),
l'[organisation des cartes](../cartes/ORGANISATION.md) et la
[matrice](matrice-tests-interessant.md) sont conservés avec un bandeau de statut.
Ils ne sont plus des passages obligés de la synchronisation et ne définissent plus
séparément la position courante. Leur contenu n'est ni supprimé ni tenu pour validé.

Une étude comparative ciblée peut justifier une nouvelle révision de la matrice :
ce sera un travail explicite, daté, dont la conclusion rejoindra la Défense. Les
notes de lecture, sources, témoignages et anciens audits restent consultables comme
matériaux et traces ; on ne les réécrit pas pour les aligner sur une conclusion récente.

## Adaptations et versions

Le français est la source éditoriale du projet de présentation. L'anglais est adapté
lors de la préparation d'une version bilingue ; les versions diffusées et leurs
instantanés doivent avoir les mêmes sections, hypothèses, citations et numéro.
La version courte est adaptée pour un besoin de présentation ou de dossier.

Une version nommée enregistre un progrès identifiable, pas chaque échange. Compiler
et relire les rendus concernés, renseigner le changelog, puis conserver les sources
et la bibliographie correspondantes dans `projet-these/versions/`. Ne jamais corriger
silencieusement les instantanés historiques. Une publication ou un envoi reste une
action distincte de la préparation locale.

## Catalogue et site : des vues, pas des sources

Le [catalogue au 8 septembre 2026](../archives/catalogue-idees/2026-09-08/README.md)
est archivé avec son PDF, son LaTeX et la bibliographie utilisée. Il est figé :
modifier les cartes n'impose plus de le régénérer. Si un nouvel export est demandé,
le générateur écrit par défaut dans `output/catalogue-idees.tex`, sans toucher
à l'archive.

Le site continue de proposer un catalogue navigable des cartes actuelles. Sa définition
et sa question directrice sont extraites de la Défense ; ses questions de travail
du plan ; son numéro de version du projet français. Un build actualise ces vues.
Il n'actualise pas automatiquement les développements de présentation codés dans
le générateur, ni les PDF de présentation. Pas de publication automatique à la suite
d'un simple échange ; le déploiement GitHub Pages reste déclenché par un push sur main.

## Boucle de travail minimale

1. Travailler un problème déterminé et rédiger le résultat dans la Défense.
2. Ajuster les cartes directement concernées et leurs données si nécessaire.
3. Noter une décision ou un changement d'état dans le plan, sans recopier l'argument.
4. Lorsqu'un ensemble est prêt à être présenté, réviser le projet français puis les
   adaptations nécessaires ; vérifier les rendus et les liens concernés.

Le futur document **« thèse dans l'état présent »** est un manuscrit continu à préparer
plus tard, pas un export des cartes ni un quatrième résumé à entretenir dès maintenant.
Sa place dans cette organisation sera fixée au début de sa rédaction.
