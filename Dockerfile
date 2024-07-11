# Utiliser une image Python et la version Alpine
FROM python:3.9-alpine3.13


#RUN apk update \
#    && apk add --update --no-cache tzdata wkhtmltopdf \
#       curl zlib-dev libressl-dev readline-dev yaml-dev libxml2-dev libxslt-dev bash \
#       curl-dev libffi-dev \
#       poppler-utils imagemagick imagemagick-dev imagemagick-libs \
#       nodejs yarn build-base git postgresql-dev postgresql-client

# Ajouter le nom de l'instructeur (étiquette maintainer)
LABEL maintainer="projetedcp.ci"

# Définir l'environnement virtuel (recommandé lors de l'exécution de Python dans un conteneur Docker)
ENV PYTHONUNBUFFERED 1

# Copier le contenu du fichier requirements.txt dans le fichier /tmp/requirements.txt sur le serveur dans le conteneur
COPY ./requirements.txt /tmp/requirements.txt

# Copier le contenu du fichier requirements.dev.txt dans le fichier /tmp/requirementsdev..txt sur le serveur dans le conteneur
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copier le fichier app dans le répertoire de travail sur le conteneur
COPY ./app_edcp /app_edcp

# Spécifier le répertoire de travail dans le conteneur
WORKDIR /app_edcp

# Exposer le port 8000 (cela ne publie pas le port, mais indique que l'application à l'intérieur utilise le port 8000)
EXPOSE 8088

# Installer les dépendances placées dans le dossier requirements.txt
# Créer un environnement virtuel à /py
# Mettre à jour pip dans l'environnement virtuel
# Installer les dépendances depuis le fichier requirements.txt
# ajouter un client postgresql
# Supprimer le répertoire temporaire
# Désactiver le mot de passe pour l'utilisateur ajouté
# Ne pas créer de répertoire de domicile pour l'utilisateur ajouté
# Nom de l'utilisateur ajouté

# Déclaration d'une variable d'environnement DEV avec une valeur par défaut false
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Définir le chemin pour inclure le binaire du Python de l'environnement virtuel
ENV PATH="/py/bin:$PATH"

# istall flake8
RUN pip install flake8

# Changer l'utilisateur à "django-user"
USER django-user
