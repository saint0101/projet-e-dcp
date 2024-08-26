from email import message
from django import forms
from demande.models import Commentaire


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
