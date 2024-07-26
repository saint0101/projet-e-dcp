from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField

from base_edcp.models import User


class UserRegistrationForm(UserCreationForm):
  """
  Formulaires d'inscription.
  Hérite de la classe Django UserCreationForm.
  Spécifie les champs utilisés dans le formulaire.
  """

  class Meta:
    model = User
    fields = (
      'email',
      'nom',
      'prenoms',
      'telephone',
      'organisation',
      'fonction',
      'avatar',
      )
  
  def __init__(self, *args, **kwargs):
    super(UserRegistrationForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper(self)
    self.helper.layout = Layout(
      
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
      # Submit('submit', 'Submit', css_class='button white'),
    )

    def save(self, commit=True):
      user = super(UserRegistrationForm, self).save(commit=False)
      user.email_verified = False  # Définir la valeur par défaut lors de l'inscription
      if commit:
        user.save()
      return user