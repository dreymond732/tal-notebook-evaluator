# Revue pédagogique indépendante — devoir_S1_tuteur

Mission : examiner le cadrage préalable puis la copie de révision guidée du DM intermédiaire S1. Rôle : TAL-Pedagogy-Reviewer, distinct du Prof et du Designer. Branche : `pedagogy/devoir-s1-tuteur`, baseline `590b9a6`, 15 octobre 2026. Aucun support, document pédagogique, code applicatif ou test modifié par le réviseur ; aucun commit ni changement de branche.

## Prévalidation avant conception

Matrice `docs/pedagogy/devoir_s1_tuteur_spec.md` lue intégralement avant création de la copie. Les règles AGENTS, le rôle Reviewer, la politique de tutorat et les matrices de progression S1 ont été comparés. La demande autorise une édition séparée de révision et l'introduction active des notions nécessaires, sans changement du contrôle original. Aucune nouvelle confirmation enseignante n'est requise.

Le DM source a été relu dans l'audit indépendant et sauvegardé pour comparaison : 45 cellules, 18 questions, SHA-256 `6fd62ebefdb8e8cd1a7673edf1dbfca2b26a02745dd2ab98a6183f9ea46122f1`. La source est toujours inchangée et la cible n'existe pas au moment de la prévalidation. Les références des TD1–5 indiquées par cellule et identifiant dans le cadrage ont toutes été vérifiées physiquement : aucune référence erronée.

La matrice prévoit copie intégrale des 18 questions, données, réponses, explications, essais et barème ; seules les conditions d'assistance, titre et métadonnées/contextes du tuteur peuvent différer. Le profil `devoir_S1_tuteur` est une nouvelle séance `td` au manifeste. Le catalogue de notation et la distribution automatique restent inchangés ; la copie est une source ouvrable directement dans Colab. Le mode d'aide LLM et le mode privé de correction sont explicitement distincts.

Les listes fermées de 18 Q ont été comparées aux prérequis réels. Le cadrage a été complété avant validation : opérations nécessaires Q12 ; branches et fonction auxiliaire facultative Q14 ; espaces internes/accents/ponctuation Q15 ; révision transitive du comptage Q18. Ces compléments n'autorisent aucune agrégation des permissions. Division et priorités Q1–2, ordre d'insertion Q9/Q13 et accès indexé sûr/contraintes multiples Q14 sont explicitement introduits dans cette édition, sans prétendre les avoir rétrospectivement enseignés au contrôle original.

Le protocole impose choix de Q, diagnostic, révision de toutes les notions de cette seule Q individuellement, une question par tour et attente, explications et exemples conceptuels distincts en cas de besoin, suivi des acquis puis résolution personnelle. Il interdit code S1, résultat, condition ou algorithme complets, pseudocode, formulation à recopier, import et action sur les cellules. Les groupements de notions ne deviennent pas une recette.

**ACCEPT DU CADRAGE PRÉALABLE**, transmis au Prof et à l'orchestrateur avant conception. Empreinte de la version acceptée avant attribution : `b322b5916ade77cb835c8a7df9d9a99ff43369d4bc011196a2d8d4a33e2cbdf8`. Cette décision ne vaut pas validation de la copie future ni du comportement réel de Gemini.

## Revue de la cible

La copie cible et son contexte ont été relus intégralement après le relais du Designer. La vérification de conservation est indépendante des assertions du producteur. Les indices du tableau suivant commencent à **1**, comme dans la matrice préalable.

### Conservation matérielle et autonomie

La copie comporte les mêmes 45 cellules. Les 43 cellules autres que titre/contexte initial et introduction sont strictement identiques au DM source. Les métadonnées, types, identifiants, ordre, sorties et compteurs de toutes les cellules restent identiques ; toutes les sources de code sont identiques. Les 18 énoncés et réponses, leurs données, noms, marqueurs, cinq explications personnelles, trois essais complémentaires Q14 et tous les cas limites restent livrés au même emplacement. Aucun corrigé, résultat, exemple résolvant une question ou amorce d'algorithme n'a été ajouté. L'autonomie finale de résolution est maintenue ; l'accompagnement nouveau porte sur les notions préalables.

Les seules différences visibles sont le titre `devoir_S1_tuteur — Révision guidée : une bibliothèque prépare ses ateliers` et le paragraphe Conditions de travail. Ce paragraphe désigne clairement la copie comme édition de révision distincte du devoir original, indique comment choisir sa question, décrit l'aide notion par notion et maintient l'écriture/exécution par l'étudiant sans code, résultat ou solution fournis. Les autres paragraphes — contexte fictif, parcours après TD5, durée indicative, périmètre, organisation, barème et prudence sur la note — restent identiques. La durée héritée ne mesure pas le temps réel d'une conversation de révision exhaustive.

