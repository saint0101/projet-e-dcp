from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField

from base_edcp.models import User
from base_edcp import validators


class UserRegistrationForm(UserCreationForm):
  """
  Formulaires d'inscription.
  Hérite de la classe Django UserCreationForm.
  Spécifie les champs utilisés dans le formulaire.
  """
  # email = forms.EmailField(validators=[validate_unique_email])
  nom = forms.CharField(min_length=2, max_length=100, validators=[validators.validate_charfield, validators.validate_no_special_chars])
  prenoms = forms.CharField(min_length=2, max_length=100, validators=[validators.validate_charfield, validators.validate_no_special_chars])
  telephone = forms.CharField(required=True, min_length=2, max_length=100)
  organisation = forms.CharField(required=False, min_length=2, max_length=100, validators=[validators.validate_charfield, validators.validate_no_special_chars])
  fonction = forms.CharField(required=False, min_length=2, max_length=100, validators=[validators.validate_charfield, validators.validate_no_special_chars])
  avatar = forms.ImageField(required=False, validators=[validators.validate_image_size], help_text='Photo de profil (facultative). Taille limite : 1Mb')
  """ consentement = forms.BooleanField(
    validators=[validators.validate_required_boolfield],
    label='Je donne mon consentement pour le traitement de mes données personnelles',
    help_text='''Veuillez cocher cette case pour donner votre consentement : 
        les données soumises via ce formulaire seront utilisées pour la création 
        et pour l'accomplissement de vos formalités sur la plateforme e-DCP. 
        Vos données ne seront traitées que par les agents habilités de l'Autorité de Protection.
        Vous pouvez à tout moment exercer vos droits exercer à l'adresse ..... ''') """

  class Meta:
    model = User
    # form_template_name = 'forms/form_floating_label.html'
    fields = (
      'email',
      'nom',
      'prenoms',
      'telephone',
      'organisation',
      'fonction',
      'avatar',
      'password1',
      'password2',
      'consentement',
      )
    
    # apparence des champs du formulaire. Ne fonctionne pas tant que crispy_forms est utilisé
    widgets = {
      # 'consentement': forms.RadioSelect 
    }
  def save(self, commit=True):
    user = super(UserRegistrationForm, self).save(commit=False)
    print(f'User : {user.email}')
    user.email_verified = False  # Définir la valeur par défaut lors de l'inscription
    if commit:
      user.save()
    return user
  

  # Mise en forme du formulaire avec Formtools
  """ def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
      # Application du style label flottant de Bootstrap
      FloatingField(
        'email',
        'nom',
        'prenoms',
        'telephone',
        'organisation',
        'fonction',
        'avatar',
        'password1',
        'password2',
      ),
      # Possibilité de définir le bouton d'envoi
      Submit('submit', 'S\'inscrire', css_class='btn btn-primary px-5'),
    ) """
