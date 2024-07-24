from django import forms
from .models import Correspondant

class DPOForm(forms.ModelForm):
  class Meta:
    model = Correspondant
    """fields = [
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
    ]"""

    fields = '__all__'