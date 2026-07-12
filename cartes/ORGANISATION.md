# Organisation argumentative des cartes

Cette organisation ajoute deux vues aux index existants : une famille
argumentative principale pour chaque carte et un graphe restreint de relations
fortes. Elle reste volontairement antérieure au plan de thèse. Son but est de
faire apparaître les lignes de force, les recouvrements et les objections avant
de choisir un ordre de chapitres.

## Trois axes distincts

1. `indexes/by_level.md` indique le statut épistémique : proposition
   conceptuelle, résultat scientifique ou articulation entre les deux.
2. `indexes/by_argument.md` indique la fonction principale dans l'enquête. Les
   121 cartes y sont affectées une seule fois à sept familles.
3. `relations.tsv` décrit un premier ensemble de relations directionnelles et
   typées. Il ne remplace pas les sections `Liens` des cartes, plus associatives.

Ne pas fusionner ces axes dans une taxonomie unique est important. Une méthode
scientifique peut appartenir à la famille de l'attention ; une proposition
musicale peut jouer le rôle d'objection ; une carte conceptuelle peut servir de
pont avec un système.

## Colonne vertébrale actuelle

La première lecture du graphe fait apparaître quatre chaînes principales :

```text
émergence d'une forme (0083)
  -> relation forme-mémoire (0084)
  -> zone de flow entre ennui et anxiété (0121)
  -> construction d'une prise sur l'objet (0123)
  -> reconstruction du problème depuis sa solution (0085)
  -> dérives et épuisement de la relation (0122)

nécessité inventée (0085)
  -> solution rare d'un problème implicite (0096)
  -> articulation sampling / contraintes (0109)

musique comme laboratoire (0086)
  -> attentes (0038)
  -> micro-émotions et variations (0112, 0113, 0114)
  -> objection de la surattention (0115)

IA comme laboratoire philosophique (0018)
  -> limite de la naturalisation (0088)
  -> distinction résultats / idées / articulations (0110)
```

Ces chaînes ne sont pas encore quatre parties de thèse. Elles indiquent seulement
les dépendances argumentatives les plus nettes.

## Relations typées

Le registre emploie neuf relations :

- `specifies` : ajoute une condition ou un mécanisme à une proposition plus large ;
- `supports` : fournit une raison indépendante en faveur de la cible ;
- `operationalizes` : transforme la cible en opération, mesure ou test ;
- `illustrates` : fournit un cas sans constituer une preuve générale ;
- `limits` : restreint la portée ou signale une condition d'échec ;
- `objects_to` : formule une objection pouvant remettre la cible en cause ;
- `contrasts_with` : établit une distinction structurante entre deux régimes ;
- `bridges` : relie deux vocabulaires ou deux niveaux d'analyse ;
- `motivates` : fait apparaître le besoin auquel répond la cible.

Une relation est directionnelle. `idea_0096 operationalizes idea_0085` ne veut pas
dire que les deux cartes sont synonymes : la première propose une formulation
combinatoire d'une intuition philosophique plus large.

## Pivots provisoires

Les cartes les plus structurantes à ce stade sont :

- `idea_0083`, `idea_0084`, `idea_0121` et surtout `idea_0123` pour l'objet philosophique central ;
- `idea_0001`, `idea_0071`, `idea_0107` et `idea_0122` pour sa dynamique temporelle ;
- `idea_0085`, `idea_0096` et `idea_0109` pour problème, rareté et contraintes ;
- `idea_0086`, `idea_0112` et `idea_0113` pour la théorie de l'attention musicale ;
- `idea_0018`, `idea_0088` et `idea_0110` pour la contribution réflexive de la thèse.

Une carte pivot n'est pas nécessairement vraie, finale ou supérieure aux autres.
C'est une proposition dont plusieurs arguments dépendent et qu'il faudra donc
défendre ou reformuler explicitement.

## Recouvrements à examiner

Ces groupes sont proches mais ne doivent pas encore être fusionnés :

- `idea_0027`, `idea_0071` et `idea_0107` : théorie computationnelle, conséquence
  relationnelle et formulation de frontière ;
- `idea_0085`, `idea_0096` et `idea_0099` : nécessité inventée, rareté d'une
  solution et singularité du chemin de production ;
- `idea_0006` et `idea_0104` : système réflexif particulier et condition générale
  d'une interaction intéressante ;
- `idea_0034` et `idea_0112` : hook comme exemple et micro-émotion comme catégorie
  phénoménologique ;
- `idea_0049` et `idea_0107` : crédibilité de la difficulté et accessibilité d'un
  apprentissage ;
- `idea_0005` et `idea_0115` : insuffisance de la surprise et faux positif produit
  par l'attention.

## Questions ouvertes

- `idea_0083` unifie-t-elle trop vite naissance, compréhension et fascination ?
- La compression de `idea_0027` explique-t-elle l'intérêt ou seulement une de ses
  trajectoires possibles ?
- La nécessité inventée de `idea_0085` est-elle une expérience phénoménologique,
  une propriété de forme ou une reconstruction après coup ?
- Les concepts musicaux de `idea_0112` se généralisent-ils au-delà de l'oreille
  et du répertoire qui les ont produits ?
- Comment distinguer empiriquement l'optale de `idea_0113` et la surattention de
  `idea_0115` ?
- Quelles constructions scientifiques soutiennent vraiment une articulation
  philosophique, et lesquelles ne sont que des analogies suggestives ?

## Règle de maintenance

Une nouvelle carte doit recevoir une famille principale et, si elle affecte une
proposition pivot, au moins une relation typée. Une relation ne doit être ajoutée
que si une phrase peut expliquer sa direction. Les proximités vagues restent dans
les liens locaux des cartes.
