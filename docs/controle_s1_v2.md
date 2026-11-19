# Contrôle final S1 v2 — Application des corrections approuvées

## Périmètre

À partir de la révision `2445c9e18357dc6a99a8e516bf0d7bd7e462fd42`, les quatre substitutions Q5/Q24/Q25/Q30 approuvées le 19 novembre 2026 limitent le contrôle aux TD1–TD5 et au DM. Les incohérences sujet–correcteur sont corrigées dans le même lot. Le DM et ses corrections humaines ne sont pas modifiés.

La matrice enseignante et le détail des objectifs sont dans `docs/pedagogy/controle_s1_td1_5_coverage.md`.

## Contrat et correction

- Sujet actuel `Notebooks contrôles finaux/S1/Controle_final_S1_python.ipynb`, même évaluateur `Controletilt-s1`, version **2** dans le sujet et le catalogue.
- Les cellules d'identité (nom, prénom, classe) et les 30 cellules de réponse doivent être présentes avec leur rôle explicite. Aucun numéro étudiant supplémentaire n'est requis.
- Les copies version 1 ou sans métadonnées sont refusées comme « mauvaise version du notebook », sur `/submit` et `/eval/Controletilt-s1`, avant correction et persistance. Les archives déjà enregistrées ne sont ni migrées ni recalculées.
- Les poids sont conservés : 25 questions à 1 point, 5 à 2 points et 1 point d'identification, soit **36 points**. Les points d'identification ne sont pas accordés aux noms laissés à `...`.
- Les résultats sont lus dans la sortie `stdout` enregistrée de la seule cellule de réponse concernée. Une trace manquante ou dupliquée ne donne aucun point. Des affichages supplémentaires portant un autre libellé restent possibles.
- Q2 lit maintenant la trace canonique existante, puis vérifie le mot extrait et la tranche sur la chaîne de référence connue. Les indices positifs, négatifs et calculés par le programme sont autorisés. Cela remplace l'ancienne lecture des seules affectations littérales. Les bornes effectivement retrouvées sont conservées dans le rapport.
- Les booléens sont distingués des entiers : `0` ne remplace pas `False` et `1` ne remplace pas `True`. Les dictionnaires sont comparés sans imposer l'ordre des clés ; l'ordre des listes et la casse demandée sont conservés.
- Aucun code de la copie n'est exécuté. Le contrôleur lit les traces : il ne prouve ni leur authenticité, ni l'exécution des lignes, ni la généralité des fonctions. Une constante affichant le résultat attendu peut encore être créditée ; une sortie enregistrée reste une preuve technique limitée. Cette mission n'introduit pas de moteur de démonstration statique.
- Le retour public reste un reçu, sans score ni solution. Le rapport et le journal de notes sont réservés à l'enseignant.

## Corrigé et distribution

Le corrigé actuel est produit indépendamment depuis le sujet v2 dans :

`Corrigés modèles/Contrôles finaux/controle-s1-v2/Controle_S1_v2_corrige_non_execute.ipynb`.

Sa lecture préalable par question figure dans `lecture_etudiante.md`. Ce corrigé est exclu de la distribution. Il reste sans sorties enregistrées et n'a pas été exécuté dans Colab. Le fichier historique `historique/Notebooks contrôles finaux/DevoirS1_TILT_corrigé.ipynb` est conservé pour l'ancien sujet v1 ; il ne constitue pas le corrigé du contrôle révisé.

Après fusion, reconstruire la distribution via la procédure habituelle du dépôt et redistribuer le **nouveau sujet v2**, plutôt que modifier les métadonnées des anciennes copies. La présente modification n'est ni une fusion ni un déploiement du serveur.

## Vérifications prévues

- Réponses attendues des 30 questions, total borné à 36, réponses erronées/absentes et variantes recevables.
- Q2 : quatre combinaisons de bornes positives/négatives, bornes calculées, refus des bornes fractionnaires et tranches incorrectes.
- Contrat v2 et rejet des anciens sujets sur les deux chemins de dépôt ; pas de persistance en cas de refus.
- Rapport privé et reçu public ; données synthétiques et dossiers temporaires uniquement.
- Suite de non-régression, vérification des instructions du tuteur et génération/vérification d'une distribution neutre.
- Revues indépendantes pédagogique, éditoriale, technique et gouvernance. Les résultats effectifs sont consignés dans le rapport de gouvernance et la PR ; cette liste ne vaut pas preuve de réussite.
