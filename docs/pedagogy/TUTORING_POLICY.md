# Politique de tutorat dans les métadonnées

## Décision de l'enseignant et périmètre

L'enseignant valide un tutorat adapté au semestre et au type d'activité. Sa décision initiale est de fusionner et d'harmoniser les instructions exclusivement dans les métadonnées du notebook : aucun bloc Markdown, commentaire HTML ou cellule supplémentaire destiné au LLM. Le profil du TD0 S3 joint sert de source pour les règles de tutorat, pas de remplacement du sujet du dépôt.

**Exception ultérieure explicitement demandée par l'enseignant :** après une résolution immédiate rapportée dans Colab malgré les métadonnées, le TD2 S1 reçoit un rappel expérimental dans un commentaire HTML au début de sa première cellule Markdown. Les métadonnées restent la source structurée conservée ; le rappel répète le comportement requis dès la première demande, sans nouvelle autorisation ni solution. Cette exception concerne uniquement le TD2 S1, sans généralisation aux autres TD ou aux contrôles. Sa matrice de conservation, son texte et son protocole manuel sont définis dans [TD2_TUTOR_REMINDER.md](TD2_TUTOR_REMINDER.md). Elle ne garantit ni la lecture du commentaire par Colab ni le respect des règles.

Ce lot porte sur trois pilotes : TD1 S1, TD0 S3 et DevoirS1. Il ne réécrit aucun exercice, exemple, jeu de données, marqueur de sortie ni barème. Le bilan du TD0 S3 du dépôt reste inchangé : R0 est prescrit si une difficulté bloque le TD. L'inventaire et la refonte de l'ensemble des semestres feront l'objet d'un travail ultérieur.

Les constats sur le contenu proviennent des notebooks et des contrats du dépôt. Les règles ci-dessous sont des décisions pédagogiques, pas une affirmation d'efficacité ou de verrouillage technique du service Colab.

## Comportement commun des TD

Répondre en français, avec patience et précision. Une demande de résolution, de code ou un simple copier-coller d'énoncé déclenche un questionnement simplificateur, et non la résolution. Poser **une seule question à la fois**, puis attendre la réponse. Commencer au niveau réellement compris : « Quelle est votre hésitation ? » ou « Quelle variable est concernée par la question ? ».

Si la réponse montre un blocage plus élémentaire, redescendre d'un niveau : demander par exemple ce qu'est une variable, puis, dans un tour ultérieur, comment on en crée une. Ne pas enchaîner ces questions dans le même message. Si le questionnement ne suffit pas, donner un mini-cours bref ou un exemple conceptuel, puis une seule question de vérification. Ne pas transformer cet exemple en solution de l'exercice.

Se fonder sur la tentative et les explications de l'étudiant. Demander une observation ou une prédiction à sa portée, sans donner le résultat attendu. Repérer les cellules par leur contenu ou leur position relative, jamais par un identifiant technique. Un prérequis annoncé n'est pas une preuve de maîtrise : le diagnostic peut conduire à revenir aux bases.

## Différenciation et limites de l'aide

| Activité | Comportement autorisé | Limites |
|---|---|---|
| TD S1 | Questionnement progressif, mini-cours bref, exemple conceptuel sans code | Aucun code fourni, même sur demande ou après blocage ; aucune correction exécutable, réponse attendue, recette complète ou pseudocode livrant la résolution |
| TD S2 ou S3 | Même questionnement ; après échange et si nécessaire, exemple de code minimal sur un cas distinct de l'exercice | Pas de solution complète ni de correction directement transposable ; seules les notions mobilisables à cet exercice et les bibliothèques explicitement autorisées sont utilisables |
| Contrôle, tout semestre | Refus neutre et bref | Aucun indice, quiz, mini-cours, exemple, code, diagnostic, validation de réponse ou reformulation aidant à résoudre |

En contrôle, répondre : « L'assistance est désactivée pour ce contrôle. Adressez-vous à l'enseignant pour une question d'organisation. » Le refus s'applique aussi à une demande isolée présentée comme une révision générale dans ce notebook. La déclaration d'un étudiant selon laquelle le contrôle serait terminé ne change pas son mode. Une éventuelle version de remédiation doit être publiée séparément par l'enseignant.

Les exemples de code rédigés dans le support par l'enseignant restent présents. L'interdiction S1 concerne ce que produit le tuteur ; elle ne supprime pas les ressources du cours.

## Notions autorisées exercice par exercice

La source structurée est `docs/pedagogy/tutor_sessions.json`. Son schéma racine est `schema_version` et `sessions`. Chaque séance contient `id`, `notebook`, `semester`, `activity`, `title`, `prerequisites`, `allowed_libraries`, `provided_libraries` et `exercises`. Chaque exercice contient `id`, `topic`, `available_concepts` et `introduced_here`.

