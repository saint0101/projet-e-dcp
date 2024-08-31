from django import forms
# Commentaire, PersConcernee, DemandeAuto, DemandeAutoBiometrie, DemandeAutoTraitement, DemandeAutoTransfert, DemandeAutoVideo, TypeDemandeAuto, Finalite, SousFinalite
from base_edcp.models import Enregistrement
from demande.models import Status, Commentaire, AnalyseDemande
from demande_auto.forms_structures import FORM_STRUCTURE_BIOMETRIE, FORM_STRUCTURE_TRANSFERT, FORM_STRUCTURE_TRAITEMENT, FORM_STRUCTURE_VIDEO, get_form_fields
from demande_auto.models import TypeDemandeAuto, Finalite, SousFinalite, PersConcernee, DemandeAuto, DemandeAutoTraitement, DemandeAutoBiometrie, DemandeAutoTransfert, DemandeAutoVideo


class ChangeStatusForm(forms.Form):
  """ Formulaire de changement de statut de la demande """
  # CHOICES = []
  # status = forms.ModelChoiceField(queryset=Status.objects.all())
  pass


class AnalyseDemandeForm(forms.ModelForm):
  """ Formulaire d'analyse d'une demande d'autorisation """
  # NOTATION_CHOICES = [('', '---------'),] + [(notation.id, notation.description) for notation in EchelleNotation.objects.all()]
  NOTATION_CHOICES = []
  critere_completude = forms.IntegerField(
    label='1. Completude du dossier',
    required=False,
    widget=forms.Select(choices=NOTATION_CHOICES),
  )
  critere_docsvalides = forms.IntegerField(
    label='2. Validité des documents',
    required=False,
    widget=forms.Select(choices=NOTATION_CHOICES),
  )
  critere_finalite = forms.IntegerField(
    label='3. Finalité',
    required=False,
    widget=forms.Select(choices=NOTATION_CHOICES),
  )
  critere_transparence = forms.IntegerField(
    label='4. Transparence',
    required=False,
    widget=forms.Select(choices=NOTATION_CHOICES),
  )

  class Meta:
    model = AnalyseDemande
    fields = ['critere_completude', 'critere_docsvalides', 'critere_finalite', 'critere_transparence', 'observations','prescriptions', 'avis_juridique', 'avis_technique']

    """ def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      list_notations = EchelleNotation.objects.all()
      self.fields['critere_completude'].widget = forms.forms.Select(choices=[(notation.id, notation.description) for notation in list_notations])
    """


class CreateDemandeForm(forms.Form):
  """ Formulaire permettant de créeer une nouvelle demande d'autorisation """
  
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
    

