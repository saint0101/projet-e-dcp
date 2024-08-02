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


from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from base_edcp import models

# Create your views here.
"""
Menu à afficher dans barre latérale (sidebar.html) du tableau de bord pour les utilisateurs de type client.
TODO: Prévoir un enregistrement dans la base de données pour les versions futures.
"""
MENU_CLIENT = [
  {
    'text' : 'Formalités',
    'type' : 'section',
  },

  {
    'text' : 'Enregistrement',
    'id' : 'enregistrement',
    'type' : 'sous-menu',
    'icon' : '',
    'url' : '',
    'disabled': False,
    'items' : [
      {
        'text' : 'Enregistrer',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'Mes organisation',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
    ],
  },

  {
    'text' : 'Demandes d\'autorisation',
    'id' : 'demande-auto',
    'type' : 'sous-menu',
    'icon' : '',
    'url' : '',
    'disabled': False,
    'items' : [
      {
        'text' : 'Nouvelle demande',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'En cours',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'Mes demandes',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
    ]
  },

  {
    'text' : 'Mise en conformité',
    'id' : 'mise-en-conf',
    'type' : 'sous-menu',
    'icon' : '',
    'url' : 'dashboard:index',
    'disabled': False,
    'items' : [
      {
        'text' : 'Démarrer',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'En cours',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'Mes demandes',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
    ],
  },

  {
    'text' : 'Notifications',
    'type' : 'section',
  },

  {
    'text' : 'Correspondants',
    'type' : 'sous-menu',
    'id' : 'correspondants',
    'icon' : '',
    'url' : '',
    'disabled': False,
    'items' : [
      {
        'text' : 'Désignation',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'Informations',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
    ],
  },

  {
    'text' : 'Violations',
    'id' : 'violations',
    'type' : 'sous-menu',
    'icon' : '',
    'url' : '',
    'disabled': False,
    'items' : [],
  },

  {
    'text' : 'AIPD',
    'id' : 'aipd',
    'type' : 'sous-menu',
    'icon' : '',
    'url' : '',
    'disabled': False,
    'items' : [],
  },

]

"""
Menu à afficher dans barre latérale (sidebar.html) du tableau de bord pour les utilisateurs de type gestionnaire.
TODO: Prévoir un enregistrement dans la base de données pour les versions futures.
"""
MENU_MGR = [
  {
    'text' : 'Formalités',
    'type' : 'section',
  },

  {
    'text' : 'Enregistrement',
    'id' : 'enregistrement',
    'type' : 'sous-menu',
    'icon' : '',
    'url' : '',
    'disabled': False,
    'items' : [
      {
        'text' : 'Récent',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'Toutes les organisation',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
    ],
  },

  {
    'text' : 'Demandes d\'autorisation',
    'id' : 'demande-auto',
    'type' : 'sous-menu',
    'icon' : '',
    'url' : '',
    'disabled': False,
    'items' : [
      {
        'text' : 'Nouvelle demande',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'En cours',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'Toutes les demandes',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
    ]
  },

  {
    'text' : 'Mise en conformité',
    'id' : 'mise-en-conf',
    'type' : 'sous-menu',
    'icon' : '',
    'url' : 'dashboard:index',
    'disabled': False,
    'items' : [
      {
        'text' : 'Démarrer',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'En cours',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'Toutes les demandes',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
    ],
  },

  {
    'text' : 'Notifications',
    'type' : 'section',
  },

  {
    'text' : 'Correspondants',
    'type' : 'sous-menu',
    'id' : 'correspondants',
    'icon' : '',
    'url' : '',
    'disabled': False,
    'items' : [
      {
        'text' : 'Désignation',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
      {
        'text' : 'Informations',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:index',
        'disabled': False,
      },
    ],
  },

  {
    'text' : 'Violations',
    'id' : 'violations',
    'type' : 'sous-menu',
    'icon' : '',
    'url' : '',
    'disabled': False,
    'items' : [],
  },

  {
    'text' : 'AIPD',
    'id' : 'aipd',
    'type' : 'sous-menu',
    'icon' : '',
    'url' : '',
    'disabled': False,
    'items' : [],
  },

]



# def get_menu(req)
"""

@login_required(login_url=reverse_lazy('login'))
def index(request):

  Vue qui génère la page de tableau de bord d'un utilisateur
  Accepte en paramètre la requête HTTP (objet request).
  Renvoie la page de tableau de bord avec le contexte de menu correspondant à l'utilisateur.

  user = request.user
  if user.is_staff :
    return render(request, 'dashboard/index.html', context={'menu': MENU_MGR})

  return render(request, 'dashboard/index.html', context={'menu': MENU_CLIENT})


"""
@login_required(login_url=reverse_lazy('login'))
def index(request):
    """
    Vue qui génère la page de tableau de bord d'un utilisateur.
    Accepte en paramètre la requête HTTP (objet request).
    Renvoie la page de tableau de bord avec le contexte de menu correspondant à l'utilisateur.
    """
    user = request.user

    # Récupération des types d'autorisation depuis la base de données
    types_demandes = models.TypeDemandeAutorisation.objects.all()

    # Vérifiez si l'utilisateur est staff et définissez le contexte en conséquence
    if user.is_staff:
        context = {
            'menu': MENU_MGR,
            'types_demandes': types_demandes
        }
    else:
        context = {
            'menu': MENU_CLIENT,
            'types_demandes': types_demandes
        }

    # Rendu du template avec le contexte approprié
    return render(request, 'dashboard/index.html', context=context)



"""
Vue qui gère l'affichage de la page 403 en cas de permission refusée
"""
def custom_permission_denied_view(request):
  return render(request, '403.html', context={'message': ''})


""" def index_client(request):
  return render(request, 'dashboard/client/index_c.html', context={'menu': MENU_CLIENT})


def index_mgr(request):
  if not request.user.is_authenticated :
    return redirect('dashboard:index_client')

  return render(request, 'dashboard/manager/index_m.html') """
