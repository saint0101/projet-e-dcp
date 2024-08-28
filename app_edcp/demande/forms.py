from email import message
from typing import Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from demande.models import Commentaire, Demande, ReponseDemande, TypeReponse


class ValidateForm(forms.Form):
  """ Formulaire de validation de projet de réponse. """
  observations = forms.CharField(
    label='Observations', 
    required=False,
    widget=forms.Textarea(attrs={'rows': 3}),
  )



class CommentaireForm(forms.ModelForm):
  """ Formulaire d'ajout de commentaires """
  message = forms.CharField(
    label='Message', 
    required=True,
    widget=forms.Textarea(attrs={'rows': 3}),
  )
  class Meta:
    model = Commentaire
    fields = ['objet', 'message']



class ProjetReponseModelForm(forms.ModelForm):
  """ Formulaire de génération de projet de réponse. """
  type_reponse = forms.ModelChoiceField(
    queryset=TypeReponse.objects.all(),
    widget=forms.RadioSelect
  )
  class Meta:
    model = ReponseDemande
    fields = ['type_reponse', 'titre_destinataire', 'adresse_destinataire']

  def __init__(self, demande=None, *args, **kwargs):
    """ Initialisation du formulaire avec la demande en traitée afin de filtrer les types de réponses possibles. """
    super().__init__(*args, **kwargs)
    # demande = Demande.objects.filter(analyse__projet_reponse=self.instance).last()
    types_reponses = demande.categorie.types_reponses.all()
    self.fields['type_reponse'].queryset = types_reponses



""" TO DELETE """
class ProjetReponseForm(forms.Form):
  """ Formulaire de génération de projet de réponse. Privilégier la version ModelForm ci-dessus. """
  type_reponse = forms.ModelChoiceField(
    queryset=TypeReponse.objects.all(),
    widget=forms.RadioSelect
  )
  titre_destinataire = forms.CharField(
    label='Titre',
  )
  adresse_destinataire = forms.CharField(
    label='Adresse',
  )