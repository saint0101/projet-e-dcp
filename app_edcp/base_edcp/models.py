from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from base_edcp import validators

# Create your models here.
# Gestionnaire personnalisé pour le modèle d'utilisateur
    ## - BaseUserManager: gérer la création des utilisateurs et des super utilisateurs
class CustomUserManager(BaseUserManager):
    """Manager pour le modèle User"""

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
    is_dpo = models.BooleanField(default=False, verbose_name='Est un Correspondant') # Est un Correspondant
    
    consentement = models.BooleanField(
        default=False,
        verbose_name='Je donne mon consentement', 
        help_text='''Veuillez cocher cette case pour donner votre consentement : 
        les données soumises via ce formulaire seront utilisées pour la création 
        et pour l'accomplissement de vos formalités sur la plateforme e-DCP. 
        Vos données ne seront traitées que par les agents habilités de l'Autorité de Protection.
        Vous pouvez à tous moments exercer vos droits exercer à l'adresse ..... ''')

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
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        verbose_name='Utilisateur'
    )
    # correspondant = models.ForeignKey('correspondant.Correspondant', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Correspondant')
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Date de Création'
    )
    # Lien vers le type de client
    typeclient = models.ForeignKey(
        'TypeClient', 
        on_delete=models.CASCADE, 
        null=True, 
        verbose_name='Type de Client'
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
    # Lien vers le secteur d'activité
    secteur = models.ForeignKey(
        'Secteur', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='Secteur d\'Activité'
    )
    # secteur_description = models.CharField(max_length=100, null=True, verbose_name='Description du Secteur')
    telephone = models.CharField(
        max_length=20, 
        null=True, 
        blank=True,
        verbose_name='Téléphone',
        # validators=[validators.validate_phone_number]
    )
    email_contact = models.EmailField(
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
        'Pays', 
        on_delete=models.CASCADE,
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
        'TypePiece', 
        null=True, 
        default='', 
        on_delete=models.CASCADE, 
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


# Modèle pour représenter une finalité
class Finalite(models.Model):
    """ Table finalite """
    label = models.CharField(max_length=255, verbose_name="Label")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.label


# Modèle pour représenter une sous-finalité liée à une finalité
class SousFinalite(models.Model):
    """ Table des sous finalités """
    finalite = models.ForeignKey('Finalite', related_name='sous_finalites', on_delete=models.CASCADE, verbose_name="Finalité")
    label = models.CharField(max_length=255, verbose_name="Label")
    sensible = models.BooleanField(default=False, verbose_name="Sensible")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        """ les champs à retourner """
        return f"{self.label} ({self.finalite.label})"


# Modèle pour représenter une légitimité
class Legitimite(models.Model):
    label = models.CharField(max_length=255, verbose_name="Label")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.label}"


# Modèle pour représenter un mode de recueil de consentement
class ModeRecueilConsent(models.Model):
    """ Table de recueil des concentement"""
    label = models.CharField(max_length=255, verbose_name="Label")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.label}"


# Modèle pour représenter un transfert de données
class Transfert(models.Model):
    """ Table des transferts de donnees """
    pays = models.CharField(max_length=255, verbose_name="Pays")
    destinataire = models.CharField(max_length=255, verbose_name="Destinataire")
    mode = models.CharField(max_length=255, verbose_name="Mode")
    type_destinataire = models.CharField(max_length=255, verbose_name="Type de Destinataire")

    def __str__(self):
        return f"{self.destinataire} ({self.pays})"


# Modèle pour représenter une personne concernée
class PersConcernee(models.Model):
    """ Table des personnes concernees """
    label = models.CharField(max_length=255, verbose_name="Label")
    sensible = models.BooleanField(default=False, verbose_name="Sensible")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Personne Concernée'
        verbose_name_plural = 'Personnes Concernées'

    def __str__(self):
        """ les champs à retourner """
        return f"{self.label}"


