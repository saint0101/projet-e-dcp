from django.test import TestCase
from django.urls import reverse

from notifications.models import Notification
from base_edcp.models import User


class NotificationTests(TestCase):
    def setUp(self):
        # Création d'un utilisateur test
        self.user = User.objects.create_user(
            email='fouriersaint@gmail.com',
            password='Qsaint2024&',
            nom="N'GUESSAN",
            prenoms='Konan Saint-fourier onesyme',
            username='saint'
        )
        
        # Connexion de l'utilisateur pour le test
        self.client.login(email='fouriersaint@gmail.com', password='Qsaint2024&')
    
        # Création d'une notification de test
        self.notification = Notification.objects.create(
            user=self.user,
            message="Message de test"
        )

    def test_notification_liste(self):
        """ Test de la liste des notifications """
        # Obtenir l'URL de la vue
        url = reverse('notification_list')
        # Faire la requête GET avec un utilisateur authentifié
        response = self.client.get(url)
        # Vérifier que la requête a réussi avec un code 200
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Message de test") 
    
    def test_marquer_comme_lue(self):
        """ Test de la fonctionnalité de marquage d'une notification comme lue """
        url = reverse('mark_as_read', args=[self.notification.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirection après marquage
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

#TODO: cotinuer les tests