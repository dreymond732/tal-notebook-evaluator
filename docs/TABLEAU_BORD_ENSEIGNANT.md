# Tableau de bord enseignant — progression TAL

## Accès protégé

La page /enseignant/progression est accessible depuis l'accueil du correcteur.
Elle est indépendante du portail individuel des étudiants. Un code aléatoire
de 12 caractères est envoyé à l'adresse TAL_TEACHER_EMAIL configurée sur le
serveur. Il est valable 10 minutes et utilisable une seule fois.
La session enseignante est limitée à deux heures.

Un seul destinataire autorisé est défini en configuration : il n'existe pas
de champ permettant de choisir une autre adresse depuis le site. Les codes
sont stockés sous forme de dérivés cryptographiques salés dans la base privée
soumissions/suivi/acces_enseignant.sqlite3. Les tentatives et demandes sont
limitées, les formulaires sont protégés contre le CSRF, et HTTPS est obligatoire.

## Configuration sur le serveur

Ajouter dans le fichier .env (privé et jamais commité) :

    TAL_TEACHER_EMAIL=adresse-enseignant@example.fr

Les variables SMTP TAL_SMTP_* existantes et TAL_ACADEMIC_YEAR=2026-2027
sont réutilisées. FLASK_SECRET_KEY doit être définie, privée et comporter
au moins 24 caractères (32 ou plus recommandés). Ne pas la changer sans
nécessité : cela invaliderait également les sessions étudiantes.

Le fichier docker-compose.yml transmet TAL_TEACHER_EMAIL au conteneur.
Après fusion de la PR, depuis la racine du projet :

    git pull
    docker-compose up -d --build --force-recreate corrector-tal

Contrôle de configuration sans divulguer les secrets :

    docker-compose exec -T corrector-tal python - <<'PY'
    import os
    import teacher_access
    print("Email autorisé :", "CONFIGURÉ" if os.getenv("TAL_TEACHER_EMAIL") else "ABSENT")
    print("Préconditions actives :", teacher_access.configured())
    print("Année :", os.getenv("TAL_ACADEMIC_YEAR") or "ABSENTE")
    PY

Un résultat True confirme la présence de la configuration ; seul un test
réel d'envoi depuis la page confirme la réception du message. Ne jamais
communiquer publiquement les codes, les clés SMTP ou les secrets Flask.

## Fonctionnalités

La synthèse par semestre S1, S2 ou S3 présente tous les étudiants ayant
au moins un essai valide, avec le nombre de TD, de devoirs maison et de
contrôles réalisés, et le nombre total de tentatives. Une recherche par
nom, prénom ou numéro fonctionne directement dans le navigateur sans
envoyer la recherche au serveur ni l'inscrire dans une URL.

La fiche individuelle d'un étudiant précise, activité par activité,
le minimum, le maximum et le nombre d'essais. Les groupes TD, DM et
Contrôles sont distincts. Le fichier CSV original du semestre peut
être téléchargé par l'enseignant authentifié.

Les résultats des correcteurs sont parfois provisoires. Il n'y a aucune
moyenne transversale entre des barèmes différents. Les étudiants sans
dépôt enregistré sont absents de la synthèse.

La source des données est le dossier privé soumissions/suivi/ :
progression_S1.csv, progression_S2.csv, progression_S3.csv. Ces fichiers
sont régénérés automatiquement après chaque soumission acceptée.
Si nécessaire :

    docker-compose exec -T corrector-tal python progression.py --annee 2026-2027

## Confidentialité

Le portail étudiant /ma-progression reste inchangé et ne permet toujours
pas de consulter les contrôles ou les dossiers d'autres étudiants.

Les routes collectives, la fiche et l'export sont interdits avant
authentification. La fiche est demandée par POST avec vérification CSRF,
sans numéro étudiant dans l'URL. Les réponses ne doivent pas être
mises en cache. La page bloque son inclusion dans un iframe et ne charge
pas de ressources externes. Les CSV, les copies et la base d'accès ne
sont ni déplacés dans dist/ ni exposés directement par le serveur web.

Le changement de l'adresse TAL_TEACHER_EMAIL invalide les sessions
enseignantes antérieures. Cette méthode repose sur la maîtrise de la
boîte email ; elle n'est pas une connexion SSO institutionnelle.

## Vérifications de développement

    python -m unittest discover -s tests -p test_teacher_dashboard.py -v
    python -m unittest discover -s tests -v

Tous les tests emploient des données fictives et un SMTP simulé.
Aucune donnée de production n'est modifiée par la PR. Une revue de
sécurité indépendante est requise avant fusion ou déploiement.