# Représente les types de données individuelles collectées.
# Par exemple, cela peut inclure des informations comme les noms, les adresses, etc.
class Donnee(models.Model):

    """ Modèle pour représenter une donnée individuelle """
    label = models.CharField(max_length=255, verbose_name="Label")
    sensible = models.BooleanField(default=False, verbose_name="Sensible")
    duree_conservation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Durée de Conservation")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.label}"


# Représente des ensembles de données traitées, qui peuvent inclure plusieurs types de données individuelles.
# Cela permet de grouper les données traitées en catégories pour la demande d’autorisation.
class DonneeTraitee(models.Model):
    """ Modèle pour représenter un ensemble de données traitées """
    label = models.CharField(max_length=255, verbose_name="Label")
    sensible = models.BooleanField(default=False, verbose_name="Sensible")
    duree_conservation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Durée de Conservation")
    donnees = models.ManyToManyField('Donnee', related_name='donnees_traitees', verbose_name="Données")
    id_categorie = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID Catégorie")

    def __str__(self):
        return f"{self.label}"


# Modèle pour représenter une interconnexion de données
class Interco(models.Model):
    """ Modèle pour représenter une interconnexion de données """
    destinataire = models.CharField(max_length=255, verbose_name="Destinataire")
    mode = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mode")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.destinataire}"


# Modèle pour représenter un support de collecte de données
class SupportCollecte(models.Model):
    """ Modèle pour représenter un support de collecte de données """
    label = models.CharField(max_length=255, verbose_name="Label")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.label}"


# Modèle pour représenter une méthode d'authentification
class Authentication(models.Model):
    """ Modèle pour représenter une méthode d'authentification """
    label = models.CharField(max_length=255, verbose_name="Label")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.label}"


# Décrit les méthodes de sauvegarde des données
class Backup(models.Model):
    """ Modèle pour représenter une méthode de sauvegarde des données """
    label = models.CharField(max_length=255, verbose_name="Label")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.label}"


# Spécifie les modes d’hébergement des données (par exemple, sur site ou dans le cloud).
class Hebergement(models.Model):
    """ Modèle pour représenter un mode d'hébergement des données """
    label = models.CharField(max_length=255, verbose_name="Label")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.label}"


# Modèle pour représenter une protection physique des données
class SecuritePhysique(models.Model):
    """ Modèle pour représenter une protection physique des données """
    label = models.CharField(max_length=255, verbose_name="Label")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.label}"


# Modèle pour regrouper les mesures de sécurité des données
class Securite(models.Model):
    """
    Modèle pour regrouper les mesures de sécurité des données
    Les relations ManyToManyField dans le modèle Securite permettent de gérer efficacement
        les multiples relations entre les mesures de sécurité et les différents aspects de la sécurité des données.
    """
    supports_collecte = models.ManyToManyField('SupportCollecte', related_name='securite_supports', verbose_name="Supports de Collecte")
    authentications = models.ManyToManyField('Authentication', related_name='securite_auth', verbose_name="Authentification")
    backups = models.ManyToManyField('Backup', related_name='securite_backup', verbose_name="Backup")
    hebergement = models.ManyToManyField('Hebergement', related_name='securite_hebergement', verbose_name="Hébergement")
    protect_physique = models.ManyToManyField('SecuritePhysique', related_name='securite_protect', verbose_name="Protection Physique")

    def __str__(self):
        return "Sécurité"


# Modèle pour représenter le statut de la demande
class Status(models.Model):
    """ Modèle pour représenter le statut de la demande """
    label = models.CharField(max_length=255, verbose_name="Label")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.label}"


