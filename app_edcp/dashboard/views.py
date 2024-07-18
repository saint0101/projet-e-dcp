from django.shortcuts import render, redirect

# Create your views here.
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

def index(request):
  if request.user.is_authenticated :
    return redirect('dashboard:index_mgr')
  
  return redirect('dashboard:index_client')


def index_client(request):
  """ Vue tableau de bord usager"""
  return render(request, 'dashboard/client/index_c.html', context={'menu': MENU_CLIENT})


def index_mgr(request):
  """ Vue tableau de bord manager"""
  if not request.user.is_authenticated :
    return redirect('dashboard:index_client')
  
  return render(request, 'dashboard/manager/index_m.html')
