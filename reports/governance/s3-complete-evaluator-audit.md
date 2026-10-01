# Revue complète des évaluateurs S3 hors R0–R2

## Verdict, périmètre et référence

Audit du **1er octobre 2026**, branche `governance/s3-complete-evaluator-audit`,
référence `c649cfe51f0dce66efcaef7aad652c0b92d606ad` : état contenant les corrections
R0–R2 de la PR17. Il ne faut pas assimiler cet état à un déploiement déjà effectué.
La mission demandée est une **revue**, sans modification du produit.

**Produit : REQUEST_CHANGES. Processus de revue documentaire : CONFORME.**
Les deux verdicts portent sur des objets différents : les défauts ci-dessous
restent présents dans les correcteurs ; ce rapport ne les corrige pas et ne
certifie pas la fiabilité globale du produit. Aucun verdict `READY_TO_MERGE`
ni autorisation de mise en production n'est donné.

Les **15 autres évaluateurs S3** ont été examinés : TD0–TD7 (**55 questions**) et
contrôles TD1–TD7 (**49 questions**), soit **104 questions**. R0–R2 sont exclus de
cette matrice : leur révision est documentée séparément dans
[r012-s3-evaluation-v2.md](r012-s3-evaluation-v2.md). Les 104 lignes ci-dessous
explicitent ce que contrôle réellement le serveur, ce qui relève de la relecture
et les écarts constatés. Aucun support n'est simplifié ni supprimé.

Les correcteurs ne souffrent pas tous du défaut initial de R0–R2. Les microcas
TD4–TD7 et les contrôles C4–C7 confrontent déjà les valeurs enregistrées à des
références numériques cohérentes. Des défauts transversaux d'attribution et de
contrat de cellules concernent néanmoins les 15 évaluateurs. Des défauts précis
d'indices, d'ordre et de dépendances affectent TD1–TD3. TD1/TD2 vérifient aussi des
structures et des cohérences, explicitement sans certifier les mesures spaCy.

## Méthode, indépendance et preuves

Sources normatives consultées : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`,
`docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et rôles d'audit.
Quatre auditeurs techniques indépendants ont réparti TD0–TD3, TD4–TD7,
C1–C4 et C5–C7. Un Pedagogy-Reviewer a lu les 15 supports et leur couverture.
L'orchestrateur a reproduit les défauts transversaux par le client Flask.
Le Governance-Auditor consolide les constats et écrit uniquement dans
`reports/governance/`. Aucun agent de cette mission n'a modifié les notebooks,
les correcteurs, les tests, les règles normatives ou les fichiers de déploiement.

Les sondes appellent les validateurs sur des cellules JSON fabriquées, avec
identités fictives et persistance temporaire. **Aucun code de notebook étudiant
n'a été exécuté.** Des calculs indépendants de référence ont été exécutés comme
code d'audit enseignant. Pour TD1/TD2, ils utilisent spaCy 3.8.7 et
`fr_core_news_sm` 3.8.0 sur les textes publics fixés par les sujets : 6/6 et 7/7.
Cela ne constitue pas une exécution des sujets dans Colab.

Preuves durables : [résultats structurés](s3-complete-evaluator-audit-evidence.json)
et [sondes reproductibles](s3-complete-evaluator-audit-probes.md).
Les chemins de fonctions sont relatifs au dépôt, à la référence ci-dessus.
Les résultats des auditeurs sont des preuves de session, pas des approbations
GitHub déjà publiées.

| Vérification | Résultat et portée |
|---|---|
| Suite de tests existante | Orchestrateur : **169 tests PASS**, 3,646 s. Une suite verte ne couvre pas les défauts nouveaux reproduits par les sondes. |
| TD0–TD3 | 21 tests existants PASS ; références enseignant TD1 6/6, TD2 7/7 ; faux intervalles, occurrence répétée, ordre et booléens reproduits séparément. |
| TD4–TD7 | 28 références numériques cohérentes ; 28 traces remplacées par `{}` refusées au critère concerné ; rôles `provided` et erreurs enregistrées exclus. |
| C1–C4 | 28 critères exercés, 20/20 par contrôle sur traces synthétiques cohérentes ; 122 mutations entières/booléennes de C4 rejetées. Les traces linguistiques C1–C3 ne sont pas des vérités linguistiques de référence. |
| C5–C7 | 21 références indépendantes ; 21 mutations de structure et 21 mutations de valeur rejetées ; erreurs ciblées, rôles `example` et erreurs enregistrées exclus. |
| Confidentialité des contrôles | Tests et sondes HTTP : reçu public seul, rapports et notes privés ; aucun défaut de divulgation reproduit dans cette mission. |
| Métadonnées des sources | 15 identifiants globaux v1 cohérents ; 104 réponses identifiées ; une identité par notebook. Les cellules d'identité ne demandent pas de numéro étudiant. |
| Tuteurs | Orchestrateur : **34 tuteurs vérifiés** ; règles TD/contrôle conservées. |
| Distribution | Orchestrateur : **33 copies générées et vérifiées** avec URL neutre ; cellule HTML finale dans les copies distribuables, volontairement absente des sources. L'adresse reste lisible par le destinataire, mais hors Git source. |
| Conditions non testées | Colab, navigateur de production, proxy réel et Docker dans cette mission : **NOT_TESTED**. Pas d'observation en classe ni preuve d'authenticité des réponses. |

## Constats priorisés et critères de correction

P1 : attribution, contrat de dépôt, valeur de preuve ou sens du score à corriger
avant d'utiliser les résultats comme base de notation. P2 : précision du contrat,
diagnostic et relecture. Une **limite déclarée** ne devient pas un bug par le seul
fait qu'une trace correcte ne démontre pas la maîtrise d'un programme.

### S3-A01 — P1 : identité non fiable et collisions de copies, 15/15

Sources : `app/outils.py::extract_identification_info`, `check_identification`,
`log_grade_to_csv` ; `app/routes.py::process_submission` ; moteurs
`app/s3_audit.py::check_audit` et `app/s3_controls.py::check_control`.