class UpdateDemandeForm(forms.ModelForm):
  """ Formulaire de mise à jour d'une demande d'autorisation """
  finalite = forms.ModelChoiceField(
    label='Finalité du traitement', 
    queryset=Finalite.objects.all(),
  )
  sous_finalites = forms.ModelMultipleChoiceField(
    label='Sous-finalités', 
    queryset=SousFinalite.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  personnes_concernees = forms.ModelMultipleChoiceField(
    label='Personnes concernées', 
    queryset=PersConcernee.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )

  class Meta:
    model = DemandeAuto
    fields = '__all__'
    # widgets={'personnes_concernees': forms.CheckboxSelectMultiple},

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    """ list_finalites = TypeDemandeAuto.objects.get(label=self.label_type).finalites.all()
    self.fields['finalite'].queryset = list_finalites
    self.fields['sous_finalites'].queryset = SousFinalite.objects.filter(finalite__in=list_finalites) """


class UpdateDemandeTraitementForm(forms.ModelForm):
  """ Formulaire de mise à jour d'une demande d'autorisation de traitement """
  # type_demande_auto = TypeDemandeAuto.objects.get(label='traitement')
  label_type = 'traitement'
  finalite = forms.ModelChoiceField(
    label='Finalité du traitement', 
    queryset=Finalite.objects.all(),
  )
  sous_finalites = forms.ModelMultipleChoiceField(
    label='Sous-finalités', 
    queryset=SousFinalite.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    help_text='Veuillez sélectionner une finalité pour afficher les sous-finalités correspondantes.'
  )
  personnes_concernees = forms.ModelMultipleChoiceField(
    label='Personnes concernées', 
    queryset=PersConcernee.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  
  class Meta:
    model = DemandeAutoTraitement
    fields = get_form_fields(FORM_STRUCTURE_TRAITEMENT)
    # exclude = ['created_by', 'organisation', 'type_demande', 'created_at', 'status']
    # widgets={'personnes_concernees': forms.CheckboxSelectMultiple},

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    list_finalites = TypeDemandeAuto.objects.get(label=self.label_type).finalites.all()
    self.fields['finalite'].queryset = list_finalites
    self.fields['sous_finalites'].queryset = SousFinalite.objects.filter(finalite__in=list_finalites)


class TraitementFormDisabled(UpdateDemandeTraitementForm):
  """ Formulaire d'affichage' d'une demande d'autorisation de traitement """
  class Meta:
    model = DemandeAutoTraitement
    fields = get_form_fields(FORM_STRUCTURE_TRAITEMENT, hide_files=True)


class UpdateDemandeTransfertForm(forms.ModelForm):
  """ Formulaire de mise à jour d'une demande d'autorisation de transfert """
  label_type = 'transfert'
  finalite = forms.ModelChoiceField(
    label='Finalité du traitement', 
    queryset=Finalite.objects.all(),
  )
  sous_finalites = forms.ModelMultipleChoiceField(
    label='Sous-finalités', 
    queryset=SousFinalite.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    help_text='Veuillez sélectionner une finalité pour afficher les sous-finalités correspondantes.'
  )
  personnes_concernees = forms.ModelMultipleChoiceField(
    label='Personnes concernées', 
    queryset=PersConcernee.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  
  class Meta:
    model = DemandeAutoTransfert
    # fields = '__all__'
    fields = get_form_fields(FORM_STRUCTURE_TRANSFERT)
    # exclude = ['created_by', 'organisation', 'type_demande', 'created_at', 'status']
    # widgets={'personnes_concernees': forms.CheckboxSelectMultiple},
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    list_finalites = TypeDemandeAuto.objects.get(label=self.label_type).finalites.all()
    self.fields['finalite'].queryset = list_finalites
    self.fields['sous_finalites'].queryset = SousFinalite.objects.filter(finalite__in=list_finalites)


class TransfertFormDisabled(UpdateDemandeTransfertForm):
  """ Formulaire d'affichage' d'une demande d'autorisation de transfert """
  class Meta:
    model = DemandeAutoTransfert
    fields = get_form_fields(FORM_STRUCTURE_TRANSFERT, hide_files=True)


class UpdateDemandeVideoForm(forms.ModelForm):
  """ Formulaire de mise à jour d'une demande d'autorisation de vidéosurveillance """
  label_type = 'videosurveillance'
  finalite = forms.ModelChoiceField(
    label='Finalité du traitement', 
    queryset=Finalite.objects.all(),
  )
  sous_finalites = forms.ModelMultipleChoiceField(
    label='Sous-finalités', 
    queryset=SousFinalite.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  personnes_concernees = forms.ModelMultipleChoiceField(
    label='Personnes concernées', 
    queryset=PersConcernee.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )

  class Meta:
    model = DemandeAutoVideo
    # fields = '__all__'
    fields = get_form_fields(FORM_STRUCTURE_VIDEO)
    # exclude = ['created_by', 'organisation', 'type_demande', 'created_at', 'status']
    # widgets={'personnes_concernees': forms.CheckboxSelectMultiple},

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    list_finalites = TypeDemandeAuto.objects.get(label=self.label_type).finalites.all()
    self.fields['finalite'].queryset = list_finalites
    self.fields['sous_finalites'].queryset = SousFinalite.objects.filter(finalite__in=list_finalites)


class VideoFormDisabled(UpdateDemandeVideoForm):
  """ Formulaire d'affichage' d'une demande d'autorisation de vidéosurveillance """
  class Meta:
    model = DemandeAutoVideo
    fields = get_form_fields(FORM_STRUCTURE_VIDEO, hide_files=True)


class UpdateDemandeBioForm(forms.ModelForm):
  """ Formulaire de mise à jour d'une demande d'autorisation de biométrie """
  label_type = 'biometrie'
  finalite = forms.ModelChoiceField(
    label='Finalité du traitement', 
    queryset=Finalite.objects.all(),
  )
  sous_finalites = forms.ModelMultipleChoiceField(
    label='Sous-finalités', 
    queryset=SousFinalite.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )
  personnes_concernees = forms.ModelMultipleChoiceField(
    label='Personnes concernées', 
    queryset=PersConcernee.objects.all(),
    widget=forms.CheckboxSelectMultiple,
  )

  class Meta:
    model = DemandeAutoBiometrie
    # fields = '__all__'
    fields = get_form_fields(FORM_STRUCTURE_BIOMETRIE)
    # exclude = ['created_by', 'organisation', 'type_demande', 'created_at', 'status']
    # widgets={'personnes_concernees': forms.CheckboxSelectMultiple},

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    list_finalites = TypeDemandeAuto.objects.get(label=self.label_type).finalites.all()
    self.fields['finalite'].queryset = list_finalites
    self.fields['sous_finalites'].queryset = SousFinalite.objects.filter(finalite__in=list_finalites)

    # print('user : ', request.user)



class BiometrieFormDisabled(UpdateDemandeBioForm):
  """ Formulaire d'affichage' d'une demande d'autorisation de biométrie """
  class Meta:
    model = DemandeAutoBiometrie
    fields = get_form_fields(FORM_STRUCTURE_BIOMETRIE, hide_files=True)

