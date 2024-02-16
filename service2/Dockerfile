# Utilisez une image Python comme base
FROM python:3.9

# Copiez les fichiers de l'application dans le conteneur
COPY . /app

# Définissez le répertoire de travail
WORKDIR /app

# Installez les dépendances de l'application
RUN pip install -r requirements.txt

# Commande pour démarrer l'application
CMD ["python", "app.py"]