Les 15 POST de copies aux noms/prénoms vides sont acceptés et sauvegardés.
Le numéro étudiant, même ajouté dans la cellule d'identité, n'est pas extrait.
Pour chacun des 15 évaluateurs, deux étudiants fictifs homonymes, avec numéros
distincts et même nom de fichier, laissent **une seule copie et un seul rapport**
mais deux lignes CSV : le second dépôt remplace les fichiers du premier.
La regex `nom` reconnaît également la fin de `prenom` et les commentaires :
`prenom="Alice"` avant `nom="Dupont"` donne `nom=Alice` ; un commentaire
`# nom="Commentaire"` donne `nom=Commentaire`.

**Correction minimale :** extraction AST d'affectations littérales, noms exacts,
commentaires ignorés, cellule d'identité unique ; numéro obligatoire et identité
complète validés avant correction/persistance. Fichiers, CSV et rapport doivent
conserver le numéro et différencier les homonymes. Prévoir un stockage compatible
avec les anciens CSV, sans les écraser. Le renouvellement de la copie d'un même
étudiant peut rester autorisé selon une règle explicite.

**Acceptation :** identité vide refusée ; ordre des affectations libre ; commentaire
sans effet ; deux numéros distincts produisent deux copies/deux rapports ; aucun
CSV n'est ajouté lors du rejet. L'ancien contrat de notebook est refusé par
« mauvaise version du notebook », sans note zéro ni migration automatique.

### S3-A02 — P1 : absence de métadonnées de cellules réactive la collecte historique

Sources : `app/notebook_contract.py::resolve_notebook`, `validate_cell_metadata`,
`resolve_cells` ; `app/s3_audit.py::collect` et moteur des contrôles.

La version globale est contrôlée, mais la présence du jeu de cellules contractuel
ne l'est pas. Après suppression de toutes les métadonnées de cellules, les moteurs
reprennent le chemin historique. Sonde HTTP TD4 : une trace dans une cellule
`example` donne 0 avec les métadonnées, puis 1 après leur suppression ; les deux
soumissions sont persistées. Les auditeurs reproduisent aussi 7/7 sur TD4–TD7 et
20/20 sur C4 après retrait des métadonnées cellulaires.

**Correction minimale :** valider, pour chaque contrat strict, les identifiants et
rôles obligatoires, l'unicité et les correspondances attendues avant d'évaluer.
Refuser le contrat absent/incompatible avec **« mauvaise version du notebook »**,
sans correction ni persistance. Ne pas confondre cellule réponse présente mais
vide (question non faite) et cellule contractuelle manquante (mauvais contrat).
Les déplacements et les cellules personnelles autorisées doivent rester possibles.

### S3-A03 — P1 : offsets hors texte acceptés dans TD1 et TD3

Sources : `app/s3_audit_linguistic.py::annotations` (TD1 Q1/Q6),
`app/app_correction_TD3_S3.py::research_modes` (Q3), `evidence` (Q7).

Le slicing Python tronque une fin supérieure à la longueur du texte. Une tranche
égale au passage ne prouve donc pas que l'intervalle est valide. Les sondes TD1 Q1
et TD3 Q3 avec `fin=999` obtiennent le point. Une sonde du validateur Q7 accepte
également des fins après le corpus ; cette dernière porte sur le helper, pas sur
une trace complète acceptée à travers la limite de taille du collecteur.

**Correction/acceptation :** imposer des entiers stricts et
`0 <= debut < fin <= len(source)`, puis longueur et égalité du passage. Tester les
bornes exactes, dépassements, valeurs négatives/booléennes, Unicode et CRLF.
Aucun changement du sujet n'est nécessaire si ses formats actuels suffisent.

### S3-A04 — P1 : TD3 Q7 compte des fenêtres au lieu d'occurrences distinctes

Source : `app/app_correction_TD3_S3.py::evidence`.
Trois fenêtres différentes entourant **la même première occurrence**
d'« intelligence » sont acceptées pour la demande de trois preuves distinctes.
La distinctivité actuelle porte sur les limites de fenêtres, pas sur le pivot.

**Correction/acceptation :** déterminer les positions absolues des occurrences du
pivot dans les passages et exiger trois positions distinctes. Une occurrence avec
trois fenêtres doit être refusée ; trois occurrences réelles, avec contextes libres
et intervalles valides, doivent être acceptées.

### S3-A05 — P2 : « Note Finale » sur les huit TD, alors que le score est partiel

Sources : `app/s3_audit.py::check_audit`,
`app/templates/corrector_template.html`, sélection dans `app/routes.py`.
Les introductions et `LIMIT_NOTE` décrivent correctement une vérification limitée,
mais les TD ne fournissent pas `score_nature` ; le template affiche alors
« Note Finale ». Les contrôles ont déjà un libellé technique provisoire.

**Correction/acceptation :** rendre la nature formative/technique explicite dans
l'en-tête et le rapport ; aucun résultat TD0–TD7 ne doit être intitulé « Note Finale ».
Préciser que figures, interprétation, généralité des fonctions et transfert ne sont
pas certifiés par le score. Aucun changement de maxima n'est requis.

### S3-A06 — P2 : ordre, types et dépendances de TD1/TD2

Sources : `app/s3_audit_linguistic.py::filters`, `exclusions`, `chart_data`,
`generalization` ; contexte construit dans `app/s3_audit.py`.

- TD1 Q3 demande l'ordre des lemmes, mais accepte `mots_pleins` inversé car le test
  utilise des multisets. Vérifier au minimum une sous-séquence ordonnée ; tout
  contrôle exhaustif du filtrage exige les traces nécessaires.
- TD2 accepte des recoupements Python où `True == 1`. Q2 avec un booléen est
  refusée, mais Q3/Q6/Q7 reçoivent chacune un point en réutilisant ce contexte
  invalide. Valider le schéma des dépendances et comparer avec typage strict.