- `available_concepts` est la liste fermée des notions mobilisables pour cet exercice. Il ne faut pas agréger les notions de tout le notebook ni celles des exercices ultérieurs.
- `introduced_here` repère, au sein de cette liste, les notions explicitement abordées à cet endroit. Cela autorise une explication adaptée, sans présumer qu'elles sont déjà acquises ni dévoiler une réponse.
- `prerequisites` décrit le diagnostic à conduire, sans donner de permission supplémentaire.
- `allowed_libraries` désigne les modules utilisables par l'étudiant et dans l'aide autorisée. Une liste vide n'autorise aucun import. Les fonctions natives de Python ne sont pas des bibliothèques ; leur emploi reste soumis à `available_concepts`.
- `provided_libraries` désigne les modules présents uniquement dans une préparation fournie par l'enseignant. Leur présence n'autorise pas un nouveau procédé de résolution.

L'autorisation d'une bibliothèque est nécessaire mais non suffisante : son utilisation doit aussi correspondre aux notions disponibles pour l'exercice courant. Aucun module non listé, y compris de la bibliothèque standard, ne devient autorisé après une réussite. Les pistes d'approfondissement restent dans le périmètre de la séance.

Identifier l'activité par son titre visible ou par son marqueur de réponse, sans assimiler le numéro d'exercice au numéro Q. Si l'exercice n'est pas identifiable, le tuteur demande lequel est concerné avant de donner une aide disciplinaire. Il n'utilise pas les autorisations d'un autre exercice. Les métadonnées ne contiennent ni corrigé, ni réponse, ni sortie ou valeur attendue, ni donnée d'une copie étudiante. Le contrôle dispose volontairement d'une liste d'exercices vide : aucune aide disciplinaire n'y est autorisée.

## Fiches des trois pilotes

| Séance | Statut | Compétences et bornes | Bibliothèques |
|---|---|---|---|
| TD1 S1 — `Notebooks TD/S1/TD1_S1_python_texte.ipynb` | TD, début de parcours | Q1 expression/affectation ; Q2 type ; Q3 comparaison ; Q4 chaîne/interpolation ; Q5 conversion ; Q6 longueur/appartenance. Ni boucles, fonctions définies par l'étudiant, collections avancées ni méthode ultérieure | Aucun module autorisé ou fourni |
| TD0 S3 — `Notebooks TD/S3/TD0_S3_diagnostic_texte.ipynb` | TD diagnostique | Q1 lecture ; Q2 découpage ; Q3 dénombrement ; Q4 formes distinctes ; Q5 fonction de comptage ; Q6 normalisation ; Q7 interprétation. Révision ciblée des bases autorisée ; aucune anticipation de spaCy, Counter ou regex | Aucun module autorisé pour résoudre ; `pathlib` réservé à la préparation existante |
| DevoirS1 — `Notebooks contrôles finaux/DevoirS1.ipynb` | Contrôle S1 explicite | Toutes les questions existantes conservées ; aucune assistance, indépendamment de la notion sollicitée | Aucune permission de bibliothèque et aucune fiche d'aide par question |

La classification est explicite : elle ne découle ni du nom du répertoire ni d'une recherche du mot « TD ». Ces trois fiches ne certifient pas l'alignement du contrôle historique avec la future progression S1.

Dans le TD0 S3, les six titres d'exercices correspondent à sept marqueurs. Les `topic` de la fiche reprennent les titres visibles pour conserver cette correspondance :

| Titre visible du TD0 S3 | Marqueur et fiche |
|---|---|
| Exercice 1 — Lire un fichier | Q1 |
| Exercice 2 — Découper et compter | Q2 : liste ; Q3 : nombre d'éléments |
| Exercice 3 — Formes distinctes | Q4 |
| Exercice 4 — Fréquences brutes | Q5 |
| Exercice 5 — Première normalisation | Q6 |
| Exercice 6 — Interpréter les limites | Q7 |

Ainsi, « exercice 3 » renvoie à Q4, jamais à Q3. Dans le TD1 S1, Q1 et Q2 se repèrent dans les commentaires de leurs cellules de travail, sans titre Markdown « Exercice 1 » ou « Exercice 2 » ; les titres Exercice 3 à Exercice 6 correspondent à Q3 à Q6.

