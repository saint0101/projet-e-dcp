from django import forms
from demande_auto.models import DemandeAuto, TypeDemandeAuto, Finalite, SousFinalite

from base_edcp.models import Enregistrement

FORM_STRUCTURE = [
  {'label': 'page1',
   'display_name': 'Page 1',
   'fields': ['type_demande', 'organisation']
  },
  {'label': 'page2',
   'display_name': 'Page 2',
   'fields': ['finalite', 'sous_finalite']
  },
]

class CreateDemandeForm(forms.Form):
  """
  Formulaire permettant de créeer une nouvelle demande d'autorisation
  """
  
  organisation = forms.ModelChoiceField(
    label='2. Organisation concernée', 
    queryset=Enregistrement.objects.all(),
    help_text='Choisissez l\'organisation pour laquelle vous souhaitez effectuer la demande d\'autorisation.',
  )
  type_demande = forms.ModelChoiceField(
    label='Type de demande', 
    queryset=TypeDemandeAuto.objects.all(),
    # widget=forms.RadioSelect,
  )
    

  """ finalite = forms.ModelChoiceField(
    label='Finalité', 
    queryset=Finalite.objects.all(),
  )
  sous_finalite = forms.ModelMultipleChoiceField(
    label='Sous-finalités',
    queryset=SousFinalite.objects.all(),
    widget=forms.CheckboxSelectMultiple
  ) """

  # template_name = 'forms/multisteps_form.html'

  def __init__(self, request=None, *args, **kwargs):
    # request_kwargs = kwargs.pop('request')
    super().__init__(*args, **kwargs)
    # print('user : ', request.user)
    if request:
      self.fields['organisation'].queryset = Enregistrement.objects.filter(user=request.user)