- TD0 Q7 n'alerte pas sur la synthèse vide pourtant demandée ; TD1 Q1 accepte un
  `tag` nul. Séparer la présence/type attendu de l'évaluation qualitative humaine.

**Acceptation :** permutation indue refusée ; répétitions conservées ; booléen jamais
traité comme effectif ; référence amont mal typée signalée ; champ manquant signalé
sans score de qualité fondé sur la longueur ou des mots-clés.

### S3-A07 — P2 : dépendance manquante présentée comme erreurs indépendantes

Sources : `app/s3_controls.py::check_control`, validateurs linguistiques et contexte
TD1/TD2. Retirer seulement la trace Q2 de C1 fait passer 20 à 8 ; retirer seulement
Q1 de C2 fait passer 20 à 6. Les questions aval restent remplies mais affichent des
croix et retours génériques, sans cause commune « dépend de Q… ».

**Correction minimale :** distinguer `incorrect`, `preuve absente` et
`non vérifiable — dépend de Q…`, regrouper la cause et les points à revoir. Ne pas
accorder automatiquement des points non démontrés ni remplacer les annotations
étudiantes par une vérité serveur. Toute redistribution des points pour limiter
les pénalités en cascade doit être arbitrée par l'enseignant et documentée.

Le retour C1 Q1 doit aussi être clarifié : « split du texte original ; fréquences
après passage en minuscules », au lieu de la formulation ambiguë actuelle.

### S3-A08 — P2 : diagnostic binaire et relecture peu préparée

Sources : `app/s3_controls.py` (tout ou rien par question),
`app/s3_audit.py`, `app/templates/s3_controle_report_template.html`.
Une seule erreur dans une grande trace composite fait perdre l'ensemble des
points de la question. Par exemple, changer seulement une moyenne de C6 Q7 annule
ses trois points. Les critères humains existent, mais le rapport ne rassemble pas
les productions attendues/présentes, question par question.

**Suite proposée :** détailler les sous-critères et identifier la composante fautive ;
conserver les maxima mais soumettre tout nouveau partage des points à validation
enseignante. Préparer des liens/extraits et un état de présence des figures,
analyses et transferts dans le rapport privé. Présence n'est pas qualité : ni
longueur ni mots-clés ne doivent devenir une note d'interprétation. Les contrôles
continuent à renvoyer au public le seul reçu de dépôt.

## Limites déclarées et enrichissements possibles

1. **TD1/TD2 : cohérence n'est pas exactitude du pipeline.** Des traces absurdes mais
   cohérentes obtiennent 6/6 et 7/7. Les modules l'annoncent, ce n'est donc pas une
   garantie linguistique violée. Pour l'objectif de fiabilité quantitative, définir
   soit une référence du pipeline versionné, soit des annotations assez complètes
   pour recalculer les sommes, filtres et distributions. Distinguer conformité au
   modèle et analyse manuelle de ses erreurs ; prévoir les alternatives motivées.
2. **Source, trace et authenticité.** Une trace correcte n'atteste pas le programme
   qui l'a produite, sa fraîcheur ou sa généralité. Ce point est déjà déclaré et
   testé. Le serveur doit rester sans exécution du code étudiant. Des contrôles
   AST ciblés peuvent améliorer les preuves, sans promettre d'authentification.
3. **Données fournies.** Dans C4, remplacer la donnée fournie par une liste vide et
   conserver les anciennes sorties ne change pas le score. Une empreinte ou une
   comparaison des littéraux contractuels est un durcissement utile, pas une preuve
   de fraîcheur de toutes les sorties. L'introduire requiert un contrat clair.
4. **C6 Q7 : cas peu discriminant.** Les trois dénominateurs valent 8 ; moyenne
   simple et taux global valent donc 125 pour mille. Les références sont correctes
   et le sujet dit « éventuel écart ». Un cas supplémentaire à dénominateurs
   inégaux serait plus discriminant, sans modifier silencieusement les données.
5. **Productions humaines.** Les fonctions, figures, lectures linguistiques et
   dossiers Faguet doivent être conservés. Leur absence du score automatique est
   souvent volontaire et annoncée ; la réponse adaptée est une meilleure grille
   de relecture, pas leur suppression des sujets.

## Plan minimal de mise en œuvre

| Lot | Modifications | Version/distribution | Vérification attendue |
|---|---|---|---|
| 1 — Attribution et contrat | Identité AST/numéro, stockage homonymes, jeu de cellules strict, rejet avant calcul/persistance | Les 15 sujets ont besoin d'une identité enrichie ; versionner ces nouveaux contrats et redistribuer après validation. Ne pas simplement changer `version` dans les copies anciennes. | 15 scénarios identité ; anciens contrats refusés exactement ; homonymes séparés ; cellules déplacées et réponses vides valides |
| 2 — Bugs de validation | Bornes, occurrences distinctes, ordre, types/dépendances, en-tête et retours ciblés | Correction seule sans nouveau champ : conserver le contrat lorsque possible. | Transformer les sondes négatives et leurs témoins positifs en tests ciblés |
| 3 — Portée quantitative TD1/TD2 | Définir quelles mesures doivent être exactes, compléter les traces ou figer une référence de pipeline, préserver la relecture linguistique | Matrice source → cible et double revue avant changement ; nouvelle version seulement si le contrat étudiant évolue | Références correctes, fausses mesures cohérentes, variantes légitimes, types et dépendances |
| 4 — Diagnostic enseignant | Statuts de dépendance, liste des productions humaines, sous-critères proposés | Barème inchangé tant que la nouvelle granularité n'est pas validée ; nouvelle trace à versionner si nécessaire | Une erreur localisée identifiable ; aucun détail de contrôle dans le reçu public |
| 5 — Validation et diffusion | Revue technique/pédagogique, gouvernance, régressions, génération `dist/`, déploiement mainteneur | Régénérer et vérifier les copies distribuables après fusion ; rejeter les anciennes, sans migration ni note zéro | Métadonnées/identité/104Q, cellule HTML, dépôt proxy, confidentialité et stockage |

