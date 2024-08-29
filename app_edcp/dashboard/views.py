from multiprocessing import context
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base_edcp.models import Enregistrement, User
from correspondant.models import Correspondant


# Create your views here.


def page_en_construction(request):
  """ Vue page en construction """
  return render(request, 'dashboard/construction.html')



@login_required(login_url=reverse_lazy('connexion:login'))
def index(request):
  """
  Vue qui génère la page de tableau de bord d'un utilisateur
  Accepte en paramètre la requête HTTP (objet request).
  Renvoie la page de tableau de bord avec le contexte de menu correspondant à l'utilisateur.
  """
  #user = request.user
  # Récupération des types d'autorisation depuis la base de données
  # types_demandes = models.TypeDemandeAutorisation.objects.all()

  # Si l'utilisateur doit rénitialiser son mot de passe (valable pour les comptes créés dynamiquement)
  if request.user.must_reset:
    messages.info(request, 'Vous devez réinitialiser votre mot de passe.')
    return redirect('connexion:password_change')

  # Si l'utilisateur n'est pas un manager
  if not request.user.is_staff:
    return render(request, 'dashboard/index.html')
  
  # Si l'utilisateur est un manager, préparation des données pour son tableau de bord
  context = {}
  organisations = Enregistrement.objects.order_by('-created_at')[:4] # Liste des 4 derniers enregistrements
  correspondants = Correspondant.objects.order_by('-created_at')[:4] # Liste des 4 derniers correspondants
  users = User.objects.order_by('-created_at')[:4] # Liste des 4 derniers utilisateurs

  context['organisations'] = organisations
  context['correspondants'] = correspondants
  context['users'] = users

  return render(request, 'dashboard/index_manager.html', context=context)


def custom_permission_denied_view(request):
  """
  Vue qui gère l'affichage de la page 403 en cas de permission refusée.
  Renvoie la page 403.
  """
  return render(request, '403.html', context={'message': ''})
