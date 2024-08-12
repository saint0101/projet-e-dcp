from cProfile import label
from django import forms
from demande_auto.models import PersConcernee, DemandeAuto, DemandeAutoBiometrie, DemandeAutoTraitement, DemandeAutoTransfert, DemandeAutoVideo, TypeDemandeAuto, Finalite, SousFinalite

from base_edcp.models import Enregistrement



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

  def __init__(self, *args, **kwargs):
    # request_kwargs = kwargs.pop('request')
    super().__init__(*args, **kwargs)
    # print('user : ', request.user)
    """ if user:
      self.fields['organisation'].queryset = Enregistrement.objects.filter(user=user)
      pass """
    


class UpdateDemandeTraitementForm(forms.ModelForm):
  # type_demande_auto = TypeDemandeAuto.objects.get(label='traitement')
  label_type = 'traitement'
  finalite = forms.ModelChoiceField(
    label='Finalité du traitement', 
    queryset=Finalite.objects.all(),
  )
  sous_finalites = forms.ModelChoiceField(
    label='Sous-finalités', 
    queryset=SousFinalite.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  personnes_concernees = forms.ModelChoiceField(
    label='Personnes concernées', 
    queryset=PersConcernee.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  
  class Meta:
    model = DemandeAutoTraitement
    fields = '__all__'
    # widgets={'personnes_concernees': forms.CheckboxSelectMultiple},

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    list_finalites = TypeDemandeAuto.objects.get(label=self.label_type).finalites.all()
    self.fields['finalite'].queryset = list_finalites
    self.fields['sous_finalites'].queryset = SousFinalite.objects.filter(finalite__in=list_finalites)


class UpdateDemandeTransfertForm(forms.ModelForm):
  label_type = 'transfert'
  finalite = forms.ModelChoiceField(
    label='Finalité du traitement', 
    queryset=Finalite.objects.all(),
  )
  sous_finalites = forms.ModelChoiceField(
    label='Sous-finalités', 
    queryset=SousFinalite.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  personnes_concernees = forms.ModelChoiceField(
    label='Personnes concernées', 
    queryset=PersConcernee.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  
  class Meta:
    model = DemandeAutoTransfert
    fields = '__all__'
    # widgets={'personnes_concernees': forms.CheckboxSelectMultiple},
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    list_finalites = TypeDemandeAuto.objects.get(label=self.label_type).finalites.all()
    self.fields['finalite'].queryset = list_finalites
    self.fields['sous_finalites'].queryset = SousFinalite.objects.filter(finalite__in=list_finalites)


class UpdateDemandeVideoForm(forms.ModelForm):
  label_type = 'videosurveillance'
  finalite = forms.ModelChoiceField(
    label='Finalité du traitement', 
    queryset=Finalite.objects.all(),
  )
  sous_finalites = forms.ModelChoiceField(
    label='Sous-finalités', 
    queryset=SousFinalite.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  personnes_concernees = forms.ModelChoiceField(
    label='Personnes concernées', 
    queryset=PersConcernee.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )

  class Meta:
    model = DemandeAutoVideo
    fields = '__all__'
    # widgets={'personnes_concernees': forms.CheckboxSelectMultiple},

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    list_finalites = TypeDemandeAuto.objects.get(label=self.label_type).finalites.all()
    self.fields['finalite'].queryset = list_finalites
    self.fields['sous_finalites'].queryset = SousFinalite.objects.filter(finalite__in=list_finalites)


class UpdateDemandeBioForm(forms.ModelForm):
  label_type = 'biometrie'
  finalite = forms.ModelChoiceField(
    label='Finalité du traitement', 
    queryset=Finalite.objects.all(),
  )
  sous_finalites = forms.ModelChoiceField(
    label='Sous-finalités', 
    queryset=SousFinalite.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  personnes_concernees = forms.ModelChoiceField(
    label='Personnes concernées', 
    queryset=PersConcernee.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )

  class Meta:
    model = DemandeAutoBiometrie
    fields = '__all__'
    # widgets={'personnes_concernees': forms.CheckboxSelectMultiple},

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    list_finalites = TypeDemandeAuto.objects.get(label=self.label_type).finalites.all()
    self.fields['finalite'].queryset = list_finalites
    self.fields['sous_finalites'].queryset = SousFinalite.objects.filter(finalite__in=list_finalites)

    # print('user : ', request.user)