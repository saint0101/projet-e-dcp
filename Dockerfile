# Utiliser une image Python et la version Alpine
FROM python:3.9-alpine3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Définir le chemin pour inclure le binaire du Python de l'environnement virtuel
ENV PATH="/py/bin:$PATH"

# Changer l'utilisateur à "django-user"
USER django-user
