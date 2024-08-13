"""
    Test des tables du models.
"""
from django.core.exceptions import ValidationError

from cProfile import label
from pydoc import describe
from re import T
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import set_script_prefix

from base_edcp.models import Enregistrement, User, TypeClient, Secteur, Pays, TypePiece


class UserModelTest(TestCase):

    """ Classe de test des modeles de la base de donnees """

    def test_create_user_with_infos_successful(self):
        """ Test de creation d'iuntilisateur avec succes """

        # champs de la base de donnees
        email = 'test@example.com'
        password = 'mptestuser123'
        user_data = {
            'username': 'john',
            'avatar': 'avatar.jpg',
            'nom': 'Doe',
            'prenoms': 'John',
            'organisation': 'XYZ Corp',
            'telephone': '+1234567890',
            'fonction': 'Manager',
            'consentement': True,
        }

        # creation d'un objet utilisateur
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            **user_data
        )

        # les tests possibles
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.nom, user_data['nom'])
        self.assertEqual(user.prenoms, user_data['prenoms'])
        self.assertEqual(user.organisation, user_data['organisation'])
        self.assertEqual(user.telephone, user_data['telephone'])
        self.assertEqual(user.fonction, user_data['fonction'])
        self.assertEqual(user.consentement, user_data['consentement'])

    def test_new_user_email_normalized(self):
        """ Test de normalisation de l'email d'un nouvel utilisateur """

        # champs de la base de donnée
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            # creation d'un nouvel utilisateur
            user = get_user_model().objects.create_user(email, 'test123')

            # les tests possibles de l'email normalisé
            self.assertEqual(user.email, expected)

    def test_new_without_email_raises_error(self):
        """ Test de creation d'un nouvel utilisateur sans email """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """ Test de creation d'un superutilisateur """
         # creation d'un objet utilisateur
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123'
        )
        # les tests possibles de Vérification des droits d'administrateur
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class TypeClientModelTest(TestCase):
    """ Classe de test des modeles de la table type client dans la base de donnees """

    # les case possible
    def test_create_type_client_successful(self):
        """ Test de creation d'un type de client avec succes """

        # Donnees de test
        label = 'Entreprise'
        description = 'Client d\'une entreprise'
        sensible = True
        ordre = 1

        # creation de l'objet type de client
        type_client = TypeClient.objects.create(
            label=label,
            description=description,
            sensible=sensible,
            ordre=ordre
        )

        # les tests possibles
        self.assertEqual(type_client.label, label)
        self.assertEqual(type_client.description, description)
        self.assertEqual(type_client.sensible, sensible)
        self.assertEqual(type_client.ordre, ordre)


    def test_str_representation(self):
        """ Test de la representation de l'objet type de client """
        # valeur de test
        label = 'Particulie'

        # Création d'une instance de TypeClient
        type_client = TypeClient.objects.create(
            label=label
        )

        # Vérification de la méthode __str__
        self.assertEqual(str(type_client), label)

    def test_create_type_client_default_values(self):
        """Test de création d'un TypeClient avec les valeurs par défaut."""

        # Données de test avec uniquement le label
        label = 'Gouvernement'

        # Création d'une instance de TypeClient avec seulement le label
        type_client = TypeClient.objects.create(label=label)

        # Vérifications des valeurs par défaut
        self.assertEqual(type_client.label, label)
        self.assertIsNone(type_client.description, '')
        self.assertFalse(type_client.sensible)
        self.assertEqual(type_client.ordre, 0)


