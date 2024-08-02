from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base_edcp import models

# Create your views here.


@login_required(login_url=reverse_lazy('login'))
def index(request):
  """
  Vue qui génère la page de tableau de bord d'un utilisateur
  Accepte en paramètre la requête HTTP (objet request).
  Renvoie la page de tableau de bord avec le contexte de menu correspondant à l'utilisateur.
  """
  user = request.user

  # Récupération des types d'autorisation depuis la base de données
  types_demandes = models.TypeDemandeAutorisation.objects.all()

  # Vérifiez si l'utilisateur est staff et définissez le contexte en conséquence
  """if user.is_staff:
      context = {
          'menu': MENU_MGR,
          'types_demandes': types_demandes
      }
  else:
    context = {
        'menu': MENU_CLIENT,
        'types_demandes': types_demandes
    }"""

  messages.success(request, f'Bienvenue {user} !') # message d'accueil. Utilise le framework de messages de Django.
  print(f'==== messages : {messages}')
  return render(request, 'dashboard/index.html')


def custom_permission_denied_view(request):
  """
  Vue qui gère l'affichage de la page 403 en cas de permission refusée.
  Renvoie la page 403.
  """
  return render(request, '403.html', context={'message': ''})