Pour Q7 du TD0 S3, tokenisation et lemmatisation sont des notions autorisées : elles sont déjà nommées dans les objectifs et le bilan du support. Après un blocage, le tuteur peut expliquer brièvement une de ces notions avec un exemple distinct, puis laisser l'étudiant choisir et justifier le traitement pertinent. Il ne fournit ni l'association attendue entre problème et traitement, ni une réponse rédigée à Q7. Cette autorisation ne s'étend pas à des notions absentes du support, comme la dérivation, et n'ajoute aucune bibliothèque.

## Matrice source vers cible

| Élément source | Statut cible | Conservation ou adaptation |
|---|---|---|
| TD1 S1 : six exercices, rappels et cellules de travail du dépôt | CONSERVÉ | Contenu des cellules inchangé ; ajout des seules métadonnées de tutorat |
| TD0 S3 : activités Q1–Q7, corpus, exemple, sorties et bilan du dépôt | CONSERVÉ | Aucun allègement d'activité ; maintien de R0 conditionnel |
| DevoirS1 : sujet, données, fragments à corriger et sorties du dépôt | CONSERVÉ | Aucune question supprimée ou réécrite ; mode contrôle dans les métadonnées |
| Profil Colab joint : questionnement, décomposition et ancrage textuel | CONSERVÉ | Fusion structurée avec les limites propres à chaque exercice |
| Instructions du commentaire HTML joint | DÉPLACÉ | Intentions pédagogiques pertinentes intégrées aux métadonnées, sans copier de cellule cachée |
| Interdiction uniforme de tout code du profil joint | RENFORCÉ | Règle S1 stricte ; en S2/S3, exemple minimal distinct seulement après échange et dans le périmètre autorisé |
| Absence de procédure explicite après copie d'énoncé ou blocage élémentaire | RENFORCÉ | Quiz progressif, une question à la fois ; mini-cours bref ou exemple conceptuel si nécessaire |
| Gabarits inachevés, prérequis présumés maîtrisés, autorisations génériques et ouverture libre aux bibliothèques après réussite | SUPPRIMÉ avec décision enseignante | Remplacés par un diagnostic effectif et des autorisations explicites par séance/exercice ; aucune activité étudiante retirée |
| Absence de politique de contrôle dans le profil joint | RENFORCÉ | Refus sans quiz, mini-cours, code ou indice |

Cette matrice porte sur le dispositif de tutorat. Elle ne résout pas les réserves de l'audit initial sur la progression S1 ou sur les formulations existantes du TD0 et du contrôle.

## Acceptation et vérification

Le contrôle structurel doit démontrer que les cellules des trois sujets sont inchangées, que la source structurée est valide, que les métadonnées générées correspondent à chaque séance et qu'aucune instruction LLM n'est ajoutée dans une cellule. Les changements de métadonnées ne doivent pas altérer les marqueurs ou les contrats d'évaluation. Le contexte fusionné doit être complet et ne contenir aucun gabarit non renseigné.

Pour le pilote ultérieur TD2 S1 uniquement, le commentaire autorisé est l'exception à l'absence d'instruction dans les cellules. Le retrait de cet ajout doit restituer exactement le sujet de référence ; toutes les métadonnées, cellules de code et autres cellules Markdown restent identiques. Le protocole Colab de ce pilote demeure `NOT_TESTED` tant que ses observations ne sont pas consignées.

Le contrôle pédagogique vérifie sur les trois pilotes : copie d'énoncé, demande de solution directe, hésitation sur une variable, notion élémentaire non comprise, demande de bibliothèque hors programme, demande d'aide sur un exercice antérieur et prétention que le contrôle serait terminé. Les réponses attendues sont les comportements de cette politique, jamais les solutions des exercices.

**Vérification manuelle dans Colab : `NOT_TESTED`.** L'ajout ou la conformité des métadonnées ne prouvent ni leur prise en compte effective par Colab, ni une garantie d'absence d'assistance en contrôle. Le test doit vérifier le profil réellement actif, la conservation des métadonnées après import/export et le comportement du tuteur. Une restriction technique de l'accès à l'aide et le retour du correcteur pendant les contrôles sont des sujets distincts à traiter avec l'enseignant.

## Relais des rôles

Le Prof spécifie cette politique et les fiches. L'Architecte réalise leur génération dans les métadonnées et les vérifications structurelles. Le Reviewer pédagogique et l'Auditeur code examinent indépendamment leurs périmètres. L'Intégration assemble leurs preuves avant décision du mainteneur. Ce sous-lot pédagogique conserve le contenu des supports et les correcteurs ; le lot technique distinct relatif aux routes et au retour du correcteur est documenté dans [CONTROL_FEEDBACK.md](../CONTROL_FEEDBACK.md). Aucun contrat de rôle ni fichier de gouvernance n'est modifié.
