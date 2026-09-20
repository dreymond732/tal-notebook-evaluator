# S3 — Construire un audit quantitatif d’une analyse LLM

## Statut, objectif et périmètre

**Décision enseignante :** progression proposée puis approuvée le 20 septembre 2026, huit TD de deux heures, plusieurs exemples par séance. **Référence préalable :** [matrice source → cible](S3_COVERAGE_MATRIX.md). Les TD0–TD2 existants sont renforcés ; TD3–TD7 réalisent la nouvelle finalité. R0–R2 restent disponibles sans modification.

**Objectif terminal :** à partir d’un corpus et d’une analyse produite par un LLM, construire un dispositif reproductible qui vérifie les fréquences, les cooccurrences et les citations, mesure l’effet des choix de traitement et justifie ses conclusions par des traces et des passages sources.

Le dispositif doit aussi vérifier ses propres calculs. Un résultat du modèle linguistique spaCy n’est pas une vérité d’évaluation, et une différence avec Gemini n’est pas automatiquement une erreur de Gemini. Une mesure mal définie peut rester non comparable.

Compétences observables : définir une unité ; préserver le corpus ; calculer de manière reproductible ; valider un instrument sur un petit cas indépendant ; distinguer chiffre, inférence et interprétation ; présenter un verdict proportionné aux preuves. Le produit est un instrument d’audit et un rapport argumenté, pas une démonstration imposée de l’échec des LLM.

## Données et provenance

Le texte `feminismeFaguet` et le document de réponses Gemini viennent de l’archive fournie par l’enseignant. Le document rapporte une conversation du 18 septembre 2026, avec trois prompts successifs : analyse lexicométrique, tableau de cooccurrences, puis ajout d’estimations quantitatives. **Il ne s’agit pas de trois modèles, de trois répétitions indépendantes ou d’une comparaison expérimentale.** Le nom exact de version du modèle Gemini n’est pas fourni ; ne pas l’inventer.

Conserver les octets du texte original, le document source et l’extraction textuelle séparément ; documenter empreintes, extraction, encodage et normalisations. Ne pas substituer silencieusement la version Gutenberg actuelle au fichier effectivement analysé. La mention bibliographique de Gutenberg provient du prompt ; la provenance de cette édition doit rester distincte du fichier nettoyé transmis.

Les six lignes du dernier tableau sont transcrites sans transformer les fourchettes en valeurs exactes :

| Pivot annoncé | Associés annoncés | Fourchette annoncée |
|---|---|---:|
| Intelligence | inaptitude, aptes, également, professions, génie | 15–20 |
| Aptitude(s) | professions, capacité, instincts, métier | 12–18 |
| Raison / Bon sens | rationnelle, logique, droit, précision, équité | 25–35 |
| Devoir | travail, règle, femme forte, sacrifice, conscience | 10–15 |
| Morale / Vertu | haute moralité, saine, probité, moralisation, dépravation | 15–22 |
| Exception | généralité, infinitésimale, type, rare | 8–12 |

Les paramètres absents sont des données de l’audit : fenêtre, forme/lemme, traitement des expressions et variantes, sens de la relation, comptage de positions ou de contextes, union ou somme. Une convention choisie par l’étudiant doit porter l’étiquette **reconstruction de l’auditeur**, jamais être attribuée rétrospectivement au LLM.

## Contrat scientifique de mesure

1. **Forme :** chaîne observée, éventuellement normalisée en minuscules selon le protocole. **Lemme :** annotation du modèle ; un adjectif et un nom apparentés ne constituent pas nécessairement le même lemme. **Famille thématique :** liste construite et justifiée, distincte de la lemmatisation.
2. **Expression :** suite contiguë de tokens sous convention déclarée ; ne pas chercher `bon sens` comme un token ni `raison` comme sous-chaîne de n’importe quel mot. Les apostrophes, traits d’union et expressions chevauchantes demandent une décision.
3. **Cooccurrence de référence :** une phrase contenant au moins une occurrence de chacun des deux termes compte une fois pour cette paire. La répétition d’un terme ne multiplie pas le nombre de phrases. La variante paragraphe applique la même logique à un autre contexte.
4. **Fenêtre :** distance absolue entre indices de tokens, borne incluse `<= k`, avec règle explicite de ponctuation et franchissement des phrases. Les paires de positions et les contextes booléens sont des mesures différentes ; ne pas comparer leurs effectifs comme s’ils étaient interchangeables.
5. **Plusieurs associés :** conserver les comptes par paire, leur somme et le nombre de contextes où apparaît le pivot avec au moins un associé. La dernière quantité est une union ; elle ne vaut généralement pas la somme.
6. **Marges :** sur le même univers de N contextes, le compte conjoint ne dépasse aucune marge ; la table 2 × 2 est non négative et totalise N. Une proportion conditionnelle avec dénominateur nul est indéfinie, pas zéro par défaut.
7. **Normalisation :** le dénominateur appartient au résultat. Des occurrences pour mille tokens lexicaux et des phrases contenant un terme pour cent phrases ne mesurent pas la même chose.
8. **Association :** fréquence conjointe et force d’association sont distinctes. La PMI est un prolongement après définition des probabilités et du logarithme ; faibles effectifs et compte nul doivent être explicités. Elle n’est pas requise pour terminer TD7.
9. **Citations :** conformité exacte, conformité sous normalisation déclarée, candidat approché et interprétation sont quatre statuts différents. Un candidat de recherche approchée exige une lecture humaine ; ne pas produire une similarité qui certifie automatiquement l’authenticité.
10. **Lecture distante :** toute figure conserve son tableau source et des coordonnées permettant le retour aux passages. Un segment mécanique du texte n’est pas appelé chapitre. Ni proximité ni fréquence ne prouvent l’adhésion de l’auteur à une opinion qu’il peut rapporter ou discuter.

