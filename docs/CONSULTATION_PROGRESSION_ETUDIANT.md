# Accès étudiant à « Ma progression » sans SSO

## Principe validé

Le premier utilisateur qui connaît un numéro étudiant présent dans les synthèses
et contrôle une adresse email peut associer **définitivement** cet email au numéro.
Cette méthode dite de premier rattachement (« first claim ») ne vérifie pas
l'identité administrative de l'étudiant. En particulier, un étudiant pourrait
revendiquer le numéro d'un autre avant lui. Le contrôle de l'email prouve la
maîtrise de cette boîte, pas la titularité du numéro.

L'association n'est validée qu'après l'utilisation du code expédié par email,
jamais au moment de la simple saisie d'une adresse. Le premier code, aléatoire
(18 caractères parmi un alphabet sans ambiguïtés), reste réutilisable pour
consulter le suivi après cette validation.

Les demandes suivantes :
- sur le même numéro et un email différent : **aucun envoi ni modification** ;
- sur le même numéro et le bon email : nouveau code envoyé, l'ancien reste
  valable jusqu'à validation du nouveau ; la confirmation remplace l'ancien,
  et invalide les sessions établies avant la rotation.

Les codes ne figurent jamais dans les URL, journaux, exports ou rapports ; la
base privée ne conserve que leur dérivé cryptographique (PBKDF2-HMAC avec sel).
L'interface nécessite numéro, email associé et code pour l'ouverture de
session ; une session authentifiée dure au plus 12 heures. Un nouveau code
remplace le précédent, mais le code confirmé n'expire pas automatiquement.
En cas de divulgation, une demande de remplacement au même email est nécessaire.

## Portée des données visibles

La page /ma-progression, depuis l'accueil du correcteur TAL, présente
exclusivement les TD formatifs de S1, S2, S3 : essais, minimum et maximum
sur le barème propre à chaque activité. Les anciens correcteurs sont exclus
par le consolidateur, les versions historiques par le filtrage habituel.
Les **contrôles et devoirs maison restent privés**, même lorsque leurs
scores figurent dans le CSV consolidé de l'enseignant.

Les relevés des autres étudiants, les cahiers et les rapports HTML ne sont
jamais transmis au navigateur. Le serveur sélectionne le numéro associé
à la session côté serveur, et ne prend aucun numéro depuis l'URL
pour lire une progression. Les sorties ne sont pas mises en cache.

L'accès s'appuie sur soumissions/suivi/progression_S1.csv,
progression_S2.csv et progression_S3.csv : ces fichiers sont produits
automatiquement par progression.py après chaque dépôt.

## Configuration indispensable

Configurer dans le fichier .env privé utilisé par Docker Compose (ne jamais
le commiter ni le communiquer aux étudiants) :

    FLASK_SECRET_KEY=cle-longue-aleatoire-et-privee
    TAL_ACADEMIC_YEAR=2026-2027
    TAL_SMTP_HOST=smtp.exemple.invalid
    TAL_SMTP_PORT=465
    TAL_SMTP_SECURITY=ssl
    TAL_SMTP_FROM=enseignant@exemple.invalid
    TAL_SMTP_USER=identifiant-smtp
    TAL_SMTP_PASSWORD=secret-smtp

Pour un relais STARTTLS, renseigner TAL_SMTP_SECURITY=starttls et son port
(d'ordinaire 587). Les certificats TLS sont vérifiés. Les paramètres
d'envoi doivent correspondre à un compte ou domaine validé par le
prestataire ; aucun service SMTP gratuit n'est présumé disponible.
Les SMS ne sont pas intégrés, pour éviter d'ouvrir un canal payant ou
non maîtrisé.

La page refuse l'accès tant que l'année universitaire, la clé Flask et
l'envoi SMTP ne sont pas configurés. Le site doit être exposé uniquement
en HTTPS (SESSION_COOKIE_SECURE). Les requêtes POST sont protégées
par un jeton CSRF et les demandes/essais sont limités par numéro et IP.
Les réponses de demande de code restent volontairement identiques pour
un numéro connu, inconnu ou un email non autorisé, afin d'éviter
de divulguer les associations.

Dans une nouvelle installation, lancer la consolidation une première
fois, avec l'année configurée, avant de présenter le portail.

## Réinitialisation administrative

Si un numéro étudiant a été associé à un mauvais email, aucune modification
n'est possible depuis la page publique. Après vérification de l'identité
du demandeur par un canal indépendant, révoquer l'association depuis
le conteneur :

    docker compose exec corrector-tal python reset_student_access.py --numero 00123 --confirmer

La révocation supprime l'association et tout code en attente ; les
sessions existantes échouent au prochain contrôle. La demande suivante
peut établir une nouvelle adresse. La progression et les CSV des
évaluations ne sont pas modifiés.

## Tests de sécurité et limites

    python -m unittest discover -s tests -p test_student_portal.py -v
    python -m unittest discover -s tests -v

Les tests utilisent un serveur SMTP simulé et des numéros/noms fictifs ;
ils ne déclenchent aucun envoi externe. Ils couvrent l'inscription différée,
le rattachement exclusif, les codes renouvelables, la séparation des
étudiants, l'exclusion des contrôles, le refus hors configuration,
la protection CSRF et les limites de débit.

**Limite à assumer :** le modèle « premier email vérifié » ne suffit pas
à garantir que le demandeur est le titulaire universitaire du numéro.
Un import administratif ultérieur ou une validation enseignante serait
nécessaire pour cette garantie. Cette fonctionnalité ne constitue pas
un accès aux notes officielles.
