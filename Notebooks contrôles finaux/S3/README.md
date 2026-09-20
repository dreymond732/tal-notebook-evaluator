# S3 — Contrôles cumulatifs de la progression textométrique

Sept contrôles prolongent les [TD0–TD7](../../Notebooks%20TD/S3/README.md). **Le premier contrôle intervient après le TD1 et mobilise également le TD0.** Chaque contrôle suivant se concentre sur le dernier TD étudié et réinvestit les acquis antérieurs utiles au problème.

L'objectif est le transfert : les étudiants construisent et expliquent des traitements sur des données originales, dans de nouveaux contextes. Les sujets ne reprennent pas simplement les résultats de Faguet avec d'autres mots. Les corpus embarqués sont des données pédagogiques fictives ; les notebooks ne dépendent ni d'une production antérieure ni d'un export de TD.

| Support | Moment | Compétences focales | Contextes |
|---|---|---|---|
| [Contrôle TD1 S3 — Annotations linguistiques et décisions de lecture](Controle_TD1_S3.ipynb) | Après TD1 | Annotations, positions, segmentation, filtres, dépendances, contrôle manuel | Musée ; transport ; météo |
| [Contrôle TD2 S3 — Fréquences et choix de représentation](Controle_TD2_S3.ipynb) | Après TD2 | Fonctions de fréquences, exclusions, POS, Counter, annotation, nuage et barres | Atelier de réparation ; port ; alimentation |
| [Contrôle TD3 S3 — Concordances et fidélité documentaire](Controle_TD3_S3.ipynb) | Après TD3 | Concordances, formes/lemmes/expressions, citations, normalisation, preuves | Bulletin patrimonial ; radio |
| [Contrôle TD4 S3 — Cooccurrences entre fiches et documents](Controle_TD4_S3.ipynb) | Après TD4 | Présence, marges, paire, agrégations, fenêtres et frontières | Signalements de mobilité ; archives sonores |
| [Contrôle TD5 S3 — Dénominateurs et portée des associations](Controle_TD5_S3.ipynb) | Après TD5 | Dénominateurs, proportions conditionnelles, table 2×2 et sensibilité | Médiation muséale ; alertes du littoral |
| [Contrôle TD6 S3 — Figures vérifiables et retour aux passages](Controle_TD6_S3.ipynb) | Après TD6 | Dispersion, carte de chaleur, segmentation, sensibilité et retour aux passages | Bulletins d’exposition ; retours d’ateliers |
| [Contrôle TD7 S3 — Audit quantitatif d’un rapport synthétique](Controle_TD7_S3.ipynb) | Après TD7 | Moteur paramétrable, comparaison conditionnelle, citations et rapport vérifiable | Médiathèque ; jardin partagé |

Chaque sujet comporte **sept exercices, plusieurs productions par exercice et une durée prévisionnelle de deux heures**. Le calendrier des contrôles est à organiser séparément des huit séances de TD : la série représente quatorze heures supplémentaires si tous les sujets sont administrés intégralement. La durée n'a pas encore été mesurée en classe.

## Conditions de travail

Le travail est individuel. Les étudiants peuvent reprendre leurs propres fonctions et notes de TD ; ils doivent les adapter, expliquer leur fonctionnement et calculer les résultats sur les nouvelles données. Aucun ancien fichier n'est techniquement nécessaire au sujet. Les corrigés et toute assistance d'un LLM sont interdits.

Les instructions de refus d'assistance sont synchronisées dans les métadonnées Colab **et dans la première cellule Markdown**, au moyen du manifeste [tutor_sessions.json](../../docs/pedagogy/tutor_sessions.json). Elles concernent ces contrôles ; les TD conservent leur tuteur de guidage. Ce contexte embarqué n'est pas un dispositif de surveillance ni une garantie de blocage d'un outil externe.

Les données, imports et installations sont fournis ; aucune fonction de résolution, valeur de résultat ou exemple résolu n'est embarqué. Les réponses restent vierges. Les versions de spaCy et du modèle français sont fixées ; l'installation initiale demande Internet et doit être disponible au début de l'épreuve. Un modèle prédit des annotations : les contrôles humains demandés ne sont pas remplacés par le score automatique.

## Évaluation et relecture

Les sept traces portent les marqueurs `S3_Cn_Qm`. Q1 vaut 2 points techniques, Q2–Q7 valent chacune 3 points, soit **un indicateur technique provisoire sur 20**. Celui-ci ne constitue pas la note globale. Les activités de programmation, les analyses linguistiques, les figures et les interprétations font l'objet d'une grille humaine distincte, présente à la fin de chaque notebook.

Les traces doivent être calculées, exécutées et sauvegardées dans la copie. Le serveur examine les données enregistrées ; il n'exécute jamais le code étudiant et ne peut garantir l'authenticité d'une sortie. Une cohérence de format ne démontre pas la validité scientifique d'une analyse. Les contrôles ne divulguent pas les détails de correction dans le reçu étudiant.

La [matrice de couverture](../../docs/pedagogy/S3_CONTROLES_COVERAGE_MATRIX.md) relie chaque contrôle au TD focal et aux acquis mobilisés. La [spécification pédagogique](../../docs/pedagogy/S3_CONTROLES_SPECIFICATION.md) précise les hypothèses, limites et critères de revue. Les tests techniques et les revues indépendantes ne remplacent pas la vérification du rythme auprès d'étudiants.
