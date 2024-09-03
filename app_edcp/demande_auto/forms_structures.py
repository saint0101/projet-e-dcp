"""
Dictionnaires décrivant la présentation des formulaires de demandes d'autorisation,
sous forme de formulaire multisteps
"""

FORM_STRUCTURE_TRAITEMENT = [
  {'label': 'finalite',
   'display_name': 'Finalité du traitement',
   'fields': ['finalite', 'sous_finalites', 'autre_sous_finalite', 'description_traitement',]
  },

  {'label': 'transparence',
   'display_name': 'Transparence',
   'fields': ['personnes_concernees', 'fondement_juridique', 'description_fondement', 'mode_consentement', 'autre_mode_consentement', 'procedures']
  },

  {'label': 'donnees',
   'display_name': 'Données traitées',
   'fields': ['donnees_traitees', 'autre_donnees_traitees', ]
  },

  {'label': 'transferts',
   'display_name': 'Transferts de données',
   'fields': ['transferts', ]
  },

  {'label': 'interconnexions',
   'display_name': 'Interconnexions de données',
   'fields': ['interconnexions', ]
  },

  {'label': 'securite',
   'display_name': 'Mesures de sécurité',
   'fields': ['mesures_securite']
  },

  {'label': 'documents',
   'display_name': 'Documents justificatifs',
   'fields': ['file_consentement', 'file_cgu']
  },

]

FORM_STRUCTURE_TRANSFERT = [
  {'label': 'finalite',
   'display_name': 'Finalité du traitement',
   'fields': ['finalite', 'sous_finalites', 'description_traitement', 'personnes_concernees']
  },

  {'label': 'details',
   'display_name': 'Détails du transfert',
   'fields': ['destination', 'motif_transfert']
  },

  {'label': 'securite',
   'display_name': 'Sécurité',
   'fields': ['mesures_securite']
  },
]

FORM_STRUCTURE_VIDEO = [
  {'label': 'finalite',
   'display_name': 'Finalité du traitement',
   'fields': ['finalite', 'sous_finalites', 'description_traitement', 'personnes_concernees']
  },

  {'label': 'details',
   'display_name': 'Détails du dispositf',
   'fields': ['types_cameras', 'nb_cameras']
  },

  {'label': 'securite',
   'display_name': 'Sécurité',
   'fields': ['mesures_securite']
  },
]

FORM_STRUCTURE_BIOMETRIE = [
  {'label': 'finalite',
   'display_name': 'Finalité du traitement',
   'fields': ['finalite', 'sous_finalites', 'description_traitement', 'personnes_concernees']
  },

  {'label': 'details',
   'display_name': 'Détails du dispositf',
   'fields': ['types_dispositifs', 'nb_dispositifs']
  },

  {'label': 'securite',
   'display_name': 'Sécurité',
   'fields': ['mesures_securite']
  },
]


def get_form_fields(form_structure, hide_files=False):
  fields = []
  for elmt in form_structure:
    if elmt['label'] == 'files' and hide_files:
      continue
    fields += elmt['fields']

  return fields