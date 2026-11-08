# Fichier: app/app.py
from flask import Flask
from datetime import timedelta
import os
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

    # Cookies signés, non accessibles en JavaScript, servis uniquement sous TLS.
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',
                      SESSION_COOKIE_SECURE=True,
                      PERMANENT_SESSION_LIFETIME=timedelta(hours=12))

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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, port=5001)