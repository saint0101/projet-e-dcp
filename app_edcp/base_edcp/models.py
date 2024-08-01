from django.db import models
from django.utils import timezone

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.
# Gestionnaire personnalisé pour le modèle d'utilisateur
    ## - BaseUserManager: gérer la création des utilisateurs et des super utilisateurs
class CustomUserManager(BaseUserManager):
    """Gestionnaire pour les utilisateurs"""

    # Méthode pour créer un utilisateur
    def create_user(self, email, password=None, **extra_fields):
        """Crée, enregistre et retourne un nouvel utilisateur."""
        # verifier si l'email est fourni
        if not email:
            raise ValueError("L'utilisateur doit avoire une adresse email.")
        # Crée une instance du modèle utilisateur
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # Définit le mot de passe de l'utilisateur
        user.set_password(password)
        # Sauvegarde l'utilisateur dans la base de données
        user.save(using=self._db)

        return user

    # Méthode pour créer un superutilisateur
    def create_superuser(self, email, password=None, **extra_fields):
        """Crée et enregistre un superutilisateur avec les informations fournies."""
        # Assurer que l'utilisateur est un membre du personnel et un superutilisateur
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Vérification des droits de superutilisateur
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Les superutilisateurs doivent avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Les superutilisateurs doivent avoir is_superuser=True.')

        # Création de l'utilisateur avec les droits de superutilisateur
        return self.create_user(email, password, **extra_fields)


# Gestion del'utiilsateur
    ## -  AbstractBaseUser: fournit les fonctionnalités de base pour un modèle d'utilisateur personnalisé
    ## - PermissionsMixin: fournit des fonctionnalités liées aux permissions et aux groupes
class User(AbstractBaseUser, PermissionsMixin):
    """Utilisateur de l'application """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création', null=True)
    username = models.CharField(max_length=100, blank=True, verbose_name='Nom d\'utilisateur')
    avatar = models.ImageField(upload_to='avatars', max_length=255, null=True, blank=True, verbose_name='Avatar')
    nom = models.CharField(max_length=225, verbose_name='Nom')
    prenoms = models.CharField(max_length=255, verbose_name='Prénoms')
    organisation = models.CharField(max_length=255, null=True, blank=True, verbose_name='Organisation')
    telephone = models.CharField(max_length=100, null=True, blank=True, verbose_name='Téléphone')
    fonction = models.CharField(max_length=255, null=True, blank=True, verbose_name='Fonction')
    consentement = models.CharField(max_length=255, null=True, blank=True, verbose_name='Consentement')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=True, verbose_name='Est Actif')
    is_staff = models.BooleanField(default=False, verbose_name='Est Membre du Personnel')
    email_verified = models.BooleanField(default=False)  # Utiliser une valeur par défaut pour éviter les valeurs nulles
    is_dpo = models.BooleanField(default=False) # Est un Correspondant

    # extenssier la gestionnaire d'utilisateur
    objects = CustomUserManager()

    # USERNAME_FIELD est défini sur 'email' pour l'authentification par e-mail.
    USERNAME_FIELD = 'email'

    #REQUIRED_FIELDS spécifie les champs supplémentaires requis
    REQUIRED_FIELDS = [
        'username',
        'nom',
        'prenoms',
    ]


    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        """ les champs a retourner pour l'affichage d'un objet USER"""
        return self.nom + ' ' + self.prenoms