Aucune réécriture générale des 104 validateurs numériques n'est justifiée par les
preuves. Les valeurs déterministes vérifiées peuvent être conservées. Une nouvelle
version doit matérialiser un contrat précis, pas servir de label abstrait de
fiabilité. Cette revue n'a pas changé `dist/` distribué sur le serveur : ne pas
annoncer aux étudiants qu'un correctif a déjà été appliqué.

## Matrice exhaustive des 104 questions

Les matrices suivantes sont issues des quatre revues techniques indépendantes.
« Conforme » signifie conforme à la **trace technique annoncée**, sous réserve des
défauts transversaux précédents. Les références TD03, TD47, C14, PED et C57 renvoient
aux identifiants des revues spécialisées, rattachés aux constats consolidés :
TD03-01→A03, TD03-02→A04, TD03-03/04/05→A06 ; TD47-01/C14-04→A02 ;
TD47-02/C14-01/02→A01 ; PED-01→A05 ; PED-02/C14-03→A07 ; PED-03/04→A08.
Les suffixes L indiquent une limite déclarée ou un enrichissement facultatif.

### TD0–TD3 : 27 questions

| Question | Attendu du sujet | Vérification effective | Verdict / lacune |
|---|---|---|---|
| TD0 Q1 | Lire UTF-8, préserver fichier, comparer texte, transférer Faguet ; trace longueur texte | Dict exact `caracteres=277` | Exact pour trace ; lecture réelle et transfert non évalués automatiquement, partiel déclaré |
| TD0 Q2 | split brut, observer ponctuation/apostrophes, essai personnel ; liste complète | Liste de 47 éléments exactement identique au texte | Exact ; observations/essai hors score |
| TD0 Q3 | len et boucle concordants, transfert ; occurrences | Entier typé 47 | Exact trace ; présence de boucle non exigée par code, partiel déclaré |
| TD0 Q4 | ensemble, cardinalité, occurrence/forme ; nombre formes | Entier typé 41 | Exact trace ; explication humaine |
| TD0 Q5 | fonction, dictionnaire, somme/cardinalité, liste vide et transfert | Dictionnaire complet `Counter(TEXT0.split())` | Exact trace ; fonction/tests/transfert non validés |
| TD0 Q6 | fonction minuscule puis split, réutilisation, comparaison | Dictionnaire complet `Counter(TEXT0.lower().split())` | Exact trace ; comparaison interprétative humaine |
| TD0 Q7 | split du microcas et synthèse explicitement non vide | Liste exacte, `limites` seulement str | Partiel déclaré pour argumentation ; non-vacuité non vérifiée (TD03-05) |
| TD1 Q1 | Tous tokens non ponctuation, forme/lemme/POS/tag et offsets, comparaison manuelle | Présence des clés, POS valide, recouvrement alphanumérique du texte sans trous | Partiel déclaré pour prédictions ; bornes fin et type tag incomplets (TD03-01/05) ; un token couvrant tout le texte accepté |
| TD1 Q2 | Chaque phrase doc.sents et nombre tokens, essai abréviation | Reconstruction texte, taille tokens entre split et caractères | Partiel déclaré : une phrase unique avec autant de tokens que de caractères acceptée ; pas de vérité segmentation certifiée |
| TD1 Q3 | NOUN, VERB, NOUN/VERB/ADJ sans stopwords ; **« Gardez les lemmes dans l'ordre, y compris leurs répétitions »** | NOUN/VERB égaux aux listes Q1 ; mots_pleins sous-multiensemble non vide | Bug ordre ignoré (TD03-03). Stopwords et exhaustivité hors champ faute de is_stop dans trace ; partiel déclaré |
| TD1 Q4 | Visualiser première phrase, verbe principal et dépendant, relation et interprétation | Deux chaînes retrouvées à leurs offsets ; relation chaîne >=3 ; interprétation str | Repères uniquement, déclaré ; `Les` pris comme verbe et dépendant accepté, qualité linguistique/figure humaine |
| TD1 Q5 | Comparer split/tokens/non-ponctuation sur TEXT0 | split=47 strict, autres nombres bornés | Partiel déclaré, aucun comptage spaCy exact certifié |
| TD1 Q6 | Extrait 2–4 phrases, cinq **premiers** tokens, noms/verbes, question | Texte non vide, compteur 2–4, cinq annotations localisées, listes de chaînes | Cinq tokens quelconques plus tard dans texte acceptés ; nombres et listes non recoupés. Partiel déclaré sur annotations, « premiers » non vérifié ; bornes fin bug TD03-01 |
| TD2 Q1 | Longueur, phrases, tokens, dix **premiers** tokens non ponctuation | Longueur exacte, nombres bornés, 10 formes retrouvées dans ordre | Partiel déclaré ; peut sauter les premiers tokens/autoriser ponctuation attachée, pas de référence tokenisation |
| TD2 Q2 | Fonctions NOUN/VERB sans stopwords, fréquences complètes, tests | Deux dicts non vides, chaînes et effectifs entiers positifs, somme <=15 | Partiel déclaré substantiel : `licorne/dragon/voler` absents du texte acceptés ; totalité quanti non assurée (TD03-L01) |
| TD2 Q3 | Exclure >=1 nom présent, conserver effectifs, justification | Avant=Q2, exclusions minuscules, après exact | Cohérence utile ; comparaison Python bool==int accepte contexte Q2 invalide (TD03-04) |
| TD2 Q4 | POS hors ponctuation/espaces, total tokens conservés, top3 | POS valides, somme <=15, top3 conforme effectifs triés, ex æquo acceptés | Partiel déclaré : {'NOUN':1} accepté, total exact non recoupé |
| TD2 Q5 | Lemmes NOUN/VERB/ADJ hors stops ; contrôle manuel 5 tokens | Liste non vide bornée, 5 formes sous-chaînes présentes, POS valide, textes explicatifs str | Partiel déclaré ; cinq copies du caractère `L` avec lemme inventé passent ; absence de distinctivité/provenance de tokens à renforcer |
| TD2 Q6 | Nuage + barres des mêmes noms filtrés ; interprétation | Fréquences non vides égales après Q3, textes str | Partiel déclaré : figures explicitement à vérifier humainement ; bool==int de contexte partagé TD03-04 |
| TD2 Q7 | Fonction générale égale spécialisées, combinaison, vide/exclusions, transfert | Dictionnaires égaux Q2 ; combinaison somme Counter | Cohérence utile ; aucune fonction requise (limite traces) ; parent invalide/type non strict TD03-04 |
| TD3 Q1 | Provenance, hash, G1–G6, 3 prompts, paramètres manquants | Hash exact, IDs exacts, entier3, >=2 chaînes et limite str | Exact partie provenance ; paramètres/limite jugés humainement ; doublons de paramètres acceptés |
| TD3 Q2 | Concordances exactes 3 occurrences et absent ; fonction/tests bords/motif vide/transfert | Égalité exacte indices/pivots/contextes largeur20 et absent=[] | Exact trace ; cas de tests supplémentaires et fonction ne font pas partie de la trace contrôlée |
| TD3 Q3 | Fragment/forme lit et lemme lire sur texte fixé, offsets, transfert, PhraseMatcher | Fragment et forme exacts ; lemme: >=1 passage localisable | Partiel déclaré lemmatisation ; **fin hors texte accepté** (TD03-01) ; doublons/ordre/limites de tokens non vérifiés |
| TD3 Q4 | 3 citations, match exact ou -1, bool, limite | Dict exact par ID, ordre des lignes libre ; CRLF préservé/hash vérifié | Exact ; typage strict ; limites humaines |
| TD3 Q5 | C1 passage original, indice, substitution et qualification | Passage exact à position donnée contenant légalement/naturellement | Partiel déclaré pour argumentation ; provenance contrôlée, pas de borne max de passage ; faux verdict textualisé non évalué |
| TD3 Q6 | Deux cas personnels contrastés, attente et observation, règle humaine | 2 sources/citations non vides ; inclusion exacte ; bools typés ; un vrai/un faux | Exact pour tests ; choix Faguet et règle restent humains |
| TD3 Q7 | Au moins trois concordances d'un pivot, positions, proposition | >=3 fenêtres distinctes retrouvées contenant pivot G1/G2 | Bugs **une occurrence sous trois fenêtres** (TD03-02), fin hors borne (TD03-01) ; interprétation humaine |

