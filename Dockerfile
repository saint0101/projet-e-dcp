FROM python:3.12-alpine

RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.20/main" > /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/v3.20/community" >> /etc/apk/repositories && \
    echo "http://dl-3.alpinelinux.org/alpine/v3.20/main" >> /etc/apk/repositories && \
    echo "http://dl-3.alpinelinux.org/alpine/v3.20/community" >> /etc/apk/repositories

# Installer les dépendances nécessaires, y compris Git
RUN apk update && apk add --no-cache \
       git \
       tzdata \
       curl \
       zlib-dev \
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
       postgresql-client

# Spécifier le répertoire de travail dans le conteneur
WORKDIR /app_edcp

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

# Commande par défaut à exécuter
CMD ["python", "manage.py", "runserver", "0.0.0.0:8088"]