## Organisation des huit séances

Les budgets ci-dessous sont **prévisionnels**, installation et synthèse comprises ; ils ne proviennent pas d’une observation en classe. Les prolongements identifiés comme facultatifs sont hors budget. Chaque séance comporte au moins trois exemples sur d’autres données, une prédiction avant calcul, une modification et un transfert ; les exemples ne livrent pas les sorties du travail demandé.

| Séance | Prérequis réactivés | Acquis et productions obligatoires | Budget en minutes |
|---|---|---|---|
| TD0 — Du texte à la mesure | S1 fichiers, chaînes, collections, fonctions ; R0 si blocage | Lire en UTF-8 ; conserver liste et nombre ; formes distinctes ; fonction de fréquence ; minuscules ; limites split/lemme. Petit cas vérifié à la main et trace des conventions. | 10 préparation + 25 Q1–Q3 + 30 Q4–Q5 + 20 Q6 + 25 Q7 + 10 export = 120 |
| TD1 — Annoter et retrouver les unités | TD0 ; réactiver boucle et filtre ; R1 au besoin | Doc, formes/lemmes/POS/tag et positions ; phrases et longueurs ; listes noms/verbes ; lecture displaCy ; comparaison split ; extrait personnel. Contrôle manuel des annotations. | 15 préparation + 20 Q1 + 15 Q2 + 20 Q3 + 15 Q4 + 15 Q5 + 15 Q6 + 5 export = 120 |
| TD2 — Construire les objets comptés | TD1 ; R2 au besoin ; fonctions à paramètres | Corpus, Counter, fonctions noms/verbes, exclusions ; POS/top3 ; cinq lemmes contrôlés et expression ; WordCloud ; fonction générale. Fréquences normalisées et effet des unités. | 10 préparation + 10 Q1 + 20 Q2 + 15 Q3 + 10 Q4 + 15 Q5 + 15 Q6 + 20 Q7 + 5 export = 120 |
| TD3 — Retrouver les preuves | Indices, tranches, tokens et phrases | Concordances avec positions ; expressions ; citations exactes et normalisées ; lot d’annotation manuelle et erreurs ; candidat approché optionnel ; export et retour au corpus. | 10 préparation + 10 Q1 + 20 Q2 + 15 Q3 + 15 Q4 + 15 Q5 + 15 Q6 + 15 Q7 + 5 export = 120 |
| TD4 — Compter les cooccurrences | TD3 localiser ; TD0 fonctions ; TD1 phrases | Contextes booléens ; marges ; compte conjoint ; répétitions/union/somme ; paragraphes et fenêtres ; cas limite ; preuves sur Faguet et export réutilisable. | 8 préparation + 12 Q1 + 14 Q2 + 14 Q3 + 17 Q4 + 15 Q5 + 18 Q6 + 16 Q7 + 6 bilan = 120 |
| TD5 — Comparer les associations | TD4 comptes conjoints/marges ; division et conditions | Univers commun ; table 2 × 2 ; proportions conditionnelles ; compte/force ; normalisation ; sensibilité ; commentaires fondés sur effectifs et incertitudes de méthode. | 8 préparation + 12 Q1 + 14 Q2 + 14 Q3 + 17 Q4 + 15 Q5 + 18 Q6 + 16 Q7 + 6 bilan = 120 |
| TD6 — Visualiser et revenir au texte | TD3 concordances ; TD4–TD5 tableaux ; TD2 Matplotlib | Dispersion ; segments et dénominateurs ; carte de chaleur ; matrice cooccurrences ; retour aux occurrences ; sensibilité aux conventions ; export des données et des figures. | 8 préparation + 12 Q1 + 14 Q2 + 14 Q3 + 17 Q4 + 15 Q5 + 18 Q6 + 16 Q7 + 6 bilan = 120 |
| TD7 — Auditer une analyse LLM | Modules TD0–TD6 validés ; aucun nouveau modèle nécessaire | Formaliser six lignes Gemini ; reconstruire plusieurs protocoles ; réutiliser les calculs ; contrôler citations ; éprouver sur cas non utilisé ; rapport et traces. | 8 préparation + 12 Q1 + 20 Q2 + 14 Q3 + 12 Q4 + 16 Q5 + 14 Q6 + 18 Q7 + 6 bilan = 120 |

