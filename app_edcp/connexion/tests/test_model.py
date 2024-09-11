from django.test import TestCase
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile

from connexion.forms import UserRegistrationForm
from base_edcp.models import User 

class UserRegistrationFormTest(TestCase):

    def setUp(self):
        # Créer un utilisateur existant avec un certain email
        self.existing_user = User.objects.create_user(
            email='fouriersaint@gmail.com',
            username='saint',
            password='Qsaint2024&'
        )
    """
        def create_test_image(self, size_in_mb=2):
            
            Crée une image de taille spécifiée en mémoire.
            :param size_in_mb: Taille de l'image en Mo.
            :return: Un fichier image en mémoire.
            
            img = Image.new('RGB', (1000, 1000), color=(255, 0, 0))  # Créer une image rouge 3000x3000 pixels
            byte_array = io.BytesIO()
                
            # Sauvegarder l'image dans un buffer jusqu'à ce qu'elle atteigne la taille voulue
            img.save(byte_array, format='JPEG')
            while byte_array.tell() < size_in_mb * 1024 * 1024:
                img.save(byte_array, format='JPEG')
            byte_array.seek(0)
                
            return byte_array


        def test_avatar_too_large(self):
            # Créer une image valide de plus de 2 Mo
            large_avatar = SimpleUploadedFile(
                'large_avatar.jpg',
                self.create_test_image(2).getvalue(),
                content_type='image/jpeg'
            )
            form_data = {
                'email': 'nouvel_utilisateur@example.com',
                'nom': 'Nouveau',
                'prenoms': 'Utilisateur',
                'telephone': '123456789',
                'password1': 'motdepasse123',
                'password2': 'motdepasse123',
                'consentement': True,
            }
            form_files = {'avatar': large_avatar}
            form = UserRegistrationForm(data=form_data, files=form_files)
            
            # Le formulaire doit être invalide à cause de l'image trop grande
            self.assertFalse(form.is_valid())
            self.assertIn('avatar', form.errors)
            self.assertEqual(form.errors['avatar'], ["L'image d'avatar dépasse la taille maximale autorisée de 1 Mo."])
    """

    def test_duplicate_email(self):
        """ Test de la duplication de l'email """
        form_data = {
            'email': 'fouriersaint@gmail.com',  # Email en double
            'nom': "N'GUESSAN",
            'prenoms': 'Konan Saint-fourier onesyme',
            'telephone': '12345678',
            'password1': 'Qsaint2024&',
            'password2': 'Qsaint2024&',
            'consentement': True
        }

        form = UserRegistrationForm(data=form_data)
        # Le formulaire doit être invalide à cause de l'email en double
        self.assertFalse(form.is_valid())
        
        # Vérifier que l'erreur est associée au champ 'email'
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ["Un objet Utilisateur avec ce champ Email existe déjà."])