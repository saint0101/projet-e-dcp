from django import forms
from base_edcp.models import Enregistrement

class EnregistrementForm(forms.ModelForm):
  class Meta:
    model = Enregistrement
    fields = [
        'typeclient',
        'raisonsociale',
        'representant',
        'secteur',
        'presentation',
        'telephone',
        'email_contact',
        'site_web',
        'pays',
        'ville',
        'adresse_geo',
        'gmaps_link',
        'adresse_bp',
        'effectif',
        'type_piece',
        'num_piece',
    ]
    widgets = {
      'type-piece': forms.RadioSelect()
    }