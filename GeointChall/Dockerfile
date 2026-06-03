# 1. Utiliser une image Python officielle et légère
FROM python:3.12-slim

# 2. Définir le dossier de travail dans le conteneur
WORKDIR /app

# 3. Copier les fichiers de dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier le reste du code de l'application (app.py et templates/)
COPY . .

# 5. Informer Docker que l'application écoute sur le port 5000
EXPOSE 5000

# 6. Commande pour lancer l'application
CMD ["python", "app.py"]
