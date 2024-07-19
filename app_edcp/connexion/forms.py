from django.contrib.auth.forms import UserCreationForm
from base_edcp.models import User


class UserRegistrationForm(UserCreationForm):
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