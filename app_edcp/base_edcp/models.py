from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
)
# apps

from options.models import TypeClient, TypePiece, Secteur, Pays, GroupName
from base_edcp import validators

# Create your models here.
# Gestionnaire personnalisé pour le modèle d'utilisateur
    ## - BaseUserManager: gérer la création des utilisateurs et des super utilisateurs
class CustomUserManager(BaseUserManager):
    """Manager pour le modèle personnalisé User"""

    # Méthode pour créer un utilisateur
    def create_user(self, email, password=None, **extra_fields):
        """Créer et retourner un utilisateur avec un email et un mot de passe"""
        # verifier si l'email est fourni
        if not email:
            raise ValueError("L'adresse email doit être fournie.")
        # Crée une instance du modèle utilisateur
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # Définit le mot de passe de l'utilisateur
        user.set_password(password)
        # Sauvegarde l'utilisateur dans la base de données
        user.save(using=self._db)

        return user

    # Méthode pour créer un superutilisateur
    def create_superuser(self, email, password=None, **extra_fields):
        """Créer et retourner un super utilisateur avec un email et un mot de passe"""
        # Assurer que l'utilisateur est un membre du personnel et un superutilisateur
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Vérification des droits de superutilisateur
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Les super utilisateurs doivent avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Les super utilisateurs doivent avoir is_superuser=True.')

        # Création de l'utilisateur avec les droits de superutilisateur
        return self.create_user(email, password, **extra_fields)


# Gestion del'utiilsateur
    ## -  AbstractBaseUser: fournit les fonctionnalités de base pour un modèle d'utilisateur personnalisé
    ## - PermissionsMixin: fournit des fonctionnalités liées aux permissions et aux groupes
class User(AbstractBaseUser, PermissionsMixin):
    """Utilisateur de l'application """
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création', null=True)
    username = models.CharField(max_length=100, blank=True, verbose_name='Nom d\'utilisateur')
    avatar = models.ImageField(upload_to='avatars', max_length=255, null=True, blank=True, verbose_name='Avatar', help_text='Photo de profil (facultative)')
    nom = models.CharField(max_length=225, verbose_name='Nom', validators=[validators.validate_charfield, validators.validate_no_special_chars])
    prenoms = models.CharField(max_length=255, verbose_name='Prénoms', validators=[validators.validate_charfield, validators.validate_no_special_chars])
    organisation = models.CharField(max_length=255, null=True, blank=True, verbose_name='Organisation', validators=[validators.validate_charfield, validators.validate_no_special_chars])
    telephone = models.CharField(max_length=100, null=True, blank=True, verbose_name='Téléphone', validators=[validators.validate_charfield, validators.validate_no_special_chars])
    fonction = models.CharField(max_length=255, null=True, blank=True, verbose_name='Fonction', validators=[validators.validate_charfield, validators.validate_no_special_chars])
    is_active = models.BooleanField(default=True, verbose_name='Est Actif')
    is_staff = models.BooleanField(default=False, verbose_name='Est Membre du Personnel')
    email_verified = models.BooleanField(default=False, verbose_name='Email Vérifié')  # Utiliser une valeur par défaut pour éviter les valeurs nulles
    must_reset = models.BooleanField(default=False, verbose_name='Doit Reinitialiser son Mot de Passe')
    is_dpo = models.BooleanField(default=False, verbose_name='Est un Correspondant') # Est un Correspondant
    is_business_account = models.BooleanField(default=False, verbose_name='Est un compte entreprise')
    
    consentement = models.BooleanField(
        default=False,
        #null=True,  # Autoriser temporairement les valeurs NULL
        verbose_name='Je donne mon consentement',
        help_text='''Veuillez cocher cette case pour donner votre consentement :
        les données soumises via ce formulaire seront utilisées pour la création
        et pour l'accomplissement de vos formalités sur la plateforme e-DCP.
        Vos données ne seront traitées que par les agents habilités de l'Autorité de Protection.
        Vous pouvez à tous moments exercer vos droits exercer à l'adresse ..... ''')

    # Relation ManyToMany pour gérer les groupes de l'utilisateur
    """ groups = models.ManyToManyField(
        Group,
        related_name="base_edcp_user_set",  # Nom unique pour la relation inverse avec 'groups'
        blank=True,
        help_text="Les groupes auxquels cet utilisateur appartient.",
        verbose_name="Groupes",
    )

    # Relation ManyToMany pour gérer les permissions spécifiques de l'utilisateur
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="base_edcp_user_permissions_set",  # Nom unique pour la relation inverse avec 'user_permissions'
        blank=True,
        help_text="Permissions spécifiques pour cet utilisateur.",
        verbose_name="Permissions des utilisateurs",
    )  """

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
    
    """ def can_validate(self, demande):
        from demande.views import get_niv_validation_max
        niv_validation = get_niv_validation_max(self)
        print ('niv_validation', self.object, niv_validation)
        return True if niv_validation >= demande.analyse.niv_validation else False """
            

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        """Retourne une représentation sous forme de chaîne de l'utilisateur"""
        return f"{self.nom} ({self.prenoms})"


