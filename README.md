# e-DCP

## Description

e-DCP est une application web développée avec Django et Bootstrap. L'application utilise PostgreSQL comme système de gestion de base de données (SGBD). Ce guide vous aidera à configurer et déployer l'application en utilisant Docker et Git.

## Prérequis

- Docker
- Docker Compose
- Git

## Langages et Frameworks Utilisés

- **Framework**: Django, Bootstrap
- **Langages de programmation**: Python, HTML, CSS, JavaScript
- **SGBD**: PostgreSQL
- **Déploiement**: Docker, Git

## Étapes d'installation et de déploiement

### 1. Cloner le projet

Clonez le dépôt Git du projet sur votre machine locale :

```bash
    git clone https://github.com/saint0101/projet-e-dcp.git
```

### 2. Se déplacer dans le dossier du projet

Accédez au répertoire du projet :

```bash
    cd projet-e-dcp
```

### 3. Vérifier l'installation de Docker

Assurez-vous que Docker est installé et en cours d'exécution :

```bash
    docker --version
    docker-compose --version
```

### 4. Création de la base de données

Créez la base de données et appliquez les migrations :

```bash
    docker-compose run --rm app_edcp sh -c "python manage.py makemigrations"
    docker-compose run --rm app_edcp sh -c "python manage.py migrate"
```

### 5. Création de l'utilisateur Django admin

Créez un super utilisateur pour accéder à l'interface d'administration de Django :

```bash
    docker-compose run --rm app_edcp sh -c "python manage.py createsuperuser"
```

### 6. Lancer l'exécuption de l'application

Utiliser docker compose up pour démarrer tous les conteneurs en une fois :

```bash
    docker-compose up -d
```

Ou passer par la commande runserver de Django pour un affichage de l'output dans le terminal :

```bash
    docker-compose run --rm app_edcp sh -c "python manage.py runserver"
```

## Travailler sur le projet

### 1. Se déplacer dans le dossier du projet

Assurez-vous que vous êtes dans le répertoire du projet :

```bash
    cd projet-e-dcp
```

### 2. Créer une nouvelle branche pour travailler sur le projet

Créez une nouvelle branche pour votre travail :

```bash
    git checkout -b ma-nouvelle-branche
```

### 4. Voir les modifications

Vérifiez les modifications que vous avez apportées :

```bash
    git status
    git diff
```

### 5. Pousser les modifications sur votre branche

Poussez vos modifications vers le dépôt distant :

```bash
    git add .
    git commit -m "Description des modifications"
    git push origin ma-nouvelle-branche
```
