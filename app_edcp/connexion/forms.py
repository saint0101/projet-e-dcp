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
    
    # ajoute de point de verification du formulaires
    def check_size_pitcher(self):
        """ 
        Vérification de la taille de l'image d'avatar
        """
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Si l'image dépasse 1 Mo, lever une erreur
            if avatar.size > 1 * 1024 * 1024:  # 1 Mo
                raise forms.ValidationError({
                    'avatar': "L'image d'avatar dépasse la taille maximale autorisée de 1 Mo."
                })
        return avatar.size
          

    def check_id_user(self):
        """
        Vérifie si un utilisateur avec cet ID existe déjà
        """
        cleaned_data = super().clean()
        # Extraire l'ID de l'utilisateur s'il est défini (lorsque vous modifiez un utilisateur existant)
        user_id = self.instance.id
        if user_id:
            # Vérifier si un utilisateur avec le même ID existe
            existing_user = User.objects.filter(id=user_id).exists()
            print("existing_user", existing_user)
            if existing_user:
                raise forms.ValidationError("Un utilisateur avec cet ID existe déjà.")
        
        return cleaned_data

    def check_email_user(self):
        """
        Vérification pour éviter les doublons (email, etc.)
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        # Vérifier si un autre utilisateur avec le même email existe
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError({
            'email': "Un utilisateur avec cet email existe déjà."
        })

        return cleaned_data

    def save(self, commit=True):
        """
        Sauvegarde les données après validation
        """
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email_verified = False  # Définit l'état non vérifié de l'email lors de l'inscription

        # Vérification supplémentaire si nécessaire, par exemple avant d'enregistrer l'utilisateur.
        if commit:
            user.save()
        return user

  """
    apparence des champs du formulaire. Ne fonctionne pas tant que crispy_forms est utilisé
    widgets = {
    'consentement': forms.RadioSelect}
    
  def save(self, commit=True):
    user = super(UserRegistrationForm, self).save(commit=False)
    print(f'User : {user.email}')
    user.email_verified = False  # Définir la valeur par défaut lors de l'inscription
    if commit:
      user.save()
    return user
  """
  

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
