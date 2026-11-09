# Tableau de bord enseignant — progression TAL

## Accès protégé

La page /enseignant/progression est accessible par un lien discret.
**Aucun envoi de code n'est possible depuis une page web.** L'enseignant
déclenche personnellement un envoi depuis le terminal du NAS :

    docker-compose exec -T corrector-tal python send_teacher_code.py

Le code est expédié exclusivement à TAL_TEACHER_EMAIL, sans afficher le
secret dans le terminal. Il reste valable 10 minutes, à usage unique.
Le formulaire web demande l'adresse TAL_TEACHER_EMAIL et le code reçu.
L'adresse ne constitue pas un deuxième secret : la possession du code
envoyé exclusivement sur demande de l'administrateur est le contrôle
d'authentification. La limite des essais de code reste active.

La session enseignante est limitée à deux heures.

Un seul destinataire autorisé est défini en configuration : il n'existe pas
de champ permettant de choisir une autre adresse depuis le site. Les codes
sont stockés sous forme de dérivés cryptographiques salés dans la base privée
soumissions/suivi/acces_enseignant.sqlite3. Les tentatives de connexion et les demandes CLI sont
limitées. La connexion par code CLI n'exige plus le jeton CSRF d'une
session anonyme ; les formulaires sensibles d'une session authentifiée
(fiche et déconnexion) restent soumis au CSRF. HTTPS est obligatoire.

## Configuration sur le serveur

Ajouter dans le fichier .env (privé et jamais commité) :

    TAL_TEACHER_EMAIL=adresse-enseignant@example.fr

Réglages de session recommandés pour le proxy SWAG de TAL :

    TAL_SESSION_COOKIE_NAME=tal_corrector_session
    TAL_SESSION_COOKIE_PATH=/universite/tal/

Ce sont des paramètres **TAL**, distincts de ceux de Journalia
(`JOURNALIA_SESSION_COOKIE_NAME`, `JOURNALIA_SESSION_COOKIE_PATH`).
Le chemin du cookie doit être le préfixe **public** de TAL, avec barre
finale, et non le chemin interne du conteneur après le `rewrite`
Nginx. Si la racine publique change, adapter ce chemin avant de déployer.
Le nom et le chemin ne doivent pas être partagés avec une autre application.

Les variables SMTP TAL_SMTP_* existantes et TAL_ACADEMIC_YEAR=2026-2027
sont réutilisées. FLASK_SECRET_KEY doit être définie, privée et comporter
au moins 24 caractères (32 ou plus recommandés). Ne pas la changer sans
nécessité : cela invaliderait également les sessions étudiantes.

Le fichier docker-compose.yml transmet TAL_TEACHER_EMAIL au conteneur.
La commande CLI ci-dessus utilise les variables et SMTP déjà configurés.
Elle doit être exécutée depuis le répertoire du projet sur le NAS,
et ne peut pas être déclenchée par un étudiant ou un visiteur du site.
Après fusion de la PR, depuis la racine du projet :

    git pull
    docker-compose up -d --build --force-recreate corrector-tal

Important : `docker-compose up -d --force-recreate` **sans** `--build`
ne recharge pas les modules Python ni les templates intégrés à l'image.
Dans TAL, seul `soumissions/` est monté depuis l'hôte.


Contrôle de configuration sans divulguer les secrets :

    docker-compose exec -T corrector-tal python - <<'PY'
    import os
    import teacher_access
    print("Email autorisé :", "CONFIGURÉ" if os.getenv("TAL_TEACHER_EMAIL") else "ABSENT")
    print("Préconditions actives :", teacher_access.configured())
    print("Année :", os.getenv("TAL_ACADEMIC_YEAR") or "ABSENTE")
    PY

Un résultat True confirme la présence de la configuration. Un envoi
CLI réel et la réception de son message confirment le fonctionnement SMTP. Ne jamais
communiquer publiquement les codes, les clés SMTP ou les secrets Flask.

## Fonctionnalités