class Enregistrement(models.Model):
    """ Table enregistrement """
    # Lien vers l'utilisateur
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Utilisateur')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
    # Lien vers le type de client
    typeclient = models.ForeignKey('TypeClient', on_delete=models.CASCADE, null=True, verbose_name='Type de Client')
    raisonsociale = models.CharField(max_length=100, verbose_name='Nom ou Raison Sociale', blank=True)
    representant = models.CharField(max_length=100, verbose_name='Représentant légal', blank=True)
    rccm = models.CharField(max_length=100, null=True, verbose_name='Numéro RCCM', blank=True)
    # Lien vers le secteur d'activité
    secteur = models.ForeignKey('Secteur', on_delete=models.CASCADE, null=True, verbose_name='Secteur d\'Activité')
    # secteur_description = models.CharField(max_length=100, null=True, verbose_name='Description du Secteur')
    telephone = models.CharField(max_length=20, null=True, verbose_name='Téléphone')
    email_contact = models.CharField(max_length=100, null=True, verbose_name='Email de Contact')
    site_web = models.URLField(max_length=100, null=True, verbose_name='Site Web', blank=True)
    # Lien vers le pays
    pays = models.ForeignKey('Pays', on_delete=models.CASCADE, null=True, verbose_name='Pays')
    ville = models.CharField(max_length=100, null=True, verbose_name='Ville')
    adresse_geo = models.CharField(max_length=100, null=True, verbose_name='Adresse Géographique')
    adresse_bp = models.CharField(max_length=100, null=True, verbose_name='Boîte Postale', blank=True)
    gmaps_link = models.URLField(max_length=255, null=True, verbose_name='Lien Google Maps', blank=True)
    effectif = models.IntegerField(null=True, verbose_name='Effectif', blank=True)
    presentation = models.TextField(max_length=255, null=True, verbose_name='Présentation de l\'activité')
    # Champs personne physique
    type_piece = models.ForeignKey('TypePiece', null=True, default='', on_delete=models.CASCADE, verbose_name='Type de pièce d\'identité', blank=True)
    num_piece = models.CharField(max_length=100, null=True, verbose_name='Numéro de la pièce', blank=True)
    has_dpo = models.BooleanField(verbose_name='A désigné un Correspondant', default=False)
    # Fichiers (pièces justificatives)
    file_piece = models.FileField(null=True, blank=True, upload_to='enregistrement/docs', verbose_name='Pièce d\'identité')
    file_rccm = models.FileField(null=True, blank=True, upload_to='enregistrement/docs', verbose_name='Copie du Registre du Commerce')
    file_mandat = models.FileField(null=True, blank=True, upload_to='enregistrement/docs', verbose_name='Mandat de représentation', help_text='Si vous n\'êtes pas le représentant légal, Joindre un mandat signé par le représentatnt légal de l\'organisation')

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Enregistrement'
        verbose_name_plural = 'Enregistrements'

    def __str__(self):
        """ les champs a retourner """
        return self.raisonsociale


class TypeClient(models.Model):
    """ Table du type des clients """
    label = models.CharField(max_length=100, verbose_name='Type de Client')
    description = models.CharField(max_length=100, null=True, verbose_name='Description du Type de Client', blank=True)
    sensible = models.BooleanField(null=True, verbose_name='Est Sensible', default=False)
    ordre = models.IntegerField(null=True, verbose_name='Ordre d\'Affichage', default=0)

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Type Client'
        verbose_name_plural = 'Types Clients'

    def __str__(self):
        """ les champs a retourner """
        return self.label
    
class TypePiece(models.Model):
    """ Table du type de pièces d'identité """
    label = models.CharField(max_length=100, verbose_name='Type de pièce d\'identité')
    description = models.CharField(max_length=100, null=True, verbose_name='Description du Type de pièce', blank=True)
    sensible = models.BooleanField(null=True, verbose_name='Est Sensible', default=False)
    ordre = models.IntegerField(null=True, verbose_name='Ordre d\'affichage', default=0)

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Type de pièce'
        verbose_name_plural = 'Types de pièces'

    def __str__(self):
        """ les champs a retourner """
        return self.label


class Secteur(models.Model):
    """ Table secteur d'activité """
    label = models.CharField(max_length=100, verbose_name='Secteur d\'Activité')
    sensible = models.BooleanField(verbose_name='Est Sensible')
    ordre = models.IntegerField(verbose_name='Ordre d\'Affichage')

    def __str__(self):
        """ les champs a retourner """
        return self.label


