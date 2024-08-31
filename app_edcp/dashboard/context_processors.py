# from django.contrib.sites.shortcuts import get_current_site


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
    'icon' : 'building',
    'url' : '',
    'disabled': False, 
    'items' : [
      {
        'text' : 'Enregistrer',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:enregistrement:create',
        'disabled': False,
      },
      {
        'text' : 'Mes organisation',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:enregistrement:list',
        'disabled': False, 
      },
    ], 
  },

  {
    'text' : 'Correspondants',
    'type' : 'sous-menu',
    'id' : 'correspondants',
    'icon' : 'file-earmark-person',
    'url' : '',
    'disabled': False, 
    'items' : [
      {
        'text' : 'Désignations',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:correspondant:index',
        'disabled': False, 
      },
      {
        'text' : 'Informations',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
    ],
  },
  
  {
    'text' : 'Demandes d\'autorisation',
    'id' : 'demande-auto',
    'type' : 'sous-menu',
    'icon' : 'file-earmark-text',
    'url' : '',
    'disabled': False, 
    'items' : [
      {
        'text' : 'Nouvelle demande',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:demande_auto:create',
        'disabled': False, 
      },
      {
        'text' : 'En cours',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
      {
        'text' : 'Mes demandes',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:demande_auto:list',
        'disabled': False, 
      },
    ]
  },
  
  {
    'text' : 'Mise en conformité',
    'id' : 'mise-en-conf',
    'type' : 'sous-menu',
    'icon' : 'patch-check',
    'url' : 'dashboard:construction',
    'disabled': False, 
    'items' : [
      {
        'text' : 'Démarrer',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
      {
        'text' : 'En cours',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
      {
        'text' : 'Mes demandes',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
    ],
  },
  
  {
    'text' : 'Notifications',
    'type' : 'section',
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
    'text' : 'Administration',
    'type' : 'section',
  },

  {
    'text' : 'Listes',
    'id' : 'listes',
    'type' : 'sous-menu',
    'icon' : 'list-nested',
    'url' : '',
    'disabled': False, 
    'items' : [
      {
        'text' : 'Organisations',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:enregistrement:list',
        'disabled': False, 
      },
      {
        'text' : 'Utilisateurs',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:user:list',
        'disabled': False, 
      },
    ], 
  },
  
  {
    'text' : 'Formalités',
    'type' : 'section',
  },

  {
    'text' : 'Demandes',
    'type' : 'sous-menu',
    'id' : 'demandes',
    'icon' : 'file-earmark-person',
    'url' : '',
    'disabled': False, 
    'items' : [
      {
        'text' : 'À traiter',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:demande:liste_a_traiter',
        'disabled': False, 
      },
      {
        'text' : 'Terminées',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
      {
        'text' : 'Toutes les demandes',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:demande:liste_all' ,
        'disabled': False, 
      },
    ],
  },

  {
    'text' : 'Enregistrement',
    'id' : 'enregistrement',
    'type' : 'sous-menu',
    'icon' : 'building',
    'url' : '',
    'disabled': False, 
    'items' : [
      #{
      #  'text' : 'Récent',
      #  'type' : 'sous-menu-item',
      #  'icon' : '',
      #  'url' : 'dashboard:index',
      #  'disabled': False,
      #},
      {
        'text' : 'Toutes les organisation',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:enregistrement:list',
        'disabled': False, 
      },
      {
        'text' : 'Créer',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:enregistrement:create',
        'disabled': False, 
      },
    ], 
  },

  {
    'text' : 'Correspondants',
    'type' : 'sous-menu',
    'id' : 'correspondants',
    'icon' : 'file-earmark-person',
    'url' : '',
    'disabled': False, 
    'items' : [
      {
        'text' : 'Désignations',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:correspondant:list',
        'disabled': False, 
      },
      {
        'text' : 'Informations',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
    ],
  },
  
  {
    'text' : 'Demandes d\'autorisation',
    'id' : 'demande-auto',
    'type' : 'sous-menu',
    'icon' : 'file-earmark-text',
    'url' : '',
    'disabled': False, 
    'items' : [
      {
        'text' : 'Nouvelle demande',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:demande_auto:create',
        'disabled': False, 
      },
      {
        'text' : 'En cours',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
      {
        'text' : 'Toutes les demandes',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:demande_auto:list',
        'disabled': False, 
      },
    ]
  },
  
  {
    'text' : 'Mise en conformité',
    'id' : 'mise-en-conf',
    'type' : 'sous-menu',
    'icon' : 'patch-check',
    'url' : 'dashboard:construction',
    'disabled': False, 
    'items' : [
      {
        'text' : 'Démarrer',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
      {
        'text' : 'En cours',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
      {
        'text' : 'Toutes les demandes',
        'type' : 'sous-menu-item',
        'icon' : '',
        'url' : 'dashboard:construction',
        'disabled': False, 
      },
    ],
  },
  
  {
    'text' : 'Notifications',
    'type' : 'section',
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



def get_menu(request):
  """
  Returns the menu for the given request.
  Parameters:
  - request (HttpRequest) -- The HTTP request object.
  """
  user = request.user
  if user.is_authenticated and user.is_staff :
    return {'get_menu': MENU_MGR} 
  
  return {'get_menu': MENU_CLIENT} 


def get_site_url(request):
  """ Renvoie l'URL du site actuel afind e pouvoir l'afficher dans un template. """
  # print('processing site url : ', get_current_site(request).domain)
  # return {'site_url': 'http://' + get_current_site(request).domain}
  pass