`metadata.tal` et `tal_control` restent identiques au DM. Le profil de tutorat propre est `devoir_S1_tuteur`, activité `td`, semestre 1 ; aucune bibliothèque permise ou fournie. Le contexte HTML est complet dans la première cellule avec titre visible avant commentaire ; il est exactement identique à la chaîne Colab. Les 35 autres séances et toutes les exclusions du manifeste sont identiques à la baseline. Le DM original reste inchangé octet pour octet et sa séance de contrôle ne reçoit pas de guidage.

### Carte des 18 questions et prérequis

Les notions effectivement enregistrées dans le manifeste, les métadonnées de la copie et les 18 lignes rendues du contexte ont été comparées au JSON du cadrage prévalidé : égalité question par question, sans union de permissions. Les références TD1–5 du cadrage étaient déjà vérifiées physiquement. Le tableau indique la portée autorisée, jamais une réponse ou un plan d'exécution.

| Question | Énoncé / réponse | Notions propres à réviser séparément | Introduction nouvelle déclarée |
|---|---|---|---|
| Q1 — Calculer un budget | 5 / 6 | int(), type(), +, *, /, affectation, montant et moyenne, liste, print() | / |
| Q2 — Lire deux expressions | 7 / 8 | -, /, priorités, parenthèses, ordre de calcul, interprétation, print() | /, priorités, parenthèses, ordre de calcul |
| Q3 — Tester une inscription | 9 / 10 | tuple, in, >, and, booléen, f-string, liste, print() | Réactivation sans outil nouveau |
| Q4 — Transformer sans effacer | 12 / 13 | chaîne immuable, affectation, strip(), lower(), replace(), source conservée, liste, print() | Réactivation sans outil nouveau |
| Q5 — Extraire une référence | 14 / 15 | chaîne, indices positifs et négatifs, tranches, borne exclue, liste, print() | Réactivation sans outil nouveau |
| Q6 — Interpréter un découpage | 16 / 17 | split(), liste, len(), indices, ponctuation et apostrophe, fragment et mot, print() | Réactivation sans outil nouveau |
| Q7 — Reconstruire une annonce | 18 / 19 | liste de chaînes, join(), split(séparateur), séparateur exact, ==, print() | Réactivation sans outil nouveau |
| Q8 — Liste et référence | 21 / 22 | liste modifiable, pop(), append(), tuple ordonné, type(), ==, print() | Réactivation sans outil nouveau |
| Q9 — Construire un lexique | 23 / 24 | dictionnaire, clé/valeur, ajout, ordre insertion, items(), déballage, for, indentation, liste, append(), f-string, print() | ordre insertion |
| Q10 — Comparer deux ateliers | 25 / 26 | liste, set(), len(), répétitions et formes, intersection, différence, ordre ensemble libre, print() | Réactivation sans outil nouveau |
| Q11 — Filtrer puis mesurer | 28 / 29 | for, indentation, liste, append(), strip(), lower(), len(), >=, if, compréhension, ordre et source, print() | Réactivation sans outil nouveau |
| Q12 — Deux séries bornées | 30 / 31 | range(), for, liste, append(), while, condition, compteur, mise à jour, accumulation, bornes, print(), +, * | Réactivation sans outil nouveau |
| Q13 — Compter des demandes | 32 / 33 | dictionnaire, for, in, if/else, get(), items(), ordre insertion, liste, append(), >=, accumulation, len(), ==, print() | ordre insertion |
| Q14 — Recherche bornée | 34 / 35 | while, conditions multiples, booléen, comparaisons, liste, len(), indice sûr, borne, compteur, append(), arrêt, essais limites, def/paramètre/appel/return/localité optionnels, print(), -, and, if/else | conditions multiples, indice sûr |
| Q15 — Normaliser une notice | 37 / 38 | def, paramètre, appel, return, localité, strip(), lower(), chaîne vide, print(), espaces internes, accents, ponctuation | Réactivation sans outil nouveau |
| Q16 — Compter une collection | 39 / 40 | def, paramètre, appel, return, localité, for, dictionnaire, in, if/else, get(), comptage, casse, liste vide, source, print() | Réactivation sans outil nouveau |
| Q17 — Traduire avec un lexique | 41 / 42 | def, paramètres, appel, return, localité, composition, strip(), lower(), dictionnaire, in, if/else, for, liste, append(), split(), join(), cas inconnu et vide, limites traduction, print() | Réactivation sans outil nouveau |
| Q18 — Composer une synthèse | 43 / 44 | def, paramètre, appel, return, localité, composition, strip(), lower(), split(), len(), dictionnaire, clés, comptage, formes distinctes, ponctuation et accents, chaîne vide, print(), liste, for, in, if/else, get(), accumulation | Réactivation sans outil nouveau |

