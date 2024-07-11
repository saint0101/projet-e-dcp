from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

# user/views.py
def index(request):
    return HttpResponse("Bienvenue sur la page d'accueil de l'application Utilisateurs")
