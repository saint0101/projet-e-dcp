from django.test import TestCase
from app_edcp.connexion.forms import UserRegistrationForm
from base_edcp.models import User 
from django.core.files.uploadedfile import SimpleUploadedFile

class UserRegistrationFormTest(TestCase):

    def setUp(self):
        # Crée un utilisateur existant avec un email
        self.existing_user = User.objects.create_user(
            email='test@example.com',
            nom='Existant',
            prenoms='Utilisateur',
            password='securepassword123'
        )

    def test_avatar_too_large(self):
        # Simule l'upload d'une image trop grande (2 Mo)
        large_avatar = SimpleUploadedFile('large_avatar.jpg', b'a' * (2 * 1024 * 1024), content_type='image/jpeg')

        form_data = {
            'email': 'new_user@example.com',
            'nom': 'Nouveau',
            'prenoms': 'Utilisateur',
            'telephone': '123456789',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'consentement': True,
        }
        form_files = {'avatar': large_avatar}
        form = UserRegistrationForm(data=form_data, files=form_files)
        
        # Le formulaire doit être invalide à cause de l'image trop grande
        self.assertFalse(form.is_valid())
        self.assertIn('avatar', form.errors)
        self.assertEqual(form.errors['avatar'], ["L'image d'avatar dépasse la taille maximale autorisée de 1 Mo."])

    def test_duplicate_user_id(self):
        # Simule un formulaire avec un utilisateur existant (vérification de l'ID)
        form_data = {
            'email': 'another_user@example.com',
            'nom': 'Nouveau',
            'prenoms': 'Utilisateur',
            'telephone': '987654321',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'consentement': True,
        }
        form = UserRegistrationForm(instance=self.existing_user, data=form_data)
        
        # Le formulaire doit être invalide à cause de l'ID en double
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)  # L'erreur est attachée à l'ensemble du formulaire
        self.assertEqual(form.errors['__all__'], ["Un utilisateur avec cet ID existe déjà."])