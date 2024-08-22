from django.db import models


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
""" class DemandeAutoOld(models.Model):
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
 """

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



class Autorisation(models.Model):
    enregistrement = models.ForeignKey('Enregistrement', related_name='autorisations', on_delete=models.CASCADE)
    numero_autorisation = models.CharField(max_length=20)  # Format : YYYY-NNNN
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Autorisation {self.numero_autorisation} pour {self.enregistrement}"