La synthèse par semestre S1, S2 ou S3 présente tous les étudiants ayant
au moins un essai valide, avec le nombre de TD, de devoirs maison et de
contrôles réalisés, et le nombre total de tentatives. Un nouveau
tableau « Détail des évaluations » affiche, pour chaque TD, DM ou
contrôle, le nombre d'étudiants et le total d'essais reconnus. Une recherche par
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

## Vérification du proxy et de l'accès enseignant

Le lien est visible sur l'accueil et les pages S1/S2/S3. La route réelle
est `/enseignant/progression/`, sous le préfixe public TAL
`/universite/tal/` :

    https://<domaine>/universite/tal/enseignant/progression/

Le proxy SWAG doit retirer `/universite/tal` du chemin transmis au
conteneur **tout en transmettant** au Flask `ProxyFix` :

    X-Forwarded-Prefix: /universite/tal
    X-Script-Name: /universite/tal
    X-Forwarded-Proto: https

Cela reprend la même logique que l'installation Journalia, mais avec
le préfixe propre à TAL. Ne pas recopier les variables JOURNALIA_* dans TAL.
La configuration de SWAG n'est pas contenue dans ce dépôt ; vérifier le
fichier actif avant toute modification. Si le portail étudiant fonctionne
déjà derrière HTTPS, les en-têtes de proxy sont probablement corrects.

**Diagnostic sans divulguer de secret :**

    docker-compose exec -T corrector-tal python - <<'PY'
    from pathlib import Path
    from app import create_app
    import os
    app = create_app()
    print("Template enseignant :", "Espace enseignant" in Path("templates/selector_template.html").read_text())
    print("Route enseignant :", any("/enseignant/progression" in str(rule) for rule in app.url_map.iter_rules()))
    print("Cookie name :", app.config["SESSION_COOKIE_NAME"])
    print("Cookie path :", app.config["SESSION_COOKIE_PATH"])
    print("Email enseignant :", "CONFIGURÉ" if os.getenv("TAL_TEACHER_EMAIL") else "ABSENT")
    PY

Dans ce diagnostic, un template absent ou une route absente signifie en
premier lieu que le conteneur utilise une ancienne image. Un accès direct
sur `http://127.0.0.1:5001` ne prouve pas la disponibilité de la connexion :
le portail refuse volontairement les requêtes non HTTPS.

## Parcours sous le reverse proxy

Après validation du code, le serveur redirige directement vers la
liste des étudiants du semestre S1. La redirection conserve
explicitement le chemin public du cookie pour le cas où la requête
POST ne reçoit pas l'en-tête X-Forwarded-Prefix de SWAG.

Pour éviter les collisions avec Journalia, configurer dans le .env
du correcteur :

    TAL_SESSION_COOKIE_NAME=tal_corrector_session
    TAL_SESSION_COOKIE_PATH=/universite/tal/

Le lien enseignant reste discret. L'envoi du code n'est
désormais possible que depuis la commande CLI sur le NAS, avec
limitation de débit ; le navigateur ne déclenche aucun message.

Les TD3, TD4, TD5 et TD6 initiaux du S1, auparavant exclus,
sont maintenant reconnus comme des travaux distincts de leurs
approfondissements. Le détail des essais est lu dans les journaux
CSV canoniques, pas à partir d'un décompte des fichiers nb/rapport/.
Pour contrôler le cas de S1_TD4, voir docs/SUIVI_PROGRESSION.md.


## Correction des compteurs et de la navigation (novembre 2026)

Les TD principaux et les activités complémentaires sont maintenant séparés
dans le tableau : S1 = **7 TD principaux et 12 approfondissements** ;
S2 = **3 TD** (les deux autres exercices sont des contrôles) ;
S3 = **9 TD principaux et 3 révisions**. Les numéros affichés pour chaque
étudiant correspondent à des *activités ayant reçu au moins un dépôt valide*,
pas au nombre de fichiers présents ni au nombre total de soumissions.

