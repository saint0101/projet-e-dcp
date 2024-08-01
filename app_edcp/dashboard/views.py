from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required(login_url=reverse_lazy('login'))
def index(request):
  """
  Vue qui génère la page de tableau de bord d'un utilisateur
  Accepte en paramètre la requête HTTP (objet request).
  Renvoie la page de tableau de bord avec le contexte de menu correspondant à l'utilisateur.
  """
  user = request.user
  messages.success(request, f'Bienvenue {user} !') # message d'accueil. Utilise le framework de messages de Django.

  return render(request, 'dashboard/index.html')


def custom_permission_denied_view(request):
  """
  Vue qui gère l'affichage de la page 403 en cas de permission refusée.
  Renvoie la page 403.
  """
  return render(request, '403.html', context={'message': ''})

