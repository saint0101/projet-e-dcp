"""
Dictionnaires décrivant la présentation des formulaires de demandes d'autorisation,
sous forme de formulaire multisteps
"""

FORM_STRUCTURE_TRAITEMENT = [
  {'label': 'finalite',
   'display_name': 'Finalité du traitement',
   'fields': ['finalite', 'sous_finalites', 'personnes_concernees']
  },

  {'label': 'transparence',
   'display_name': 'Transparence',
   'fields': ['fondement_juridique', 'procedures']
  },

  {'label': 'securite',
   'display_name': 'Sécurité',
   'fields': ['mesures_securite']
  },
]

FORM_STRUCTURE_TRANSFERT = [
  {'label': 'finalite',
   'display_name': 'Finalité du traitement',
   'fields': ['finalite', 'sous_finalites', 'personnes_concernees']
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
   'fields': ['finalite', 'sous_finalites', 'personnes_concernees']
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
   'fields': ['finalite', 'sous_finalites', 'personnes_concernees']
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