# Fichier: app/app.py
from flask import Flask
from datetime import timedelta
import os
import re
import outils
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app() -> Flask:
    """Application Factory."""
    app = Flask(__name__, template_folder='templates')

    # Configuration Proxy pour avoir les bonnes IP derrière Nginx/Traefik
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    # Configuration Sécurité
    # Utilise une variable d'environnement ou une clé par défaut générique
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'cle_secrete_bases_tal_2026')

    # Un cookie dédié au correcteur TAL, indépendant de Journalia et des autres
    # applications hébergées sur le même domaine. Le chemin est le chemin PUBLIC
    # derrière SWAG, pas le chemin interne reçu par Flask après la réécriture.
    cookie_name = os.getenv('TAL_SESSION_COOKIE_NAME', 'tal_corrector_session').strip()
    cookie_path = os.getenv('TAL_SESSION_COOKIE_PATH', '/').strip()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', cookie_name):
        raise ValueError('TAL_SESSION_COOKIE_NAME invalide')
    if (not cookie_path.startswith('/') or not cookie_path.endswith('/')
            or '//' in cookie_path or any(c.isspace() or c in ';\\?#' for c in cookie_path)):
        raise ValueError('TAL_SESSION_COOKIE_PATH invalide (chemin public avec / final attendu)')
    app.config.update(
        SESSION_COOKIE_NAME=cookie_name,
        SESSION_COOKIE_PATH=cookie_path,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=True,
        PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
    )

    # Après passage de Path=/ à /universite/tal/, le navigateur peut
    # conserver deux cookies du MÊME nom. L'ancien cookie racine peut
    # masquer la nouvelle session (et faire échouer tous les POST CSRF).
    # Éteindre explicitement l'ancien Path=/ ; ne jamais toucher au cookie
    # générique "session", éventuellement utilisé par d'autres applis.
    if cookie_path != '/':
        @app.after_request
        def expire_previous_root_cookie(response):
            from flask import request
            if request.path.startswith(('/enseignant/progression',
                                        '/ma-progression')):
                response.delete_cookie(
                    cookie_name, path='/', secure=True,
                    httponly=True, samesite='Lax',
                )
            return response

    # Initialisation du dossier racine des soumissions
    os.makedirs(outils.BASE_DIR, exist_ok=True)

    # Blueprints
    from routes import main_bp, validate_evaluator_semesters
    validate_evaluator_semesters()
    app.register_blueprint(main_bp)
    from student_routes import student_bp
    app.register_blueprint(student_bp)
    from teacher_routes import teacher_bp
    app.register_blueprint(teacher_bp)
    from tal_urls import tal_url_for
    app.jinja_env.globals['tal_url_for'] = tal_url_for

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, port=5001)