# Modèle pour représenter un type de demande d'autorisation
class TypeDemandeAutorisation(models.Model):
    TYPE_CHOICES = [
        ('autorisation_prealable', 'Autorisation Préalable'),
        ('biometrie', 'Biométrie'),
        ('videosurveillance', 'Vidéosurveillance'),
        ('transfert_donnees_hors_espace_cdeao', 'Transfert de Données Hors Espace CEDEAO'),
        ('notification_violation_donnees_personnelles', 'Notification de Violation des Données Personnelles'),
        ('violation_conformite', 'Violation de la Conformité'),
        ('analyse_impact_protection_donnees_personnelles', 'Analyse d’Impact sur la Protection des Données Personnelles'),
        ('mise_en_conformite', 'Mise en Conformité'),
        ('declaration_normale', 'Déclaration Normale'),
        ('agreement', 'Agrément'),
        ('attestation_conformite', 'Attestation Conformité'),
        ('geolocalisation', 'Géolocalisation'),
    ]

    label = models.CharField(max_length=255, choices=TYPE_CHOICES, unique=True, verbose_name="Type de Demande d'Autorisation")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.get_label_display() # a méthode get_label_display(), ou en utilisant les valeurs de TYPE_CHOICES directement :
        # return dict(self.TYPE_CHOICES).get(self.label)


# Modèle principal pour représenter la demande d'autorisation
class DemandeAuto(models.Model):
    """ Modèle pour représenter un exemple de données liées a la demande d'autorisation """
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Utilisateur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
    organisation_id = models.CharField(max_length=255, verbose_name='ID de l\'Organisation')
    organisation_name = models.CharField(max_length=255, verbose_name='Nom de l\'Organisation')
    organisation_phone = models.CharField(max_length=255, verbose_name='Téléphone de l\'Organisation')
    consent_dcp = models.BooleanField(default=False, verbose_name='Consentement DCP')
    consent_docs = models.BooleanField(default=False, verbose_name='Consentement Documents')
    summary = models.TextField(blank=True, null=True, verbose_name='Résumé')
    traitement_sensible = models.BooleanField(default=False, verbose_name='Traitement Sensible')
    procedure_droit_persones = models.TextField(blank=True, null=True, verbose_name='Procédure Droit des Personnes')
    finalite = models.ForeignKey('Finalite', on_delete=models.CASCADE, verbose_name='Finalité')
    legitimite = models.ForeignKey('Legitimite', on_delete=models.CASCADE, verbose_name='Légitimité')
    modes_recueil_consent = models.ManyToManyField('ModeRecueilConsent', verbose_name='Modes de Recueil de Consentement')
    personnes_concernees = models.ManyToManyField('PersConcernee', verbose_name='Personnes Concernées')
    transferts = models.ManyToManyField('Transfert', verbose_name='Transferts')
    donnees_traitees = models.ManyToManyField('DonneeTraitee', verbose_name='Données Traitées')
    interco = models.ManyToManyField('Interco', verbose_name='Interconnexions')
    securite = models.ForeignKey('Securite', on_delete=models.CASCADE, verbose_name='Sécurité')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name='Statut')
    type_demande = models.ForeignKey('TypeDemandeAutorisation', on_delete=models.CASCADE, verbose_name="Type de Demande d'Autorisation")

    class Meta:
        verbose_name = 'Exemple de Modèle'
        verbose_name_plural = 'Exemples de Modèles'

    def __str__(self):
        return f"ID: {self.id} - Utilisateur: {self.user.username}"


class Fonction(models.Model):
    """ Table Fonction """
    fonction = models.CharField(max_length=100, verbose_name='Fonction')

    def __str__(self):
        """ les champs à retourner """
        return self.fonction


class Habilitation(models.Model):
    """ Table de gestion des habilisattions"""
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    fonction = models.ForeignKey('Fonction', on_delete=models.CASCADE)
    created = models.DateField(verbose_name='Date de Création')

    def __str__(self):
        """ les champs à retourner """
        return self.fonction


class FondJuridique(models.Model):
    """ Table Fond juridique """
    label = models.CharField(max_length=100)
    description = models.TextField(verbose_name='Description')

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Fondement Juridique'
        verbose_name_plural = 'Fondements Juridique'

    def __str__(self):
        """ les champs a retourner """
        return self.label


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


class Autorisation(models.Model):
    enregistrement = models.ForeignKey('Enregistrement', related_name='autorisations', on_delete=models.CASCADE)
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