class TypePieceModelTest(TestCase):
    """ Classe de test des modeles de la table type de piece dans la base de donnée """

    # les case possible
    def test_create_type_piece_successful(self):
        """ Test de creation d'un type de piece avec succes """

        # Donnees de test
        label = 'CNI'
        description = 'Carte nationale d\'identité'
        sensible = True
        ordre = 1

        # creation de l'objet type de piece
        type_piece = TypePiece.objects.create(
            label=label,
            description=description,
            sensible=sensible,
            ordre=ordre
        )

        # les tests possibles pour la vrification des valeurs
        self.assertEqual(type_piece.label, label)
        self.assertEqual(type_piece.description, description)
        self.assertTrue(type_piece.sensible, sensible)
        self.assertEqual(type_piece.ordre, ordre)


    def test_str_representation(self):
        """Test de la représentation en chaîne de caractères (__str__) du TypePiece."""

        # Données de test
        label = "Carte d'identité"

        # Création d'une instance de TypePiece
        type_piece = TypePiece.objects.create(label=label)

        # Vérification de la méthode __str__
        self.assertEqual(str(type_piece), label)


    def test_create_type_piece_default_values(self):
        """Test de création d'un TypePiece avec les valeurs par défaut."""

        # Données de test avec uniquement le label
        label = 'Permis de conduire'

        # Création d'une instance de TypePiece avec seulement le label
        type_piece = TypePiece.objects.create(label=label)

        # Vérifications des valeurs par défaut
        self.assertEqual(type_piece.label, label)
        self.assertIsNone(type_piece.description)  # Vérifier que description est None par défaut
        self.assertFalse(type_piece.sensible)  # Vérifier que sensible est False par défaut
        self.assertEqual(type_piece.ordre, 0)  # Vérifier que ordre est 0 par défaut


