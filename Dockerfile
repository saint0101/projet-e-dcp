# Utiliser une image Alpine avec Python
FROM python:3.12-alpine

# Installer les dépendances nécessaires, y compris Git
RUN apk update && apk add --no-cache \
       git \
       tzdata \
       curl \
       zlib-dev \
       # libressl-dev \
       readline-dev \
       yaml-dev \
       libxml2-dev \
       libxslt-dev \
       bash \
       libffi-dev \
       poppler-utils \
       imagemagick \
       imagemagick-dev \
       imagemagick-libs \
       nodejs \
       yarn \
       build-base \
       # postgresql-dev \
       postgresql-client
       # wkhtmltopdf

# Spécifier le répertoire de travail dans le conteneur
WORKDIR /app_edcp

# Cloner le dépôt GitHub dans le conteneur
RUN git clone -b dev_edcp_v0.1 https://github.com/saint0101/projet-e-dcp.git .

# Copier les fichiers de l'application
COPY ./app_edcp /app_edcp

# Installer les dépendances Python
RUN pip3 install --trusted-host pypi.python.org -r requirements.django5.txt

# Ajouter le nom de l'instructeur (étiquette maintainer)
LABEL maintainer="projetedcp.ci"

# Définir l'environnement non tamponné pour Python
ENV PYTHONUNBUFFERED=1

# Exposer le port 8088
EXPOSE 8088

# Déclaration d'une variable d'environnement DEV avec une valeur par défaut false
ARG DEV=false

# Copier le fichier requirements.dev.txt dans le répertoire de travail
COPY requirements.django5.txt /tmp/requirements.dev.txt

# Installer les dépendances de développement si DEV est défini à true
RUN if [ "$DEV" = "true" ]; then pip install -r /tmp/requirements.dev.txt; fi

# Installer flake8
RUN pip install flake8

# Changer l'utilisateur à "django-user"
RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user

USER django-user