Les cellules de préparation peuvent fournir les imports, corpus et dispositifs d’enregistrement pour réserver le temps au raisonnement. Elles ne fournissent pas les fonctions évaluées. Si les fichiers de la séance précédente manquent, un point de reprise fournit les données et contrats d’entrée, sans remplir le calcul attendu. Le corpus complet sert au transfert après validation sur les microcas.

## Fiches de réalisation par séance

### TD0 — Diagnostic et premières conventions

Exemples possibles : lecture d’un fichier de trois lignes ; répétitions `rouge/bleu/rouge` ; effet de `Livre/livre/livre.`. Travail étudiant sur un autre vocabulaire. Q1 mesure les caractères, Q2 montre la liste split, Q3 son effectif, Q4 les formes distinctes, Q5 le dictionnaire brut, Q6 sa variante minuscules, Q7 les limites et la convention. Une réponse de commentaire n’est pas reconnue juste par la seule présence de mots tels que « ponctuation ». Le dictionnaire de fréquence devient un module réutilisable.

### TD1 — Annotation comme hypothèse contrôlable

Exemples distincts : une flexion verbale ; une apostrophe ou ponctuation ; une phrase annotée dont le sujet peut être identifié à la lecture. Le tag dépend du modèle : il n’est pas promis plus informatif que POS dans chaque cas. Les positions sont testées par `texte[debut:fin]`, ce qui relie l’annotation au fichier. La comparaison de segmentation et l’extrait autonome restent obligatoires. Ne pas prendre un modèle volumineux simplement pour préparer une similarité non utilisée.

### TD2 — Le mot à compter n’est pas donné d’avance

Exemples distincts : Counter sur un lexique de couleurs ; exclusion d’un mot générique dans un mini-corpus ; deux textes de tailles différentes avec le même effectif. Conserver les fonctions spécialisées puis leur généralisation. Comparer forme, lemme et regroupement déclaré ; contrôler une expression composée sans l’assimiler à un lemme. Vérifier cinq annotations à la main. Le nuage doit susciter une question et une vérification, sans prétendre mesurer une importance conceptuelle.

### TD3 — Un chiffre doit conduire à ses preuves

Exemples distincts : concordance sur une chaîne courte ; expression de deux tokens ; citation avec accent, apostrophe ou substitution. Le lot de validation comprend présence, absence, répétition, bord du texte et correspondance trompeuse par sous-chaîne. L’étudiant écrit la recherche et expose ses résultats ; une interface fournie ne remplace pas cette activité. Conserver les références de phrase/paragraphe et les positions du texte d’origine.

### TD4 — Plusieurs définitions, plusieurs nombres

Exemples distincts : trois phrases où un mot est répété ; un contexte contenant deux associés ; une paire à la distance exacte de la fenêtre. L’étudiant compte d’abord sur papier et transforme ensuite cette convention en fonction. Tester vide, absence, répétition, symétrie des paires et frontière incluse. Une même phrase peut contribuer à plusieurs paires, mais une fois seulement à leur union. Exporter paramètres et preuves avec les comptes.

### TD5 — Interpréter les relations quantitatives

Exemples distincts : événement conjoint fréquent mais associé à un pivot très fréquent ; petit effectif produisant un grand taux ; marge nulle. Les marges et les comptes doivent provenir du même découpage et du même corpus. Les résultats ne sont pas décrits comme significatifs sans test approprié ; la séance ne suppose pas un cours complet de statistique inférentielle. PMI en approfondissement clairement séparé, avec formule, convention logarithmique et prudence sur les faibles effectifs.

### TD6 — Visualiser une mesure, pas seulement décorer

Exemples distincts : même fréquence répartie ou concentrée ; sections inégales donnant des classements inversés avant/après normalisation ; changement de fenêtre transformant une relation. Les graphiques portent unité, corpus et paramètres ; la carte a une échelle lisible et le réseau n’est pas requis. Chaque assertion visuelle est reliée à au moins un passage. Une absence graphique doit être distinguée d’un zéro réel ou d’une donnée manquante.

### TD7 — Instrument et jugement d’audit

