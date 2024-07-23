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
    'icon' : '',
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
    request (HttpRequest): The HTTP request object.
  Returns:
    list: The menu for the user.
  """
  user = request.user
  if user.is_authenticated and user.is_staff :
    return {'get_menu': MENU_MGR} 
  
  return {'get_menu': MENU_CLIENT} 