Les groupes, notamment variable/valeur/type, indices positifs/négatifs, espaces/accents/ponctuation et la fonction facultative Q14, doivent être traités par sous-notion ; le prompt le demande explicitement. Les notions des fonctions appelées Q17/Q18 restent dans leurs propres fiches, sans résoudre Q15/Q16 ni hériter des permissions de tout le devoir. `get` et if/else sont des variantes de comptage à comprendre, pas deux algorithmes à livrer. Aucun tri, tokenizer, bibliothèque, somme native ou procédé extérieur à la fiche n'est ajouté.

Q1/Q2 peuvent maintenant faire l'objet d'une introduction conceptuelle explicite de division/priorités, autorisée pour cette édition. Q9 et Q13 ne supposent pas que l'autre Q ait déjà enseigné l'ordre d'insertion. Q14 permet diagnostic de sûreté de l'indice et des motifs d'arrêt, sans condition complète ni algorithme. Ces ajouts ne changent pas rétrospectivement la préparation offerte par le DM original.

### Protocole de révision, garanties et limites

Le contexte exige de reconnaître la Q par numéro, titre ou énoncé et de demander une précision si elle est ambiguë. Il interdit de changer de question ou d'inventer une fiche. Une seule Q donne accès à sa seule liste fermée. Il demande diagnostic de chaque notion et de chaque élément d'un groupe, suivi des acquis vérifiés et des points à reprendre, une seule question par tour puis attente effective. Un « compris » ne prouve pas l'acquis.

En cas de blocage, le tuteur doit expliquer une seule notion en quelques phrases et proposer un exemple conceptuel sur des données distinctes en langage naturel, puis une question de vérification. Il doit reprendre l'erreur avant de poursuivre. La révision de toutes les notions précède reformulation de l'objectif puis essai autonome. Le contexte interdit de distribuer la solution par une succession de questions.

L'interdiction S1 de code, expression Python à recopier, correctif, pseudocode, solution rédigée et résultat s'applique dès la première demande et persiste après insistance ou revendication de rôle. Aucune addition, modification ou exécution de cellule, import, réseau, fichier ou outil de résolution n'est permis. Les noms d'opérateurs/méthodes dans la carte désignent des notions à expliquer, pas du code d'exemple autorisé.

### Constat de revue corrigé avant clôture

**TAL-PED-DST-001 — Modéré, résolu.** La première cible disait « Ne prétendez pas valider une réponse ou une note sans preuve ». Cette réserve pouvait laisser entendre qu'une réponse du devoir pouvait être validée en présence d'une prétendue preuve, alors que le cadrage sépare vérification conceptuelle et résolution. Impact : ambiguïté de l'aide permise et risque de résultat indirectement livré. Ordre transmis : remplacer cette phrase par « Vérifiez la compréhension conceptuelle, sans valider une réponse du devoir ni une note. », puis régénérer uniquement la copie. Critère d'acceptation : phrase non conditionnelle présente dans les deux copies du contexte, cartes/grading/source inchangés. L'orchestrateur a accepté ce correctif ; sa vérification finale est consignée dans l'addendum d'empreintes ci-dessous.

La revue porte sur les consignes livrées et leur couverture. Elle ne prouve pas que Gemini les appliquera dans Colab : une liste complète et un prompt correct ne sont pas une conversation effectivement observée. L'absence d'essai réel Colab restera déclarée, sans transformer des tests de génération en preuve d'acquisition.

### Verdict de spécialité

Le correctif de clôture a été vérifié indépendamment dans les deux copies du contexte. **TAL-PED-DST-001 est résolu. Le verdict final est `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE — ACCEPT`** pour cette copie de révision et son protocole explicite. Il ne valide ni le comportement réel Colab ni la note technique du correcteur original. Les revues éditoriale, technique, étudiante et de gouvernance restent distinctes.

### Handoff