Les essais sous contrat ancien, lorsqu'ils ont un score numérique, une
identité identifiable et une date dans l'année universitaire, sont
comptabilisés **uniquement pour la participation** et affichés dans la
colonne « Essais anciens ». Un étudiant n'ayant que ces anciens dépôts
apparaît désormais dans l'espace enseignant. Les notes des contrats
antérieurs ne sont pas comparées aux min/max des contrats actuels.
Les tableaux de progression CSV et le portail étudiant restent
inchangés : l'export actuel du semestre concerne les *scores actuels*.

### Résolution des liens S3, fiches et export sous SWAG

Les liens de cet espace sont construits sous le préfixe public du cookie
défini dans `.env`, même lorsque Nginx omet
`X-Forwarded-Prefix` sur une requête. Pour TAL, conserver :

    TAL_SESSION_COOKIE_NAME=tal_corrector_session
    TAL_SESSION_COOKIE_PATH=/universite/tal/

L'adresse publique de la synthèse est :

    https://hazigo.duckdns.org/universite/tal/enseignant/progression/

Après fusion de la PR, **reconstruire** l'image Docker :

    git pull
    docker-compose up -d --build --force-recreate corrector-tal

Si un onglet S3, une fiche ou un export renvoie encore 403, vérifier
dans l'inspecteur du navigateur que le chemin URL reste sous
`/universite/tal/` et que le navigateur joint le cookie
`tal_corrector_session` (ne jamais copier ou publier sa valeur).
Un 403 **sans cookie valide** reste une protection normale. Aucune
route de consultation nominative n'est accessible anonymement.

L'audit des journaux sur le NAS donne la concordance des essais des
contrats courants. Les journaux comportant des anciennes versions
doivent être distingués des corrections de résultats :
`audit_progressions.py --annee 2026-2027 --toutes-evaluations` ne
mélange pas leurs scores, mais l'espace enseignant les mentionne
désormais comme travaux réalisés.


## Changement du circuit enseignant : commande CLI exclusivement

Les anciennes explications de demande automatique et de renvoi depuis
le navigateur décrivent le fonctionnement antérieur, retiré pour
protéger le quota de mails Brevo. **Ne plus utiliser le formulaire
« Code non reçu ? » ni l'ancienne route /demander-code** : ils
n'existent plus. L'envoi est une opération du mainteneur sur le NAS.

La page de connexion demande désormais l'adresse enseignante définie
dans .env ainsi que le code à usage unique. Le code n'est pas réutilisable,
et un code erroné ne doit pas permettre d'entrer dans le tableau.

```bash
docker-compose exec -T corrector-tal python send_teacher_code.py
```

L'ancienne page pouvait générer un CSRF à partir d'un cookie anonyme
dont le contenu changeait entre les requêtes sous SWAG. **La connexion
CLI email+OTP ne dépend plus de ce CSRF** ; il reste requis pour les
actions privées d'une session enseignante déjà validée.

## Correction de la session CSRF après migration du chemin du cookie

Les anciennes versions du portail pouvaient provoquer un HTTP 400
à la connexion ou à la redemande du code, en raison d'un jeton CSRF
associé à une session différente. Une autre cause possible était la
coexistence de deux cookies TAL du même nom, l'un avec `Path=/`,
l'autre avec `Path=/universite/tal/`. Le circuit CLI actuel n'utilise
plus de CSRF anonyme pour la connexion.

Le correcteur expire maintenant explicitement **uniquement** le cookie
`tal_corrector_session` de `Path=/` lorsqu'un chemin public différent
est configuré. Il continue d'émettre le cookie actif sous
`Path=/universite/tal/`. Cette purge ciblée n'affecte pas Journalia
ni les autres applications ; le cookie générique `session` n'est pas
effacé.

Les formulaires privés (fiche, déconnexion) restent soumis au CSRF ;
une incohérence entraîne un HTTP 400 accompagné d'une explication. Les journaux techniques n'enregistrent
que des indicateurs booléens et le nombre de cookies homonymes, jamais
leur valeur ni le code de connexion.