class Pays(models.Model):
    """ Table des pays """
    label = models.CharField(max_length=100, verbose_name='Nom du Pays')

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Pays'
        verbose_name_plural = 'Pays'

    def __str__(self):
        """ les champs a retourner """
        return self.label


class CasExemption(models.Model):
    """  Cas Exemption """
    casexemption = models.CharField(max_length=100)

    def __str__(self):
        """ les champs a retourner """
        return self.casexemption


class CategorieDCP(models.Model):
    """  Cas Categorie DCP """
    categoriedcp = models.CharField(max_length=11)

    def __str__(self):
        """ les champs a retourner """
        return self.categoriedcp


class CategorieTrait(models.Model):
    """  Cas Categorie Trait """
    categorie = models.CharField(max_length=100)

    def __str__(self):
        """ les champs a retourner """
        return self.categorie


class Finalite(models.Model):
    """ Table finalite """
    label = models.CharField(max_length=100)
    sensible = models.CharField(max_length=100)
    ordre = models.IntegerField()

    def __str__(self):
        """ les champs a retourner """
        return f"La finalié {self.label} a pour {self.sensible}"


class SousFinalite(models.Model):
    """ Table des sous finalités """
    label = models.CharField(max_length=100)
    sensible = models.BooleanField()
    ordre = models.IntegerField()
    finalite = models.ForeignKey('Finalite', on_delete=models.CASCADE)

    def __str__(self):
        """ les champs à retourner """
        return f"La finalié {self.label} a pour {self.sensible} lié à l'id de la sous finalité {self.finalite}"


class Fonction(models.Model):
    """ Table Fonction """
    fonction = models.CharField(max_length=100)

    def __str__(self):
        """ les champs à retourner """
        return self.fonction


class Habilitation(models.Model):
    """ Table de gestion des habilisattions"""
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    fonction = models.ForeignKey('Fonction', on_delete=models.CASCADE)
    created = models.DateField()

    def __str__(self):
        """ les champs à retourner """
        return self.fonction


class FondJuridique(models.Model):
    """ Table Fond juridique """
    label = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Fondement Juridique'
        verbose_name_plural = 'Fondements Juridique'

    def __str__(self):
        """ les champs a retourner """
        return self.label


class Role(models.Model):
    """ Table des roles """
    role = models.CharField(max_length=100)

    def __str__(self):
        """ le champs a retourner """
        return self.role


class PersConcernee(models.Model):
    """ Table des personnes concernees """
    label = models.CharField(max_length=100, null=True)
    sensible = models.BooleanField()
    ordre = models.IntegerField()

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Personne Concernée'
        verbose_name_plural = 'Personnes Concernées'

    def __str__(self):
        """ les champs à retourner """
        return f"La finalié {self.label} a pour {self.sensible}"


class Notification(models.Model):
    """ Table notification """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='Utilisateur') # Référence à l'utilisateur recevant la notification
    message = models.TextField() # message de notification
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date et heure de création')  # Date et heure de création de la notification
    is_read = models.BooleanField(default=False, verbose_name='Est lu')    # Indique si la notification a été lue

    def __str__(self):
        """ les champs à retourner """
        return f'Notification pour {self.user} - {self.message}'



class Autorisation(models.Model):
    enregistrement = models.ForeignKey(Enregistrement, related_name='autorisations', on_delete=models.CASCADE)
    numero_autorisation = models.CharField(max_length=20)  # Format : YYYY-NNNN
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Autorisation {self.numero_autorisation} pour {self.enregistrement}"


class JournalTransaction(models.Model):
    """ Table des transactions """
    created = models.DateField()
    transaction = models.CharField(max_length=100)
    cible = models.CharField(max_length=100)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Journal Transaction'
        verbose_name_plural = 'Journals Transactions'

    def __str__(self):
        return self.transaction
