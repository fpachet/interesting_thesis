# Plan documentaire initial

Ce plan sert de carte du territoire avant classement des idees. Il distingue les documents de these actuels, les anciens documents ajoutes dans `old docs `, et les artefacts deja produits par le pipeline.

## Corpus actuel dans `input/`

| Document | Role probable | Idees dominantes |
| --- | --- | --- |
| `input/projet thèse philo.pdf` | cadrage doctoral | emergence de l'interessant, singularite des formes, naissance des idees, articulation IA/philosophie |
| `input/De l'impossibilité de créer.pdf` | grand essai central | impossibilite de creer, adjacent possible, inhibition, invention impensable, virtuosite, difficulte, IA |
| `input/ESSAI-La Virtuosité à portée des caniches-F. PACHET.pdf` | essai adjacent | virtuosite spectaculaire, fantasmagories politiques, pensee deviante, exposition reseaux |
| `input/ERCGrantPachetInterestingness.pdf` | programme scientifique | computational interestingness, gout non statique, popularite, difficultuosite, doodling, ethologie artificielle |
| `input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf` | ancrage technique IA | generation contrainte, biais inferentiels, echantillonnage, contraintes globales |
| `input/Notes thèse.pdf` | notes courtes | doodling comme echantillonnage pur, Flow Machines, adjacent possible |
| `input/The Mystery of Jotney Songs.pdf` | exemple musical | rare equilibre melodie/harmonie, naturel apparent, chanson autonome, contraintes invisibles |

## Documents anciens dans `old docs `

Le dossier existe bien sous le nom exact `old docs `, avec un espace final.

| Document | Statut de lecture | Idees dominantes |
| --- | --- | --- |
| `old docs /Synopsis MIT Press.doc` | lu en premiere passe | temporal interestingness, ennui, active listening, exploration musicale, structure d'un livre |
| `old docs /Interesting Interactions (sent to Luc).doc` | lu en premiere passe | interaction reflexive, Continuator, Flow machines, creation comme effet secondaire |
| `old docs /TBKLullyNOTES.doc` | lu en premiere passe | PathBuilder, spam interessant, ordres d'interessant, mauvais objets addictifs, apprentissage |
| `old docs /ERCInteractiveReflexions2.docx` | lu en premiere passe | reflexive interactive systems, creation individuelle, miroir, etudes musique/ecriture/dessin |
| `old docs /ERCGrantPachetInterestingness (1).docx` | lu en premiere passe | version docx du programme Computational Interestingness |
| `old docs /Paper citations_updated.docx` | lu en premiere passe | Creative AI with a Sense of Direction, generation structuree, innovation, long-range correlations |
| `old docs /interestingness.pdf` | lu en premiere passe | Schmidhuber, regularites inattendues, progres de compression, curiosite artificielle |
| `old docs /interestingness-ijhcs.pdf` | lu en premiere passe | Colton/Bundy/Walsh, interestingness en decouverte mathematique |
| `old docs /kdd95.pdf` | lu en premiere passe | mesures subjectives d'interet en knowledge discovery, croyances, surprise, actionabilite |
| `old docs /Lenat and interestingness.eml` | lu en premiere passe | Lenat, coincidence, nombreux exemples |
| `old docs /interestingness ERC.docx` | lisible mais vide a l'extraction | probablement conteneur docx sans texte principal exploitable |
| `old docs /interestingness.zip` | dezippe puis supprime | archive de references anciennes ; les fichiers texte uniques ont ete distilles, les `.ps` doublonnant des PDF et les doublons exacts ont ete supprimes, les MP3 restent non transcrits |

## Fichiers extraits de `interestingness.zip`

| Fichier extrait | Statut | Idees dominantes |
| --- | --- | --- |
| `An interesting musical relationship.doc` | premiere_passe | relation musicale optimale, distance de gout, nouveaute versus confiance |
| `Excited Bored.doc` | premiere_passe | jeu producteur/auditeur, sequences excitantes, meilleur prochain item, compromis repetition/variation |
| `ExcitingSequences.html` | premiere_passe | version courte du jeu des sequences excitantes |
| `hooks in hits/Hooks in hits.doc` | premiere_passe | hooks harmoniques, progressions populaires, surprise locale |
| `C_PKDD99.pdf` | premiere_passe | sequence mining, croyances, regles inattendues, post-mining |
| `tkde.pdf` | premiere_passe | mesures subjectives, unexpectedness, actionability, belief systems |
| `ubiq.pdf` | premiere_passe | suite de Prouhet-Thue-Morse, non-repetition, ubiquite combinatoire |
| `Dan Gang/Expectationfinal-paper.pdf` | premiere_passe | attentes musicales, realisation, surprise, ecoute en temps reel |
| `Dan Gang/aaai99A.pdf`, `aaai99B.pdf`, `netneg.pdf` | premiere_passe | systemes hybrides neuro-symboliques, connaissance musicale, regles/fuzzy/apprentissage |
| `WhereMusicWillBeComingFromNYTArticle.txt` | premiere_passe | copies parfaites/gratuites/liquides, attention comme rarete, musique comme verbe |
| `mvdig003.htm` | premiere_passe_legere | discussion fan autour de paroles/musique, interpretation, hooks, collaboration |
| `interestingness-ijhcs.pdf`, `kdd95.pdf` | supprimes_doublons | memes documents que ceux deja presents directement dans `old docs ` |
| fichiers `.ps` | supprimes_doublons | doublons PostScript des PDF disponibles |
| fichiers `.mp3` | non_transcrits | exemples sonores non analyses dans cette passe |

## Artefacts du pipeline

| Artefact | Utilite |
| --- | --- |
| `output/runs/q00_baseline_20260412/corpus_digest.md` | synthese deja calculee du corpus courant |
| `output/runs/q00_baseline_20260412/round_*.md` | debat multi-agents precedent |
| `output/runs/q00_baseline_20260412/final_synthesis.md` | formulation synthetique deja disponible |
| `memory/runs/q00_baseline_20260412.json` | memoire structuree du run |

## Grandes familles qui emergent

- L'interessant comme processus temporel plutot que qualite statique.
- L'interessant comme region intermediaire entre trivial et aleatoire.
- L'ennui comme condition, menace ou envers productif de l'interessant.
- La creation comme impossibilite, ruse, deplacement ou effet secondaire.
- Les contraintes comme machines a faire apparaitre des formes rares.
- La similarite et l'exploration comme chemins, non comme simple transfert de gout.
- Les systemes reflexifs comme miroirs qui produisent de la creation par interaction.
- La generation IA comme probleme de direction, structure et contraintes globales.
- La musique comme laboratoire privilegie de l'interessant temporel.
- La copie numerique comme passage de l'objet fixe vers la manipulation, la recommandation et la personnalisation.
- Les suites formelles comme modeles minimaux de non-repetition, surprise et attention.
