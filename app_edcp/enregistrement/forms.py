from django import forms
from base_edcp.models import Enregistrement

class EnregistrementForm(forms.ModelForm):
  class Meta:
    model = Enregistrement
    fields = [
        'typeclient',
        'raisonsociale',
        'rccm',
        'representant',
        'secteur',
        'telephone',
        'email_contact',
        'site_web',
        'pays',
        'ville',
        'adresse_geo',
        'gmaps_link',
        'adresse_bp',
        'effectif',
        'presentation',
        'type_piece',
        'num_piece',
        'file_piece',
        'file_rccm',
    ]
    widgets = {
      'type-piece': forms.RadioSelect()
    }