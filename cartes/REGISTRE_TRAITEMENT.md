# Registre de traitement

Ce registre evite de relire au hasard et de perdre des documents. Le statut `premiere_passe` signifie : texte extrait, idees principales reperees, premieres cartes creees. Ce n'est pas encore une extraction exhaustive.

| Document | Statut | Notes | Cartes creees |
| --- | --- | --- | --- |
| `input/projet thèse philo.pdf` | premiere_passe | Cadrage general de la these. | `idea_0001`, `idea_0018` |
| `input/De l'impossibilité de créer.pdf` | premiere_passe | Essai central, volumineux ; a relire par chapitres. | `idea_0008`, `idea_0009`, `idea_0010`, `idea_0020` |
| `input/ESSAI-La Virtuosité à portée des caniches-F. PACHET.pdf` | premiere_passe | Essai adjacent sur virtuosite et fantasmagories. | `idea_0010`, `idea_0021` |
| `input/ERCGrantPachetInterestingness.pdf` | premiere_passe | Redondant avec docx ancien, mais source canonique deja versionnee. | `idea_0002`, `idea_0003`, `idea_0011`, `idea_0012`, `idea_0013` |
| `input/Hidden_Biases_in_Conditioning_Autoregressive_Models.pdf` | premiere_passe | Ancrage technique pour contraintes et biais de generation. | `idea_0016`, `idea_0017` |
| `input/Notes thèse.pdf` | premiere_passe | Tres court ; carte directe sur doodling. | `idea_0012` |
| `input/The Mystery of Jotney Songs.pdf` | premiere_passe | Exemple musical concentre. | `idea_0019` |
| `old docs /Synopsis MIT Press.doc` | premiere_passe | Gros manuscrit ancien ; a relire par sections. | `idea_0001`, `idea_0004`, `idea_0005`, `idea_0006`, `idea_0007` |
| `old docs /Interesting Interactions (sent to Luc).doc` | premiere_passe | Version courte autour du Continuator. | `idea_0006`, `idea_0007` |
| `old docs /TBKLullyNOTES.doc` | premiere_passe | Notes riches mais fragmentaires. | `idea_0014`, `idea_0015`, `idea_0022`, `idea_0023`, `idea_0024` |
| `old docs /ERCInteractiveReflexions2.docx` | premiere_passe | Projet REFLEX. | `idea_0006`, `idea_0007`, `idea_0025` |
| `old docs /ERCGrantPachetInterestingness (1).docx` | premiere_passe | Variante docx du grant computational interestingness. | `idea_0002`, `idea_0003`, `idea_0011`, `idea_0012`, `idea_0013` |
| `old docs /Paper citations_updated.docx` | premiere_passe | Sense of Direction. | `idea_0016`, `idea_0017`, `idea_0026` |
| `old docs /interestingness.pdf` | premiere_passe | Schmidhuber ; extraction PDF bruitee mais exploitable. | `idea_0027` |
| `old docs /interestingness-ijhcs.pdf` | premiere_passe | Colton/Bundy/Walsh. | `idea_0028` |
| `old docs /kdd95.pdf` | premiere_passe | Silberschatz/Tuzhilin ; extraction PDF bruitee mais exploitable. | `idea_0029` |
| `old docs /Lenat and interestingness.eml` | premiere_passe | Note courte. | `idea_0030` |
| `old docs /interestingness ERC.docx` | a_revoir | Extraction texte vide. Verifier si le document contient seulement styles ou objets non textuels. | - |
| `old docs /interestingness.zip` | dezippe_puis_supprime | Archive dezippee dans `old docs /interestingness/`, puis zip supprime comme doublon. Fichiers texte uniques lus ; `.ps` et doublons exacts supprimes ; MP3 non transcrits. | `idea_0031`, `idea_0032`, `idea_0033`, `idea_0034`, `idea_0035`, `idea_0036`, `idea_0037`, `idea_0038`, `idea_0039`, `idea_0040` |

## Detail du zip dezippe

| Fichier extrait | Statut | Cartes creees |
| --- | --- | --- |
| `old docs /interestingness/.../An interesting musical relationship.doc` | premiere_passe | `idea_0031` |
| `old docs /interestingness/.../Excited Bored.doc` | premiere_passe | `idea_0032`, `idea_0033` |
| `old docs /interestingness/.../ExcitingSequences.html` | premiere_passe | `idea_0032` |
| `old docs /interestingness/.../hooks in hits/Hooks in hits.doc` | premiere_passe | `idea_0034` |
| `old docs /interestingness/.../C_PKDD99.pdf` | premiere_passe | `idea_0035` |
| `old docs /interestingness/.../tkde.pdf` | premiere_passe | `idea_0036` |
| `old docs /interestingness/.../ubiq.pdf` | premiere_passe | `idea_0037` |
| `old docs /interestingness/.../Dan Gang/Expectationfinal-paper.pdf` | premiere_passe | `idea_0038` |
| `old docs /interestingness/.../Dan Gang/aaai99A.pdf` | premiere_passe | `idea_0039` |
| `old docs /interestingness/.../Dan Gang/aaai99B.pdf` | premiere_passe | `idea_0038`, `idea_0039` |
| `old docs /interestingness/.../Dan Gang/netneg.pdf` | premiere_passe | `idea_0039` |
| `old docs /interestingness/.../WhereMusicWillBeComingFromNYTArticle.txt` | premiere_passe | `idea_0040` |
| `old docs /interestingness/.../mvdig003.htm` | premiere_passe_legere | `idea_0034` |
| `old docs /interestingness/.../interestingness-ijhcs.pdf` | supprime_doublon | deja couvert par `idea_0028` |
| `old docs /interestingness/.../kdd95.pdf` | supprime_doublon | deja couvert par `idea_0029` |
| fichiers `.ps` | supprime_doublon | PDF equivalent privilegie |
| fichiers `.mp3` | non_transcrit | a analyser seulement si on veut documenter les hooks audio |

## Prochaine passe recommandee

1. Relire `De l'impossibilité de créer.pdf` par chapitres pour produire des cartes plus fines.
2. Transcrire ou analyser les deux MP3 de hooks si l'argument musical devient central.
3. Decider si les cartes doivent rester numerotees globalement ou recevoir un prefixe par source.
4. Transformer les cartes les plus fortes en familles : `definitions`, `arguments`, `exemples`, `objections`, `technique`.