### TD4–TD7 : 28 questions

| TD/Q | Travail demandé et microcas contrôlé | Valeurs vérifiées indépendamment | Couverture automatique / humaine | Verdict |
|---|---|---|---|---|
| 4/1 | Marges de présence sur 4 contextes, répétition chat ignorée dans une phrase | chat=2, livre=2, N=4 | 3 entiers ; fonction marge, liste vide et Faguet à relire | Conforme au microcas |
| 4/2 | Paires booléennes chat/livre/plume | chat_livre=1, chat_plume=1, livre_plume=0 | 3 entiers ; assert de symétrie/bornes, pivot absent et preuves non contrôlés | Conforme au microcas |
| 4/3 | Somme des deux paires et union des contextes | somme_paires=3, union=2 | 2 entiers ; généralité cooc_union et lecture ligne Gemini humaines | Conforme au microcas |
| 4/4 | Paires de positions chat 0,4 et livre 3, fenêtres 1 et 3 | k1=1, k3=2 | Comptages ; liste des paires, refus k<1, préservation flux Faguet non contrôlés | Conforme au microcas |
| 4/5 | Deux phrases mono-token, concaténation versus frontière | sans_frontiere=1, dans_phrase=0 | 2 entiers ; frontières corpus et paragraphes humains | Conforme au microcas |
| 4/6 | Référence manuelle chat/chats/chaton, formes versus lemmes | formes_chat=1, lemmes_chat=2 | Comptages sur référence indépendante spaCy ; cinq annotations et expressions Faguet humaines | Conforme au microcas |
| 4/7 | Synthèse microcorpus Q1 chat–livre | N=4, cooc=1, marge_pivot=2, marge_associe=2 | 4 entiers ; composition des fonctions, corpus vide, export/provenance humains | Conforme au microcas |
| 5/1 | N=8, marge pivot3, associé4, commun2 | conditionnelle=0.666667, base=0.5 | Quotients arrondis ; huit cases et provenance humains | Conforme au microcas |
| 5/2 | N=12, pivot4 ; A marge9 commun3 ; B marge2 commun2 | A=0.75, B=0.5, base_A=0.75, base_B=0.166667 | Quatre ratios ; comparaison relative et contexte non notés | Conforme au microcas |
| 5/3 | 4/100 et 8/400 pour mille | court=40.0, long=20.0 | Taux ; dénominateur nul et moitiés Faguet non contrôlés | Conforme au microcas |
| 5/4 | Inversion conditionnelle 2/3 versus2/4 | associe_sachant_pivot=0.666667, pivot_sachant_associe=0.5 | Quotients ; tableau2×2 et fonction paramétrée non contrôlés | Conforme au microcas |
| 5/5 | Absence du pivot versus absence de l'associé | sans_pivot=null, sans_associe=0.0 | null distingué de zéro ; petits effectifs et inspection humaine | Conforme au microcas |
| 5/6 | Positions pivot0,4 et associé3 ; proportion de pivots couverts | k1=0.5, k3=1.0 | Deux ratios, bien distincts du nombre de paires TD4 ; fenêtres Faguet humaines | Conforme au microcas |
| 5/7 | Trace avec numérateur, dénominateur, proportion | effectif=2, denominateur=3, proportion=0.666667 | Nombres exacts ; réutilisation de fonction, export et conclusion non notés | Conforme au microcas |
| 6/1 | Positions de cible dans flux4 tokens | positions=[1,3], relatives=[0.25,0.75] | Indices et rapports ; dispersion3pivots, légende, passages humains | Conforme au microcas |
| 6/2 | 8tokens découpés en4segments contigus2tokens | effectifs=[2,0,0,1], tailles=[2,2,2,2] | Listes ordonnées ; fonction générale sur11tokens, bornes et conservation humains | Conforme au microcas |
| 6/3 | Chat/plume dans segments de2 et4tokens | chat=[500.0,250.0], plume=[0.0,250.0] | Matrice numérique2×2 ; imshow, échelle commune, Faguet et lecture humains | Conforme au microcas |
| 6/4 | Paires chat positions0,3 et livre2, fenêtres1,2,3 | k=[1,2,3], cooc=[1,2,2] | Fenêtres et nombres exacts ; courbes Faguet, distinction couverture humaine | Conforme au microcas |
| 6/5 | Contexte autour de plume index3, marge1, flux5 | debut=2, fin=5, contexte='puis plume après' | Tranche/texte exacts ; retour original Faguet et token.idx humains | Conforme au microcas |
| 6/6 | Reprise des taux chat Q3, libellés | etiquettes=['segment 1','segment 2'], valeurs=[500.0,250.0] | Données uniquement ; liaison réelle aux calculs, barres et matrice cooccurrence non certifiées, annoncé | Conforme au microcas |
| 6/7 | Agrégation numérateurs/tailles (éviter moyenne des taux) | effectif=2, taille=6, pour_mille=333.333333 | Taux global correct ; export/figures et deux paragraphes humains | Conforme au microcas |
| 7/1 | Définition incomplète, quatre champs dans ordre prescrit | mesurable=false, manquants=['unite','fenetre','normalisation','agregation'] | Ordre+bool strict ; six lignes réelles et protocoles proposés humains | Conforme au microcas |
| 7/2 | Moteur union sur4contextes, chat–livre | N=4, cooc=1, marge_pivot=2, marge_associe=2 | Nombres ; indicespreuves/expressioncontiguë/casFaguet non contrôlés | Conforme au microcas |
| 7/3 | 'preuve vient' dans 'La preuve vient du texte.', varianteabsente | exacte=true, debut=3, fin=15, alteree=false | Bool et offsets corrects (fin exclue) ; trois citations Faguet humaines | Conforme au microcas |
| 7/4 | Valeur3 puis5 comparées à[2,4] | dans_intervalle='compatible selon le protocole', hors_intervalle='contredit selon le protocole' | Libellés exacts ; bornes inclusives et garde protocole non testés automatiquement | Conforme au microcas |
| 7/5 | chat associé à livre/plume,3contextes | somme_paires=3, union=2 | Comptages ; six lignes, variantes, visualisation et provenance humaines | Conforme au microcas |
| 7/6 | Nouveau corpus5contextes,livre–plume | N=5, cooc=2, marge_pivot=3, marge_associe=3 | Second cas correct ; invariance du moteur, lot voisin et caslimites non certifiés | Conforme au microcas |
| 7/7 | Deux protocoles annonce[0,2],communchat–livre1 | indefini='insuffisamment défini', defini='compatible selon le protocole' | Statuts corrects ; appels réels, export6lignes/3citations/lotmanuel et synthèse humains | Conforme au microcas |

