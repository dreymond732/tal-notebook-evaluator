# Accès enseignant TAL : session SWAG et code personnel réutilisable

## Diagnostic du préfixe public

La correction de navigation repose sur `tal_url_for` et le chemin de cookie
configuré côté correcteur. Elle n'impose **pas** de modification de SWAG si les
pages et formulaires sous `/universite/tal/` fonctionnent déjà.

Pour le déploiement sous ce chemin, définir dans le fichier `.env` du
répertoire `docker-compose.yml` :

```dotenv
TAL_SESSION_COOKIE_NAME=tal_corrector_session
TAL_SESSION_COOKIE_PATH=/universite/tal/
```

SWAG doit transmettre l'HTTPS d'origine (`X-Forwarded-Proto: https`),
le nom d'hôte correct et idéalement
`X-Forwarded-Prefix: /universite/tal`. Un en-tête `X-Forwarded-Prefix`
absent ne doit pas casser les liens corrigés, mais le cookie doit être
rattaché au chemin réellement visible par le navigateur.

Si l'enseignant voit un formulaire de connexion après avoir déjà
ouvert une session, examiner :
- le code initial n'est utilisable qu'une seule fois dans le mode historique ;
- une session enseignante est valide pendant **2 heures**, même si le cookie
  Flask est conservé jusqu'à **12 heures** ;
- un redémarrage avec une autre `FLASK_SECRET_KEY` invalide les sessions ;
- un cookie ancien avec le même nom mais `Path=/` peut perturber les requêtes ;
- un `TAL_SESSION_COOKIE_PATH` erroné empêche le navigateur de renvoyer
  le cookie sur les URL TAL.

Ne jamais communiquer les cookies, mots de passe SMTP ou clés Flask
en clair lors du diagnostic.

## Option : code personnel réutilisable

Cette option est **désactivée par défaut** pour conserver le mécanisme OTP
précédent. Pour obtenir un code personnel durable, ajouter dans `.env` :

```dotenv
TAL_TEACHER_CODE_MODE=reusable
```

Les deux valeurs admises sont `one_time` (défaut, 12 caractères, valable
10 minutes et une seule fois) et `reusable` (20 caractères, sans date
d'expiration automatique).

Puis, après sauvegarde du volume `soumissions/`, reconstruire :

```bash
git pull --ff-only
docker compose up -d --build --force-recreate corrector-tal
docker compose exec -T corrector-tal python send_teacher_code.py
```

La dernière commande **envoie un nouveau code personnel** à l'adresse
`TAL_TEACHER_EMAIL`. Le code initialement reçu comme OTP ne peut pas être
rendu réutilisable rétroactivement. Le code reste valable après
déconnexion et expiration de session. **Ne relancez pas la commande pour
vous reconnecter** : chaque nouvel envoi remplace le précédent.

Le code doit être conservé comme un mot de passe : utiliser un gestionnaire
de mots de passe, ne pas partager l'email, ne pas déposer le code en Git,
ne pas le placer dans `.env`.

Une modification de `TAL_TEACHER_EMAIL` ou une rotation de
`FLASK_SECRET_KEY` invalide la validation des anciens codes.
Les codes sont conservés uniquement sous forme de dérivés PBKDF2 salés
dans `soumissions/suivi/acces_enseignant.sqlite3` et l'email autorisé
est lié au code par une empreinte HMAC. Les tentatives sont limitées par
IP et globalement. Aucune route HTTP ne peut envoyer ni révoquer le code.

### Rotation ou révocation

Pour remplacer un code oublié ou potentiellement compromis :

```bash
docker compose exec -T corrector-tal python send_teacher_code.py
```

La rotation invalide le précédent code **et les sessions associées**.
L'envoi SMTP est réalisé dans une transaction SQLite : s'il échoue,
l'ancien code reste valable.

Pour révoquer sans en envoyer un nouveau :

```bash
docker compose exec -T corrector-tal python send_teacher_code.py --revoke
```

Après révocation, les sessions liées au code sont également refusées.
La connexion requiert alors l'émission d'un nouveau code en mode
`reusable`. Un changement de mode désactive l'authentification par le
mode inactif, mais ne supprime pas de lui-même une ancienne empreinte :
utiliser `--revoke` pour supprimer un code réutilisable conservé.

### Ce que cette option ne change pas

Chaque session web reste limitée à 2 heures ; le code réutilisable sert
à ouvrir une **nouvelle session** sans redemander un email.

Les relevés restent privés, les vérifications CSRF des opérations
enseignantes sont maintenues, et les étudiants ne peuvent pas demander
ce code depuis le portail. Cette authentification reste dépendante de
la sécurité du code personnel et de l'adresse email configurée.