class EnregistrementModelTest(TestCase):

    """Classe de test pour le modèle Enregistrement."""

    def setUp(self):
        """Configuration initiale avant chaque test."""
        # Création d'un utilisateur pour les tests
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password123',
            nom='Test',
            prenoms='User',
            username='testuser'
        )
        # Création d'un type de client pour les tests
        self.type_client = TypeClient.objects.create(
            label='Entreprise',
            description='Client entreprise'
        )
        # Création d'un secteur pour les tests
        self.secteur = Secteur.objects.create(
            label='Technologie',
            description='Secteur technologique',
            sensible = True,
            ordre = 1
        )
        # Création d'un pays pour les tests
        self.pays = Pays.objects.create(
            label='Côte d\'Ivoire',
            code='CI'
        )
        # Création d'un type de pièce pour les tests
        self.type_piece = TypePiece.objects.create(
            label='Carte Nationale d\'Identité',
            description='CNI'
        )

    def test_create_enregistrement_successful(self):
        """Test de création d'un enregistrement avec succès."""

        # Données de test
        enregistrement_data = {
            'user': self.user,
            'typeclient': self.type_client,
            'raisonsociale': 'Test Société',
            'idu': '12345',
            'representant': 'Jean Dupont',
            'rccm': 'CI-ABJ-2023-B-1234',
            'secteur': self.secteur,
            'telephone': '+2250700000000',
            'email_contact': 'contact@example.com',
            'site_web': 'https://www.example.com',
            'pays': self.pays,
            'ville': 'Abidjan',
            'adresse_geo': 'Rue des Palmiers',
            'adresse_bp': 'BP 1234 Abidjan',
            'gmaps_link': 'https://maps.google.com/?q=5.348,4.027',
            'effectif': 50,
            'presentation': 'Présentation de la société',
            'type_piece': self.type_piece,
            'num_piece': 'CI123456789',
            'has_dpo': True
        }

        # Création d'une instance d'Enregistrement
        enregistrement = Enregistrement.objects.create(**enregistrement_data)

        # Vérifications des attributs de l'enregistrement
        self.assertEqual(enregistrement.user, self.user)  # Vérifie que l'utilisateur associé est correct
        self.assertEqual(enregistrement.typeclient, self.type_client)  # Vérifie que le type de client associé est correct
        self.assertEqual(enregistrement.raisonsociale, enregistrement_data['raisonsociale'])  # Vérifie que la raison sociale est correcte
        self.assertEqual(enregistrement.idu, enregistrement_data['idu'])  # Vérifie que le numéro d'identifiant unique est correct
        self.assertEqual(enregistrement.representant, enregistrement_data['representant'])  # Vérifie que le nom du représentant est correct
        self.assertEqual(enregistrement.rccm, enregistrement_data['rccm'])  # Vérifie que le numéro RCCM est correct
        self.assertEqual(enregistrement.secteur, self.secteur)  # Vérifie que le secteur d'activité est correct
        self.assertEqual(enregistrement.telephone, enregistrement_data['telephone'])  # Vérifie que le numéro de téléphone est correct
        self.assertEqual(enregistrement.email_contact, enregistrement_data['email_contact'])  # Vérifie que l'email de contact est correct
        self.assertEqual(enregistrement.site_web, enregistrement_data['site_web'])  # Vérifie que le site web est correct
        self.assertEqual(enregistrement.pays, self.pays)  # Vérifie que le pays est correct
        self.assertEqual(enregistrement.ville, enregistrement_data['ville'])  # Vérifie que la ville est correcte
        self.assertEqual(enregistrement.adresse_geo, enregistrement_data['adresse_geo'])  # Vérifie que l'adresse géographique est correcte
        self.assertEqual(enregistrement.adresse_bp, enregistrement_data['adresse_bp'])  # Vérifie que la boîte postale est correcte
        self.assertEqual(enregistrement.gmaps_link, enregistrement_data['gmaps_link'])  # Vérifie que le lien Google Maps est correct
        self.assertEqual(enregistrement.effectif, enregistrement_data['effectif'])  # Vérifie que l'effectif est correct
        self.assertEqual(enregistrement.presentation, enregistrement_data['presentation'])  # Vérifie que la présentation est correcte
        self.assertEqual(enregistrement.type_piece, self.type_piece)  # Vérifie que le type de pièce d'identité est correct
        self.assertEqual(enregistrement.num_piece, enregistrement_data['num_piece'])  # Vérifie que le numéro de la pièce d'identité est correct
        self.assertTrue(enregistrement.has_dpo)  # Vérifie que l'indicateur de désignation d'un DPO est correct

    def test_str_representation(self):
        """Test de la représentation en chaîne de caractères (__str__) de l'Enregistrement."""

        # Création d'une instance d'Enregistrement
        enregistrement = Enregistrement.objects.create(
            user=self.user,
            typeclient=self.type_client,
            raisonsociale='Test Société'
        )

        # Vérification de la méthode __str__
        self.assertEqual(str(enregistrement), 'Test Société')  # Vérifie que la méthode __str__ renvoie bien la raison sociale

    def test_create_enregistrement_default_values(self):
        """Test de création d'un enregistrement avec les valeurs par défaut."""

        # Création d'une instance d'Enregistrement avec uniquement les champs obligatoires
        enregistrement = Enregistrement.objects.create(
            user=self.user,
            typeclient=self.type_client,
            raisonsociale='Test Société',
            email_contact='contact@example.com',
            ville='Abidjan'
        )

        # Vérifications des valeurs par défaut
        self.assertIsNone(enregistrement.idu)  # Vérifie que le champ IDU est None par défaut
        self.assertEqual(enregistrement.telephone, None)  # Vérifie que le champ téléphone est None par défaut
        self.assertIsNone(enregistrement.site_web, '')  # Vérifie que le champ site web est vide par défaut
        self.assertIsNone(enregistrement.rccm, '')  # Vérifie que le champ RCCM est vide par défaut
        self.assertIsNone(enregistrement.adresse_geo)  # Vérifie que le champ adresse géographique est None par défaut
        self.assertIsNone(enregistrement.adresse_bp, '')  # Vérifie que le champ boîte postale est vide par défaut
        self.assertIsNone(enregistrement.gmaps_link, '')  # Vérifie que le champ lien Google Maps est vide par défaut
        self.assertIsNone(enregistrement.effectif)  # Vérifie que le champ effectif est None par défaut
        self.assertIsNone(enregistrement.presentation, '')  # Vérifie que le champ présentation est vide par défaut
        self.assertIsNone(enregistrement.type_piece)  # Vérifie que le champ type de pièce est None par défaut
        self.assertIsNone(enregistrement.num_piece, '')  # Vérifie que le champ numéro de pièce est vide par défaut
        self.assertFalse(enregistrement.has_dpo)  # Vérifie que le champ has_dpo est False par défaut
        self.assertIsNone(enregistrement.file_piece.name)  # Vérifie que le champ file_piece n'a pas de nom de fichier (donc pas de fichier associé)
        self.assertIsNone(enregistrement.file_rccm.name)  # Vérifie que le champ file_rccm n'a pas de nom de fichier (donc pas de fichier associé)
        self.assertIsNone(enregistrement.file_mandat.name)  # Vérifie que le champ file_mandat n'a pas de nom de fichier (donc pas de fichier associé)


