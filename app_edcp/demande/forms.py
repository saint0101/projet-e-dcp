import json
from django import forms

from demande_auto.models import EchelleNotation
from demande.models import (
  Commentaire, 
  Demande, 
  ReponseDemande, 
  TypeReponse, 
  CritereEvaluation, 
  CategorieDemande,
  )


class ValidateForm(forms.Form):
  """ Formulaire de validation de projet de réponse. """
  observations = forms.CharField(
    label='Observations', 
    required=False,
    widget=forms.Textarea(attrs={'rows': 3}),
  )


def generate_analyse_form(categorie_demande, analyse=None):
  AVIS_CHOICES = [('', '---------'),] + [(False, 'Refuser'), (True, 'Autoriser')]
  observations = forms.CharField(
    label='Observations', 
    required=False,
    widget=forms.Textarea(attrs={'rows': 4}),
  )
  prescriptions = forms.CharField(
    label='Prescriptions',
    required=False,
    widget=forms.Textarea(attrs={'rows': 4}),
  )
  avis_juridique = forms.BooleanField(
    label='Avis juridique',
    required=False,
    widget=forms.Select(choices=AVIS_CHOICES)
  )
  
  class AnalyseDemandeForm(forms.Form):
    """ Formulaire d'analyse d'une demande """
    pass
  
  critere_fields = CritereEvaluation.objects.filter(categorie_demande=categorie_demande)
  NOTATION_CHOICES = [('', '---------'),] + [(notation.id, notation.description) for notation in EchelleNotation.objects.all()]

  deserialized_data = {}
  if analyse and analyse.evaluation :
    deserialized_data = json.loads(analyse.evaluation)

  for field in critere_fields:
    if field.label in deserialized_data:
      form_field = forms.CharField(
        label=field.field_name,
        required=field.field_required,
        widget=forms.Select(choices=NOTATION_CHOICES),
        initial=deserialized_data[field.label],
      )
    else:
      form_field = forms.CharField(
        label=field.field_name,
        required=field.field_required,
        widget=forms.Select(choices=NOTATION_CHOICES),
      )
    AnalyseDemandeForm.base_fields[field.label] = form_field
  
  AnalyseDemandeForm.base_fields['observations'] = observations
  AnalyseDemandeForm.base_fields['prescriptions'] = prescriptions
  AnalyseDemandeForm.base_fields['avis_juridique'] = avis_juridique
  
  return AnalyseDemandeForm


class CommentaireForm(forms.ModelForm):
  """ Formulaire d'ajout de commentaires """
  message = forms.CharField(
    label='Contenu du message', 
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