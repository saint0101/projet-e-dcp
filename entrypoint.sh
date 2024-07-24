#!/bin/sh
# Appliquez les migrations de la base de données
python manage.py migrate
# Démarrez le serveur Django
python manage.py runserver 0.0.0.0:8088