Fichiers modifiés par le réviseur : aucun ; rapport temporaire seulement. Source, cible, branche et empreintes indiquées dans ce document. Tests de cette revue : comparaisons JSON, profils, carte par Q et contextes, sans exécution de programme étudiant. Références historiques privées non disponibles, sans prétention de restauration. Risques examinés : confusion révision/contrôle, permission agrégée, validation indirecte d'une solution, révision fictivement achevée après un diagnostic. Critères : conservation des 18 Q, couverture des prérequis, protocole exhaustif fermé, titre/conditions cohérents, absence de solution, fermeture du constat DST-001. Aucun changement pédagogique du contrat de notation observé ; l'évolution technique du générateur exige sa revue de code distincte. Verdict demandé au relais : intégrer les avis spécialisés puis la gouvernance, sans fusion automatique ni levée de l'audit S1 global.


## Limites

Les références privées historiques ne sont pas relues et aucune restauration historique complète n'est revendiquée. Les constats du contrôle original et des autres supports S1 restent ouverts. La révision des prérequis dans cette nouvelle édition ne résout pas leur absence démontrée dans les TD annoncés par le DM original. Aucun programme étudiant ne sera exécuté par cette revue.

## Empreintes finales et clôture

La copie régénérée a été recontrôlée après le correctif DST-001 : phrase non conditionnelle exactement présente dans le commentaire HTML et dans le contexte Colab, ancienne phrase absente. Les 43 cellules hors titre/introduction, les 18 fiches de notions et les métadonnées de notation restent identiques aux références vérifiées. Le DM original reste identique à son empreinte source.

- Notebook final : `Notebooks contrôles finaux/S1/devoir_S1_tuteur.ipynb`, SHA-256 `e67df7e49ea623346cc50964002ef0473359649b3fa3b13af7353ae9a80ac25b`.
- Contexte final : **4 256 caractères sur 4 400**, SHA-256 `1ce982aa091861a5550f50721f30e68d0eb0ae5b6f4c85cb7ff29b9752d3306b` ; les deux représentations sont strictement identiques.
- Source originale : SHA-256 `6fd62ebefdb8e8cd1a7673edf1dbfca2b26a02745dd2ab98a6183f9ea46122f1`, toujours inchangée.

ACCEPT de spécialité pédagogique confirmé sur ces empreintes. La lecture Étudiant-Modèle sera intégrée séparément après remise ; elle ne remplace pas les preuves de conservation. Aucun essai réel de Gemini dans Colab n'est revendiqué.

## Clôture après lecture étudiante indépendante

Le rapport `Corrigés modèles/TD/devoir-s1-tuteur/lecture_etudiante.md` a été lu intégralement. Il couvre les 45 cellules et les 18 questions sur la même empreinte finale `e67df7e49ea623346cc50964002ef0473359649b3fa3b13af7353ae9a80ac25b`, avec les seuls sujets TD1–5 comme ressources antérieures. Le lecteur n'a consulté ni corrigé, ni correcteur, ni matrice ; il ne revendique aucune résolution, conversation tutorielle réelle ou exécution.

La lecture confirme le choix de Q, l'aide notion par notion, les données et productions des 18 exercices ainsi que le retour autonome. Elle relève trois réserves : statut de la note hérité du sujet original ; division/priorités Q1–2 non explicitement enseignées dans les TD ; garantie d'ordre Q9/Q13 non explicitée dans ces mêmes ressources. Les deux dernières correspondent exactement aux notions introduites par le cadrage de cette édition de révision, sans prétention d'enseignement antérieur ou de maîtrise effectivement vérifiée. Le caractère facultatif de la fonction Q14 et les dépendances Q17/Q18 restent intelligibles.

Le paragraphe Conditions de travail annonce un support de révision distinct du devoir évalué original ; le paragraphe Évaluation conservé mentionne encore la confirmation de note par l'enseignant. Le lecteur ne peut donc déterminer à lui seul la portée administrative de la note de cette copie. Cette réserve d'organisation est publiée comme **limite non bloquante de cette adaptation**, sans inventer une interdiction de soumission ou une nouvelle règle de notation. Une précision enseignante pourrait aider lors de l'utilisation, mais elle ne conditionne pas la conformité des 18 activités et du protocole livré. Le barème et les métadonnées ont été conservés expressément ; les reviewers n'ont pas autorité pour en déduire un nouveau régime d'évaluation.

**ACCEPT et COUVERTURE_PÉDAGOGIQUE_CONSERVÉE maintenus sur l'empreinte finale indiquée**, sans modification additionnelle de l'introduction. Le constat DST-001 demeure résolu. La non-observation de Gemini dans Colab et les écarts du DM original restent explicitement hors de ce verdict.