class GroupExtension(models.Model):
    """ Extension des groupes par défaut de Django. """
    group_name = models.ForeignKey(
        GroupName, 
        on_delete=models.CASCADE, 
        verbose_name='Nom du Groupe',
        null=True,
        blank=True,
    )
    group = models.OneToOneField(
        Group,
        on_delete=models.PROTECT,
    )
    niv_validation = models.IntegerField(
        default=0,
        verbose_name='Niveau de Validation',
    )

    def __str__(self):
        return f"{self.group.name} (Niv. validation {self.niv_validation})"


class Enregistrement(models.Model):
    """ Table enregistrement (représente une organisation) """
    user = models.ForeignKey( # utilisateur ayant effectué l'enregistrement.
        User, 
        on_delete=models.PROTECT, 
        verbose_name='Utilisateur'
    )
    created_at = models.DateTimeField( # date d'enregistrement.
        auto_now_add=True, 
        verbose_name='Date de Création'
    )
    typeclient = models.ForeignKey( # type d'organisation
        TypeClient, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='Type d\'organisation'
    )
    raisonsociale = models.CharField(
        max_length=100,
        verbose_name='Nom ou Raison Sociale',
        validators=[validators.validate_charfield, validators.validate_no_special_chars],
        help_text='Nom de la personne physique ou de l\'organisation à enregistrer'
    )
    idu = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Numéro d\'IDentifiant Unique'
    )
    representant = models.CharField(
        max_length=100,
        verbose_name='Nom du représentant légal',
        blank=True
    )
    rccm = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        validators=[validators.validate_charfield, validators.validate_no_special_chars, validators.validate_rccm_idu],
        verbose_name='Numéro RCCM'
    )
    secteur = models.ForeignKey( # secteur d'activité
        Secteur, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Secteur d\'Activité'
    )
    telephone = models.CharField( # numéro de téléphone de l'organisation
        max_length=20, 
        null=True, 

        blank=True,
        verbose_name='Téléphone',
        # validators=[validators.validate_phone_number]
    )
    email_contact = models.EmailField( # email de contact
        max_length=100, 
        null=True, 
        verbose_name='Email de Contact'
    )
    site_web = models.URLField(
        max_length=100,
        null=True,
        verbose_name='Site Web',
        blank=True
    )
    pays = models.ForeignKey(
        Pays, 
        on_delete=models.SET_NULL,
        null=True, 
        verbose_name='Pays'
    )
    ville = models.CharField(
        max_length=100,
        null=True,
        validators=[validators.validate_charfield, validators.validate_no_special_chars],
        verbose_name='Ville'
    )
    adresse_geo = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        validators=[validators.validate_charfield, validators.validate_no_special_chars],
        verbose_name='Adresse Géographique'
    )
    adresse_bp = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Boîte Postale',
        blank=True
    )
    gmaps_link = models.URLField(
        max_length=255,
        null=True,
        verbose_name='Lien Google Maps',
        blank=True
    )
    effectif = models.IntegerField(
        null=True,
        verbose_name='Effectif',
        blank=True
    )
    presentation = models.TextField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Présentation de l\'activité'
    )
    # Champs personne physique
    type_piece = models.ForeignKey(
        TypePiece, 
        null=True, 
        default='', 
        on_delete=models.SET_NULL, 
        verbose_name='Type de pièce d\'identité', 
        blank=True
    )
    num_piece = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Numéro de la pièce',
        blank=True
    )
    has_dpo = models.BooleanField(
        verbose_name='A désigné un Correspondant',
        default=False
    )
    # Fichiers (pièces justificatives)
    file_piece = models.FileField(
        null=True,
        blank=True,
        upload_to='docs/enregistrement',
        verbose_name='Pièce d\'identité',
        validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.'
    )
    file_rccm = models.FileField(
        null=True,
        blank=True,
        upload_to='docs/enregistrement',
        verbose_name='Copie du Registre du Commerce',
        validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.'
    )
    file_mandat = models.FileField(
        null=True,
        blank=True,
        upload_to='docs/enregistrement',
        verbose_name='Mandat de représentation',
        validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        help_text='Si vous n\'êtes pas le représentant légal, Joindre un mandat signé par le représentatnt légal de l\'organisation')

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Enregistrement'
        verbose_name_plural = 'Enregistrements'

    def __str__(self):
        """ les champs a retourner """
        return self.raisonsociale


# Modèle pour représenter un rôle
class Role(models.Model):
    """ odèle pour représenter un rôle """
    role = models.CharField(max_length=100, verbose_name="Rôle")

    def __str__(self):
        return self.role


class Notification(models.Model):
    """ Table notification """
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='notifications', verbose_name='Utilisateur') # Référence à l'utilisateur recevant la notification
    message = models.TextField() # message de notification
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date et heure de création')  # Date et heure de création de la notification
    is_read = models.BooleanField(default=False, verbose_name='Est lu')    # Indique si la notification a été lue

    def __str__(self):
        """ les champs à retourner """
        return f'Notification pour {self.user} - {self.message}'


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
