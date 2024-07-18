"""
    Test du models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """ Classe de test des modeles de la base de donnees """

    def test_create_user_with_infos_successful(self):
        """ Test de creation d'iuntilisateur avec succes """

        # champs de la base de donnees
        login = 'john_doe'
        avatar = 'avatar.jpg'
        nom = 'Doe'
        prenoms = 'John'
        organisation = 'XYZ Corp'
        telephone = '+1234567890'
        fonction = 'Manager'
        consentement = 'Yes'
        email = 'test@example.com'
        password = 'mptestuser123'

        # creation d'un objet utilisateur
        user = get_user_model().objects.create_user(
            login=login,
            avatar=avatar,
            nom=nom,
            prenoms=prenoms,
            organisation=organisation,
            telephone=telephone,
            email=email,
            fonction=fonction,
            consentement=consentement,
            password=password,
        )

        # les tests possibles
        self.assertEqual(user.login, login)
        self.assertTrue(user.check_password(password))