Pour tester sans modifier les cookies existants, ouvrir une **fenêtre
privée** de Firefox et accéder à l'URL publique complète :

    https://hazigo.duckdns.org/universite/tal/enseignant/progression/

Un ancien code enseignant est **à usage unique** et ne peut pas être
réutilisé : la connexion exige un code nouvellement demandé et non expiré.

Après fusion, reconstruire l'image Docker (les fichiers Python et HTML
ne sont pas montés en volume) :

    git pull
    docker-compose up -d --build --force-recreate corrector-tal

Si l'erreur persiste, consulter les lignes `Formulaire enseignant TAL :
session CSRF non reconnue` dans les logs. Les indicateurs
`cookie_recu`, `cookies_homonymes`, `session_presente` et
`jeton_formulaire_present` permettent de différencier les causes sans
exposer les informations secrètes :

    docker-compose logs --tail=100 corrector-tal

Ne jamais copier un en-tête `Cookie:`, la valeur d'un code email ou une
clé SMTP dans les rapports de diagnostic partagés.

## Alignement du proxy SWAG sur Journalia

Un exemple vérifiable de configuration se trouve dans
`deploy/swag/universite-tal.subfolder.conf`. Les deux fichiers transmis
par le mainteneur différaient : TAL déclarait `X-Script-Name`,
`X-Forwarded-Prefix` et `X-Forwarded-Host`, tandis que Journalia
déclarait aussi explicitement `X-Forwarded-Proto $scheme` et
`Host $host`. Ajouter ces deux lignes dans TAL tout en conservant
le `rewrite` existant et le nom `corrector-tal:5001`.

La modification doit être testée dans le conteneur SWAG avec
`nginx -t` et activée par son rechargement Nginx, pas par un
`docker-compose` du correcteur. Elle n'est **pas appliquée
automatiquement** depuis le dépôt TAL.

## Présentation des fiches et barèmes (novembre 2026)

Les intitulés des TD3, TD4, TD5 et TD6 initiaux ne comportent plus
la mention « Synthèse historique ». Le devoir du S1 est libellé
« Devoir maison intermédiaire S1 ».

Dans chaque fiche individuelle S1, les approfondissements A/B/C sont
**affichés immédiatement sous le TD principal** auquel ils se rapportent.
Il n'y a plus de section indépendante « Approfondissement ». Les
identifiants techniques `td3-one-s1`, `td3-bis-s1`, `td3-ter-s1`
restent inchangés pour la compatibilité des dépôts et journaux,
mais les noms pédagogiques et nouveaux dossiers sont bien
`S1_TD3_A/B/C` (voir `MIGRATION_PHYSIQUE_S1_V2.md`).

**Conversion d'affichage uniquement** : les min/max des TD, variantes
et révisions sont ramenés sur 10 ; les devoirs maison et les contrôles
sont présentés sur 20. Chaque dénominateur provient du `MAX_SCORE_TOTAL`
du correcteur Python correspondant, pas du nombre de fichiers ni du
barème d'un autre TD. La conversion conserve deux décimales, avec
arrondi conventionnel. Si un score contient un bonus au-dessus du
maximum théorique, il n'est pas plafonné arbitrairement. Les CSV
`progression_S1/S2/S3.csv` et les journaux gardent leurs scores bruts.
Les anciens contrats continuent d'être comptabilisés pour la
participation sans conversion ni mélange de leurs notes.

**Actualisation** : après une soumission correctement enregistrée,
`process_submission()` appelle `refresh_progression()` qui régénère
les exports du volume privé. La fiche enseignant relit ces CSV et les
journaux historiques **à chaque nouvelle consultation**, sans cache
applicatif des scores. Il faut rouvrir la fiche ou actualiser le
navigateur pour voir un dépôt récent. Une erreur de consolidation
n'annule pas le dépôt et peut retarder sa visibilité ; consulter les
journaux applicatifs dans ce cas.