class PaysModelTest(TestCase):

    """Classe de test pour le modèle Pays."""

    def test_create_pays_successful(self):
        """Test de création d'un pays avec succès."""

        # Données de test
        label = 'Côte d\'Ivoire'
        code = 'CI'

        # Création d'une instance de Pays
        pays = Pays.objects.create(
            label=label,
            code=code
        )

        # Vérifications
        self.assertEqual(pays.label, label)  # Vérifie que le nom du pays est correct
        self.assertEqual(pays.code, code)  # Vérifie que le code du pays est correct

    def test_str_representation(self):
        """Test de la représentation en chaîne de caractères (__str__) du modèle Pays."""

        # Données de test
        label = 'France'
        code = 'FR'

        # Création d'une instance de Pays
        pays = Pays.objects.create(
            label=label,
            code=code
        )

        # Vérification de la méthode __str__
        self.assertEqual(str(pays), 'France (FR)')  # Vérifie que la méthode __str__ renvoie bien "France (FR)"

    def test_pays_validation_without_required_fields(self):
        """Test pour vérifier que la validation échoue si les champs obligatoires ne sont pas fournis."""

        # Tenter de créer un Pays sans le champ label
        pays = Pays(code='CI')
        with self.assertRaises(ValidationError):
            pays.full_clean()  # Doit lever une ValidationError car le champ label est manquant

        # Tenter de créer un Pays sans le champ code
        pays = Pays(label='Côte d\'Ivoire')
        with self.assertRaises(ValidationError):
            pays.full_clean()  # Doit lever une ValidationError car le champ code est manquant

        # Tenter de créer un Pays avec des champs vides
        pays = Pays(label='', code='')
        with self.assertRaises(ValidationError):
            pays.full_clean()  # Doit lever une ValidationError car les champs label et code sont vides



class SecteurModelTest(TestCase):
    """Classe de test pour le modèle Secteur."""

    def test_create_secteur_successful(self):
        """Test de création d'un secteur avec succès."""

        # Données de test
        label = 'Technologie'
        description = 'Secteur des technologies de l\'information'
        sensible = True
        ordre = 1

        # Création d'une instance de Secteur
        secteur = Secteur.objects.create(
            label=label,
            description=description,
            sensible=sensible,
            ordre=ordre
        )

        # Vérifications
        self.assertEqual(secteur.label, label)  # Vérifie que le nom du secteur est correct
        self.assertEqual(secteur.description, description)  # Vérifie que la description est correcte
        self.assertTrue(secteur.sensible)  # Vérifie que le secteur est marqué comme sensible
        self.assertEqual(secteur.ordre, ordre)  # Vérifie que l'ordre d'affichage est correct

    def test_str_representation(self):
        """Test de la représentation en chaîne de caractères (__str__) du modèle Secteur."""

        # Données de test
        label = 'Finance'

        # Création d'une instance de Secteur
        secteur = Secteur.objects.create(
            label=label,
            sensible=False,
            ordre=2
        )

        # Vérification de la méthode __str__
        self.assertEqual(str(secteur), label)  # Vérifie que la méthode __str__ renvoie bien "Finance"

    def test_create_secteur_default_description(self):
        """Test de création d'un secteur avec la description par défaut (null)."""

        # Données de test
        label = 'Santé'
        sensible = False
        ordre = 3

        # Création d'une instance de Secteur sans description
        secteur = Secteur.objects.create(
            label=label,
            sensible=sensible,
            ordre=ordre
        )

        # Vérifications
        self.assertEqual(secteur.label, label)  # Vérifie que le nom du secteur est correct
        self.assertIsNone(secteur.description)  # Vérifie que la description est None par défaut
        self.assertFalse(secteur.sensible)  # Vérifie que le secteur n'est pas marqué comme sensible
        self.assertEqual(secteur.ordre, ordre)  # Vérifie que l'ordre d'affichage est correct

    def test_validation_without_required_fields(self):
        """Test pour vérifier que la validation échoue si les champs obligatoires ne sont pas fournis."""

        # Tenter de créer un Secteur sans le champ label
        secteur = Secteur(sensible=True, ordre=1)
        with self.assertRaises(ValidationError):
            secteur.full_clean()  # Doit lever une ValidationError car le champ label est manquant

        # Tenter de créer un Secteur sans le champ sensible
        secteur = Secteur(label='Agriculture', ordre=2)
        with self.assertRaises(ValidationError):
            secteur.full_clean()  # Doit lever une ValidationError car le champ sensible est manquant

        # Tenter de créer un Secteur sans le champ ordre
        secteur = Secteur(label='Éducation', sensible=False)
        with self.assertRaises(ValidationError):
            secteur.full_clean()  # Doit lever une ValidationError car le champ ordre est manquant