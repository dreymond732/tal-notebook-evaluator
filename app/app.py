# Fichier: app/app.py
from flask import Flask
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

    # Initialisation du dossier racine des soumissions
    os.makedirs(outils.BASE_DIR, exist_ok=True)

    # Blueprints
    from routes import main_bp
    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, port=5001)