# Organisation argumentative des cartes

Cette organisation ajoute deux vues aux index existants : une famille
argumentative principale pour chaque carte et un graphe restreint de relations
fortes. Elle reste volontairement anterieure au plan de these. Son but est de
faire apparaitre les lignes de force, les recouvrements et les objections avant
de choisir un ordre de chapitres.

## Trois axes distincts

1. `indexes/by_level.md` indique le statut epistemique : proposition
   conceptuelle, resultat scientifique ou articulation entre les deux.
2. `indexes/by_argument.md` indique la fonction principale dans l'enquete. Les
   112 cartes y sont affectees une seule fois a sept familles.
3. `relations.tsv` decrit un premier ensemble de relations directionnelles et
   typees. Il ne remplace pas les sections `Liens` des cartes, plus associatives.

Ne pas fusionner ces axes dans une taxonomie unique est important. Une methode
scientifique peut appartenir a la famille de l'attention ; une proposition
musicale peut jouer le role d'objection ; une carte conceptuelle peut servir de
pont avec un systeme.

## Colonne vertebrale actuelle

La premiere lecture du graphe fait apparaitre quatre chaines principales :

```text
emergence d'une forme (0083)
  -> relation forme-memoire (0084)
  -> temporalite de l'agencement (0001)
  -> gain propre a un observateur (0071)
  -> frontiere du presque-apprenable (0107)

necessite inventee (0085)
  -> solution rare d'un probleme implicite (0096)
  -> articulation sampling / contraintes (0109)

musique comme laboratoire (0086)
  -> attentes (0038)
  -> micro-emotions et variations (0112, 0113, 0114)
  -> objection de la surattention (0115)

IA comme laboratoire philosophique (0018)
  -> limite de la naturalisation (0088)
  -> distinction resultats / idees / articulations (0110)
```

Ces chaines ne sont pas encore quatre parties de these. Elles indiquent seulement
les dependances argumentatives les plus nettes.

## Relations typees

Le registre emploie neuf relations :

- `specifies` : ajoute une condition ou un mecanisme a une proposition plus large ;
- `supports` : fournit une raison independante en faveur de la cible ;
- `operationalizes` : transforme la cible en operation, mesure ou test ;
- `illustrates` : fournit un cas sans constituer une preuve generale ;
- `limits` : restreint la portee ou signale une condition d'echec ;
- `objects_to` : formule une objection pouvant remettre la cible en cause ;
- `contrasts_with` : etablit une distinction structurante entre deux regimes ;
- `bridges` : relie deux vocabulaires ou deux niveaux d'analyse ;
- `motivates` : fait apparaitre le besoin auquel repond la cible.

Une relation est directionnelle. `idea_0096 operationalizes idea_0085` ne veut pas
dire que les deux cartes sont synonymes : la premiere propose une formulation
combinatoire d'une intuition philosophique plus large.

## Pivots provisoires

Les cartes les plus structurantes a ce stade sont :

- `idea_0083` et `idea_0084` pour l'objet philosophique central ;
- `idea_0001`, `idea_0071` et `idea_0107` pour sa dynamique temporelle ;
- `idea_0085`, `idea_0096` et `idea_0109` pour probleme, rarete et contraintes ;
- `idea_0086`, `idea_0112` et `idea_0113` pour la theorie de l'attention musicale ;
- `idea_0018`, `idea_0088` et `idea_0110` pour la contribution reflexive de la these.

Une carte pivot n'est pas necessairement vraie, finale ou superieure aux autres.
C'est une proposition dont plusieurs arguments dependent et qu'il faudra donc
defendre ou reformuler explicitement.

## Recouvrements a examiner

Ces groupes sont proches mais ne doivent pas encore etre fusionnes :

- `idea_0027`, `idea_0071` et `idea_0107` : theorie computationnelle, consequence
  relationnelle et formulation de frontiere ;
- `idea_0085`, `idea_0096` et `idea_0099` : necessite inventee, rarete d'une
  solution et singularite du chemin de production ;
- `idea_0006` et `idea_0104` : systeme reflexif particulier et condition generale
  d'une interaction interessante ;
- `idea_0034` et `idea_0112` : hook comme exemple et micro-emotion comme categorie
  phenomenologique ;
- `idea_0049` et `idea_0107` : credibilite de la difficulte et accessibilite d'un
  apprentissage ;
- `idea_0005` et `idea_0115` : insuffisance de la surprise et faux positif produit
  par l'attention.

## Questions ouvertes

- `idea_0083` unifie-t-elle trop vite naissance, comprehension et fascination ?
- La compression de `idea_0027` explique-t-elle l'interet ou seulement une de ses
  trajectoires possibles ?
- La necessite inventee de `idea_0085` est-elle une experience phenomenologique,
  une propriete de forme ou une reconstruction apres coup ?
- Les concepts musicaux de `idea_0112` se generalisent-ils au-dela de l'oreille
  et du repertoire qui les ont produits ?
- Comment distinguer empiriquement l'optale de `idea_0113` et la surattention de
  `idea_0115` ?
- Quelles constructions scientifiques soutiennent vraiment une articulation
  philosophique, et lesquelles ne sont que des analogies suggestives ?

## Regle de maintenance

Une nouvelle carte doit recevoir une famille principale et, si elle affecte une
proposition pivot, au moins une relation typee. Une relation ne doit etre ajoutee
que si une phrase peut expliquer sa direction. Les proximites vagues restent dans
les liens locaux des cartes.
