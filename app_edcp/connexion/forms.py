from django.contrib.auth.forms import UserCreationForm
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