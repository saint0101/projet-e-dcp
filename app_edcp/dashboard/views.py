from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url=reverse_lazy('login'))
def index(request):
  """
  Vue qui génère la page de tableau de bord d'un utilisateur
  Accepte en paramètre la requête HTTP (objet request).
  Renvoie la page de tableau de bord avec le contexte de menu correspondant à l'utilisateur.
  """
  user = request.user
  
  return render(request, 'dashboard/index.html')



"""
Vue qui gère l'affichage de la page 403 en cas de permission refusée
"""
def custom_permission_denied_view(request):
  return render(request, '403.html', context={'message': ''})

