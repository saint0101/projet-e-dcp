from django import forms
from base_edcp.models import Enregistrement, TypeClient, TypePiece
from base_edcp import validators

class EnregistrementForm(forms.ModelForm):
  # typeclient = forms.ModelChoiceField(queryset=TypeClient.objects.all(), widget=forms.RadioSelect)
  # raisonsociale = forms.CharField(min_length=2, max_length=100, validators=[validators.validate_charfield, validators.validate_no_special_chars])
  # rccm = forms.CharField(min_length=2, max_length=30, validators=[validators.validate_charfield, validators.validate_no_special_chars, validators.validate_rccm_idu])
  # idu = forms.CharField(required=False, min_length=2, max_length=30, validators=[validators.validate_charfield, validators.validate_no_special_chars, validators.validate_rccm_idu])
  telephone = forms.CharField(min_length=2, max_length=100)
  type_piece = forms.ModelChoiceField(
    required=False,
    label='Type de pièce d\'identité', 
    queryset=TypePiece.objects.all(), 
    widget=forms.RadioSelect
  )

  class Meta:
    model = Enregistrement
    fields = [
        'typeclient',
        'raisonsociale',
        'rccm',
        'idu',
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
        'file_mandat'
    ]


    """ widgets = {
      'type-piece': forms.RadioSelect()
    } """