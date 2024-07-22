from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

from base_edcp.models import User


class UserForm(UserCreationForm):
    # Personnalisation du champ password1
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        # modifier les texte de django pourle mettre en français
        #help_text=(
        #    "Votre mot de passe ne peut pas être trop similaire à vos autres informations personnelles.\n"
        #    "Votre mot de passe doit contenir au moins 8 caractères.\n"
        #    "Votre mot de passe ne peut pas être un mot de passe couramment utilisé.\n"
        #    "Votre mot de passe ne peut pas être entièrement numérique."
        # ),
        label='Mot de Passe',
    )

    # Personnalisation du champ password2
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        # help_text="\nEntrez le même mot de passe qu'auparavant, pour vérification.",
        label="Confirmer le Mot de Passe"
    )

    class Meta:
        model = User
        # les champs du formulaire user
        fields = [
            'login', 'avatar', 'nom', 'prenoms', 'organisation', 'telephone',
            'fonction', 'consentement', 'email', 'is_active', 'is_staff', 'email_verified',
            'password1', 'password2'
        ]
        widgets = {
            # Masquer le texte des mots de passe
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }
        labels = {
            'login': 'Nom d\'Utilisateur',
            'avatar': 'Avatar',
            'nom': 'Nom',
            'prenoms': 'Prénoms',
            'organisation': 'Organisation',
            'telephone': 'Téléphone',
            'fonction': 'Fonction',
            'consentement': 'Consentement',
            'email': 'Email',
            'is_active': 'Est Actif',
            'is_staff': 'Est Membre du Personnel',
            'email_verified': 'Email Vérifié',
            'password1': 'Mot de Passe',
            'password2': 'Confirmer le Mot de Passe',
        }

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        email = self.cleaned_data.get('email')

        password2 = self.cleaned_data.get('password2')

        # Vérifier si le mot de passe contient les informations de l'adresse e-mail
        if email and password and email in password:
            raise ValidationError("Le mot de passe est trop similaire à l'adresse e-mail.")

        # Validations du mot de passe
        if password:
            if len(password) < 8:
                raise ValidationError("Votre mot de passe doit contenir au moins 8 caractères.")
            if re.match(r'^[0-9]*$', password):
                raise ValidationError("Votre mot de passe ne peut pas être entièrement numérique.")
            common_passwords = ['password', '123456', '123456789', 'qwerty', 'abc123']
            if password.lower() in common_passwords:
                raise ValidationError("Votre mot de passe ne peut pas être un mot de passe couramment utilisé.")

        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Vérifier si les deux mots de passe correspondent
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe sont differents.")

        return password2