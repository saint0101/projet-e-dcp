from django import forms
# from .models import Correspondant
# from connexion.forms import UserRegistrationForm
# from base_edcp.models import User, Enregistrement
from base_edcp import validators


class UserIsDPOForm(forms.Form):
  """
  Formulaire permettant à l'utilisateur de choisir s'il est lui-même le DPO (auto-désignation)
  ou de créer un autre compte pour le DPO
  """
  user_is_dpo = forms.ChoiceField(
    label='Êtes-vous le correspondant ?', 
    widget=forms.RadioSelect, 
    choices=(
      (True, 'Oui, je suis le Correspondant désigné'), 
      (False, 'Non, je crée un compte pour le Correspondant'),
    ), 
    initial=True, 
    required=False,
    help_text='''Si vous chosissez "Oui", votre compte utilisateur sera associé à l\'organisation en tant que Correspondant. <br>
      Si vous chosissez plutôt "Non", vous créerez un compte utilisateur pour le Correspondant à l'étape suivante. 
      Il devra activer son compte en cliquant sur le lien reçu par email.''',
  )


class DPOFormPage1(forms.Form):
  """
  Première page du formulaire de désignation de DPO.
  Représente l'étape de création du compte utilisateur du DPO.
  L'étape suivante est gérée avec un UpdateView.
  """
  # user = User()
  # organisation = forms.ModelChoiceField(label='Organisation', queryset=Enregistrement.objects.none())
  # user_is_dpo = forms.ChoiceField(label='Êtes-vous le correspondant ?', widget=forms.RadioSelect, choices=((True, 'Oui, je suis le Correspondant désigné'), (False, 'Non, je crée un compte pour le Correspondant')), initial=False)
  
  email = forms.EmailField(label='Email', validators=[validators.validate_unique_email])
  nom = forms.CharField(label='Nom', max_length=100, strip=True)
  prenoms = forms.CharField(label='Prénoms', max_length=100, strip=True)
  telephone = forms.CharField(label='Téléphone', max_length=100, strip=True)
  fonction = forms.CharField(label='Fonction', required=False)



  """TO DELETE"""
  """ def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user', None)
    super(DPOFormPage1, self).__init__(*args, **kwargs)
    if self.user:
      # Filter the tags queryset based on the current user
      self.fields['organisation'].queryset = Enregistrement.objects.filter(user=self.user).filter(has_dpo=False) """


""" class DPOFormPage2(forms.Form):
  qualifications = forms. CharField(label='Qualifications')
  moyens_materiels = forms. CharField(label='Moyens materiels')
  moyens_humains = forms. CharField(label='Moyens humains')
  experiences = forms. CharField(label='Experiences') """



""" class DPOForm(forms.ModelForm):
  class Meta:
    model = Correspondant
    fields = [
      'user',
      'organisation',
      'type_dpo',
      'qualifications',
      'exercice_activite', 
      'moyens_materiels',
      'moyens_humains',
      'experiences',
    ] """


""" class UserDPOForm(UserRegistrationForm):
  fields = (
    'email',
    'nom',
    'prenoms',
    'telephone',
    'organisation',
    'fonction',
    )
  """ 

""" class CreateUserDPOForm(forms.Form):
  email = forms.EmailField(label='Email')
  nom = forms.CharField(label='Nom')
  prenoms = forms.CharField(label='Prénom')
  telephone = forms.CharField(label='Téléphone')
  # organisation = forms.CharField(label='Organisation')
  fonction = forms.CharField(label='Fonction', required=False)
  # is_first_step = forms.CharField(max_length=5)  # Assuming this is a hidden field

  def save(self, commit=True):
    user = User()
    user.set_password(self.cleaned_data["password"])
    user.is_dpo = True
    user.email_verified = False  # Définir la valeur par défaut lors de l'inscription
    if commit:
        user.save()
    return user"""