### Contrôles TD1–TD4 : 28 questions

| Contrôle/question | Attendu par l'énoncé | Vérification réelle | Limites / verdict |
|---|---|---|---|
| C1 Q1 | Lecture UTF8, caractères, split original, fréquences minuscules, formes, fonction et commentaire | Valeurs exactes sur corpus fixe ; dictionnaire complet et types stricts | Conforme calculs. Lecture fichier/fonction/commentaire humains. Feedback privé ambigu « split en minuscules » (C14-06). |
| C1 Q2 | Tous tokens spaCy, annotations, offsets, audit manuel de cinq tokens | Ordre, couverture du texte hors blancs, restitution par tranches, champs/types, POS autorisés, flags structurels | Conforme cohérence. Lemme/POS/tag/mot_vide/prédictions et segmentation lexicale ne sont pas certifiés. |
| C1 Q3 | Phrases exactes + positions + tailles et somme, abréviation personnelle | Couverture source par intervalles, tailles liées aux annotations Q2 et total exact | Conforme cohérence ; frontières linguistiques humaines, segmentation en une grande phrase peut passer. Q2 manquante induit zéro (C14-03). |
| C1 Q4 | Trois listes de lemmes selon NOUN, VERB, contenu filtré, ordre et répétitions | Égalité exacte aux listes dérivées des annotations Q2 | Conforme ; vérité des annotations humaine ; dépendance Q2. |
| C1 Q5 | displaCy phrase2, verbe principal, dépendant direct, relation et lecture | Deux tokens distincts localisés en phrase2 ; verbe VERB/AUX ; chaîne relation non vide | Conforme au seul critère annoncé « repères » ; ni tête réelle, ni arc, ni principal, ni rendu certifiés. Dépendance Q2. |
| C1 Q6 | Nouveau corpus transport, annotations et 3 comptages, analyse différences | Couverture source transport ; split exact ; tokens et lexicaux cohérents avec flags | Conforme cohérence, indépendant du musée ; sémantique des flags humaine. |
| C1 Q7 | Fonction bilan réutilisable sur musée/transport/météo/vide | 4 identifiants uniques, caractères/split exacts, annotations, tokens exacts ; phrases bornées et vide0 | Conforme portée annoncée ; nombre effectif de phrases seulement borné ; fonction générale humaine. Ordre des bilans libre malgré texte demandant un ordre (tolérance sans erreur de résultat). |
| C2 Q1 | Lire corpus atelier, annotation complète, nb phrases/tokens séparés, 5 contrôles manuels | Caractères exacts + couverture/positions/champs annotations | Conforme trace prévue ; phrases/tokens affichés hors trace et contrôle linguistique humains. |
| C2 Q2 | Deux fonctions fréquences noms/verbes, minuscules, exclusions optionnelles | Dictionnaires complets exacts dérivés de Q1, filtres NOUN/VERB/stop/ponctuation/espace | Conforme cohérence ; fonction/Counter/réutilisabilité humains, dépendance Q1. |
| C2 Q3 | Exclusion atelier, avant/après, contrôle totals et interprétation | Exclusion ['atelier'], dictionnaires avant/après exacts depuis Q1 | Conforme ; commentaire humain ; dépendance Q1. |
| C2 Q4 | POS hors ponctuation/espace, top3 décroissant ex aequo libres | Comptages exacts depuis Q1, valeurs/liste/classement, unicité, ex aequo libres | Conforme ; Q1 amont requise. |
| C2 Q5 | Fonction sur annotations port manuelles, noms/verbes/union/exclus/vide | Cinq dictionnaires fixés exacts et types stricts | Conforme déterministe indépendant de spaCy ; paramétrabilité humaine. |
| C2 Q6 | Deux figures mêmes données Q3, random_state42, axes et analyse | Dictionnaire exact des noms filtrés recalculé depuis Q1 | Conforme données ; rendu/présence/seed figures et interprétation humains ; dépendance Q1 et non traceQ3. |
| C2 Q7 | Fonction générale sur alimentation, fréquences, vide, comparaison fonctions et expression | Couverture corpus nouveau, trois dictionnaires selon annotations, vide{} | Conforme cohérence ; fonction/équivalence avec spécialisées/expression humains. |
| C3 Q1 | Périmètre + caractères/split/formes + citations IDs ordre donné | Mesures exactes source et IDs exacts | Conforme ; provenance/question documentaire humaines. |
| C3 Q2 | Concordances non chevauchantes plan largeur12, absent musée, fonction rejet motifvide | Toutes positions, pivot, contextes exacts, absent[] | Conforme déterministe ; fonction et refus motifvide vérifié en Q6 via trace. |
| C3 Q3 | Fragment, token forme, token lemme plan + PhraseMatcher LOWER comptes rendus | Fragment/forme/expression exacts par spans ; liste lemme non vide, offsets vrais ordonnés | Conforme portée explicitée ; regex de référence sur corpus fixe équivaut aux formes visées ; lemmes pertinents/complétude/méthode PhraseMatcher humains. « Le » comme faux lemme peut passer : abstention linguistique, pas validation sémantique. |
| C3 Q4 | Recherche citations exactement, premier index/-1 et bool | Texte citation inchangé, premier index exact, bool typé pour 4 IDs ; ordre IDs libre | Conforme déterministe. |
| C3 Q5 | Normaliser apostrophe, espaces, casse ; recherche et candidats P2/P3 originaux | Résultats normalisés exacts ; 2 IDs candidats, tranches exactes non vides | Conforme portée limitée ; pertinence des candidats/verdict humain (même passage sans rapport peut passer). |
| C3 Q6 | Prédictions et tests T1–T4, repeated/includes/empty source/empty motif ValueError | Résultats exacts sur 4 tests + bool erreur attendu ; ordre IDs libre | Conforme traces ; l'existence effective de raise/catch/production autonome n'est pas démontrée. |
| C3 Q7 | Transfert radio, fragment port largeur10, forme port, citations + rapport | Concordances exactes, spans de mots entiers, citations/indices/bools exacts | Conforme déterministe ; hypothèse lemme et rapport humains. |
| C4 Q1 | Fréquences occurrences, N fiches, marge bus | Dictionnaire et N/marge exacts recalculés corpus fixe | Conforme ; fonction paramétrable et unités rédigées humaines. |
| C4 Q2 | Cooccurrence/marges/N/preuves bus-retard et bus-accès, tests symétrie/absent/bornes | Deux mesures complètes exactes et indices ordonnés | Conforme ; tests secondaires non dans trace, relus humainement. |
| C4 Q3 | Somme paires vs union, indices union et chevauchement, intitulés | Quatre valeurs/listes exactes | Conforme ; protocole/intitulés humains. |
| C4 Q4 | Paires positionnelles k1/k3, ponctuation conservée, ordre i puis j, bornes et invalides | Effectifs et listes complètes exacts k1/k3 | Conforme ; validation k<1/absent/frontière seulement relecture code et tests. |
| C4 Q5 | Fiche vs dossier, indices dossiers, phrases spaCy et unités | Comptages fiche/dossier et indices/N dossiers exacts | Conforme ; affichage/positions phrases et justification humains. |
| C4 Q6 | Formes/lemmes retard relevé manuel, expressions contiguës, audit spaCy4tokens | Deux effectifs exacts, tous couples séquence-début ordonnés | Conforme ; annotation et contrôle manuel relus humainement. |
| C4 Q7 | Transfert archives voix-bruit/union/somme/expression + export relu + bilan | Mesures/preuves exactes sur nouveau corpus | Conforme ; fichier export/relecture/bilan/concordance supplémentaire humains. |

