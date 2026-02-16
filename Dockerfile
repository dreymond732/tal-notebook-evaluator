FROM python:3.12-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# On copie tout le contenu du dossier local ./app dans /app du conteneur
COPY ./app /app/
# On s'assure que le dossier de destination des copies existe
RUN mkdir -p /app/soumissions
EXPOSE 5001
# Commande Gunicorn pointant sur app.py (le fichier) et app (l'objet Flask)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:create_app()", "--workers", "4", "--timeout", "120"]