Six lignes du tableau Gemini sont couvertes, avec les familles lexicales exactement annoncées avant toute reconstruction. Au moins un cas contrôlé nouveau sert à éprouver l’instrument. Le rapport sépare : texte de l’affirmation ; paramètres disponibles/manquants ; convention reconstruite ; résultat mesuré ; preuve ; verdict ; limite. Comparer un nombre reconstruit à une fourchette est possible mais ne prouve pas que cette convention est celle du LLM. Le cas `naturally/naturellement` illustre une vérification de citation, sans généraliser cette erreur à toutes les affirmations. Les notes, les six lignes du tableau d’audit et les traces d’export se construisent progressivement pendant Q1–Q6. Q7 assemble ces éléments et demande une synthèse de **200 à 300 mots**, dans ses 18 minutes prévues ; il ne demande pas de refaire l’ensemble de l’audit en fin de séance.

## Évaluation formative et remise finale

**CHANGEMENT_DE_CONTRAT :** les supports S3 deviennent une progression d’audit et utilisent des traces JSON explicites. Pour chaque question, le notebook conserve `print("S3_TDn_Qm:", json.dumps(resultat_qm, ensure_ascii=False))`. Le moteur lit les sorties enregistrées et ne doit jamais exécuter le code étudiant. TD0 possède sept traces et sept exercices (les deux tâches de l’ancien exercice 2 sont désormais séparées), TD1 six traces et TD2 sept ; les nouveaux TD3–TD7 ont sept traces.

La grille automatique distingue contrôles numériques sur données fixées et contrôles structurels. Une structure présente ne prouve ni la qualité d’une interprétation ni l’authenticité d’une sortie. Les commentaires et figures exigent une relecture humaine. Les tests de l’instrument sur microcorpus doivent être indépendants de la réponse LLM et de spaCy quand ils évaluent un simple calcul.

Pour la remise finale, examiner cinq dimensions : exactitude des calculs sur cas connus ; explicitation du protocole ; provenance et retour aux preuves ; sensibilité aux choix ; pertinence et prudence de la conclusion. Ne pas noter favorablement le seul nombre d’erreurs annoncées du LLM. Ne pas présenter le score formatif comme la note finale de cette qualité scientifique.

## Outils, ressources et limites

Python standard suffit au comptage et à la traçabilité ; spaCy annote le français, collections fournit Counter, Matplotlib et WordCloud couvrent les visualisations enseignées. Environnement de référence fixé : spaCy 3.8.7, modèle `fr_core_news_sm` 3.8.0, Matplotlib 3.9.2 et WordCloud 1.9.4 dans les séances concernées. Les préparations fixent aussi `typer==0.16.1` et `typer-slim==0.16.1` : cette contrainte de dépendances corrige une incompatibilité d’import observée avec spaCy 3.8.7 ; elle ne constitue pas une nouvelle compétence étudiante. Les versions effectivement installées doivent être conservées dans les exports. Ces choix stabilisent un environnement, sans prétendre choisir les dernières versions disponibles. Le pipeline français fonctionne sur CPU ; la disponibilité réseau et le téléchargement initial restent des contraintes à prévoir. Aucune API LLM payante ni clé personnelle n’est requise pour auditer les réponses déjà fournies.

Le modèle français est une annotation apprise à contrôler sur ce texte historique. Licence du logiciel, du modèle et du corpus sont des objets distincts ; conserver les notices des ressources et ne pas attribuer une licence inventée à l’export Gemini. Les rapprochements spaCy/Gemini ne sont pas un classement global de qualité des modèles.

Références techniques de cadrage (documentation spaCy consultée le 20 septembre 2026) : [annotations linguistiques spaCy](https://spacy.io/usage/linguistic-features), [recherche par motifs](https://spacy.io/usage/rule-based-matching), [modèles français](https://spacy.io/models/fr), [analyse de corpus dans TXM](https://txm.gitpages.huma-num.fr/txm-manual/analyser-un-corpus.html). Elles soutiennent l’outillage ; les constats sur Faguet/Gemini proviennent des fichiers fournis, pas de ces documentations.

## Acceptation et tutorat

Les huit séances doivent être exécutables dans l’ordre, proposer plusieurs exemples puis un travail non résolu, prévoir les 120 minutes, préserver la matrice et donner accès aux données. Les tests logiciels ne remplacent pas une séance pilote en classe. Les contrôles existants gardent le refus de toute assistance.

Chaque nouveau TD a un profil dans `tutor_sessions.json`, avec périmètres par exercice, réutilisation explicite des fonctions précédentes, bibliothèques limitées et notions introduites. Le contrat est synchronisé dans les métadonnées et une cellule Markdown dédiée en position zéro. Au S3, le tuteur questionne d’abord, ne résout pas sur demande, peut illustrer une seule notion avec un petit exemple distinct après échange, et ne modifie ni n’exécute les cellules. Sa présence n’est pas une garantie d’obéissance du service Colab.