### Contrôles TD5–TD7 : 21 questions

| Question | Consigne mesurable et valeurs clés | Critère effectivement appliqué | Couverture exclue du score automatique | Verdict |
|---|---|---|---|---|
| C5 Q1 (2 pts) | Présences par fiche visite–audio : N=10, marges 4/7, commun=3, indices [0,1,2] | Égalité typée du dictionnaire calculé par `pair` | Réutilisabilité, affichage des fiches, distinction avec visiteurs : humain | Conforme |
| C5 Q2 (3 pts) | Proportions 3/4 et 3/7 ; contingence [[3,1],[4,2]] | Quotients avec tolérance et matrice entière exacte | Phrases d’interprétation et populations : humain | Conforme |
| C5 Q3 (3 pts) | Audio : 3,7,.75,.7,.05 ; atelier : 2,2,.5,.2,.3 | Les cinq champs de chacun des associés recalculés | Lecture de contexte et réserve de généralisation : humain | Conforme |
| C5 Q4 (3 pts) | Sections : 3/10×1000=300 ; 5/25×1000=200 ; global 8/35×1000 | Effectifs et tailles entiers, taux numériques | Commentaire des classements : humain | Conforme |
| C5 Q5 (3 pts) | Sans pivot=None ; sans cooccurrence=0 ; rareté=1/1 | Distinction `None`/zéro, booléens rejetés comme nombres | Fonction sur corpus vide et portée de n=1 : humain | Conforme |
| C5 Q6 (3 pts) | Pivots [0,4,8] ; k1 couvre [0], k2/k4 tous ; 5 paires k4 | Indices, nombres, proportion et total de paires | Cas terme absent supplémentaire, preuves et interprétation de k : humain | Conforme |
| C5 Q7 (3 pts) | Littoral : N=8, marges4/5, commun2 ; .5/.4 ; bases .625/.375 ; table [[2,2],[3,1]] | Tous les champs de trace recalculés sur le second corpus | Export/relecture, annotations, synthèse et réemploi fonctions : humain | Conforme |
| C6 Q1 (2 pts) | Flux48 ; positions affiche [1,10,19,40], public[7,16,25,37], atelier[13,22,34,43] ; i/48 | N, positions entières et relatives exactes/arrondies | Dispersion réelle, axe et interprétation : humain | Conforme |
| C6 Q2 (3 pts) | Bornes 0/12/24/36/48 ; tailles flux12 et alpha10 ; séries d’effectifs | Égalité des bornes, tailles et tableaux | Discussion des frontières et absence de sens thématique : humain | Conforme |
| C6 Q3 (3 pts) | Taux pour mille : affiche[200,100,0,100], public[100,100,100,100], atelier[0,200,100,100] | Matrice des trois séries, dénominateurs alphabétiques | Carte, unité, échelle commune et lecture d’une case : humain | Conforme |
| C6 Q4 (3 pts) | Fenêtres[1,3,6], paires public[0,3,6], atelier[0,3,5], couverture=1 | Comptages positionnels, paramètres, proportion | Paires détaillées conservées comme preuves, courbes, axes et commentaire : humain | Conforme |
| C6 Q5 (3 pts) | Concordances première/dernière affiche ; caractères [0:23] et [208:231] | Les deux dictionnaires, bornes et passages originaux exacts | Annotation spaCy et correspondance avec figure : humain | Conforme |
| C6 Q6 (3 pts) | Matrice [[0,2,1],[2,0,1],[1,1,0]], ordre fourni, preuves [1,6] | Matrice, ordre des termes, indices | Figure, légende et comparaison des représentations : humain | Conforme |
| C6 Q7 (3 pts) | Second flux29, segments [0:9],[9:19],[19:29], alpha8 chacun, formes exactes (sans pluriels), taux globaux125 | Bornes, tailles, comptes, taux segmentaires et globaux, moyennes | Figures, exports et interprétation liée aux passages : humain | Conforme ; limite pédagogique L02 |
| C7 Q1 (2 pts) | M1,M2,M4 mesurables ; M3 manque agrégation | Liste ordonnée, ids, clés manquantes et vrais booléens | Tableau détaillé et séparation original/convention : humain | Conforme |
| C7 Q2 (3 pts) | Mesures union M1…M4 : communs2,2,4,2 avec marges et indices | Expressions contiguës, alternatives en union, présence au plus1/contexte | Moteur paramétrable, annotation et preuves textuelles : humain | Conforme |
| C7 Q3 (3 pts) | C1 exacte [174:205], C2 absente, C3 seulement normalisée | Exactitude, offsets, recherche minuscule/espaces distincte | Analyse documentaire des différences/candidats : humain | Conforme |
| C7 Q4 (3 pts) | M1 compatible ; M2/M4 contredits ; M3 insuffisamment défini | Libellés exacts calculés sur protocole original ; bornes inclusives | Essais supplémentaires des bornes et intervalle inversé : humain, pas dans trace | Conforme ; limite L01 |
| C7 Q5 (3 pts) | Union4 vs somme5 ; expression[1,6], mots[1,3,6], faux[3] ; silence singulier1/groupe2 | Sept champs calculés, pas d’assimilation livraison/livre | Matrice et figure demandées au point4, contextes multipaires : humain | Conforme |
| C7 Q6 (3 pts) | Jardin union2, marges4/5,N7, conditionnelle.5 ; somme3 ; expression1 ; vide et indéfinis | Valeurs complètes dont `None` et mesures corpus vide | Généralité moteur, référence manuelle et limites d’annotation : humain | Conforme |
| C7 Q7 (3 pts) | Jardin J1 compatible2, J2 contredit1, J3 insuffisamment défini ; citation[108:121] | Mesures et verdicts séparés, citation exacte | Dossier/export, original conservé, relecture du fichier, figure et synthèse : humain | Conforme |

## Relais et conclusion de gouvernance

Les auditeurs techniques concluent `REQUEST_CHANGES` pour les défauts transversaux
et TD0–TD3 ; les valeurs numériques TD4–TD7 et C4–C7 sont acceptables dans leur
portée déclarée. Le Pedagogy-Reviewer rend `REQUEST_CHANGES` sur la présentation du
score, les dépendances et la relecture ; **COUVERTURE_PÉDAGOGIQUE_CONSERVÉE** pour
cette mission de revue sans transformation du contenu.

Le périmètre documentaire et la séparation des rôles sont conformes. La production
reste à corriger selon les lots ci-dessus. Fusion, barèmes et déploiement restent
sous décision du mainteneur. Aucun code étudiant exécuté, aucune modification
produit, aucune fusion ni mise en production effectuée par cet audit. Une future
PR mixte devra apporter sa matrice de couverture et ses revues propres : le présent
rapport n'est pas une approbation anticipée de ses modifications.
