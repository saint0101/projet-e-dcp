from django.db import models

# Create your models here.


class TypeClient(models.Model):
    """ Table du type des clients """
    label = models.CharField(max_length=100, verbose_name='Type de Client')
    description = models.CharField(max_length=100, null=True, verbose_name='Description du Type de Client')
    sensible = models.BooleanField(null=True, verbose_name='Est Sensible')
    ordre = models.IntegerField(null=True, verbose_name='Ordre d\'Affichage')

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Type Client'
        verbose_name_plural = 'Types Clients'

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

    def __str__(self):
        """ les champs à retourner """
        return f"La finalié {self.label} a pour {self.sensible}"


class User(models.Model):
    """Utilisateur de la BD """
    login = models.CharField(max_length=100, unique=True, verbose_name='Nom d\'Utilisateur')
    avatar = models.FileField(upload_to='avatars/', max_length=255, null=True, blank=True, verbose_name='Avatar')
    nom = models.CharField(max_length=225, verbose_name='Nom')
    prenoms = models.CharField(max_length=255, verbose_name='Prénoms')
    organisation = models.CharField(max_length=255, null=True, blank=True, verbose_name='Organisation')
    telephone = models.CharField(max_length=100, null=True, blank=True, verbose_name='Téléphone')
    fonction = models.CharField(max_length=255, null=True, blank=True, verbose_name='Fonction')
    consentement = models.CharField(max_length=255, null=True, blank=True, verbose_name='Consentement')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=True, verbose_name='Est Actif')
    is_staff = models.BooleanField(default=False, verbose_name='Est Membre du Personnel')

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        """ les champs a retourner """
        return f"Nom {self.nom}, Fonction {self.fonction}, Organisation {self.organisation}, Numéro de téléphone {self.telephone}"


class Notification(models.Model):
    """ Table notification """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='Utilisateur') # Référence à l'utilisateur recevant la notification
    message = models.TextField() # message de notification
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date et heure de création')  # Date et heure de création de la notification
    is_read = models.BooleanField(default=False, verbose_name='Est lu')    # Indique si la notification a été lue

    def __str__(self):
        """ les champs à retourner """
        return f'Notification pour {self.user} - {self.message}'


class Enregistrement(models.Model):
    """ Table enregistrement """
    # Lien vers l'utilisateur
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Utilisateur')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
    # Lien vers le type de client
    typeclient = models.ForeignKey('TypeClient', on_delete=models.CASCADE, null=True, verbose_name='Type de Client')
    raisonsociale = models.CharField(max_length=100, verbose_name='Raison Sociale')
    representant = models.CharField(max_length=100, verbose_name='Représentant')
    rccm = models.CharField(max_length=100, null=True, verbose_name='RCCM')
    # Lien vers le secteur d'activité
    secteur = models.ForeignKey('Secteur', on_delete=models.CASCADE, null=True, verbose_name='Secteur d\'Activité')
    secteur_description = models.CharField(max_length=100, null=True, verbose_name='Description du Secteur')
    presentation = models.CharField(max_length=255, null=True, verbose_name='Présentation')
    telephone = models.CharField(max_length=20, null=True, verbose_name='Téléphone')
    email_contact = models.CharField(max_length=100, null=True, verbose_name='Email de Contact')
    site_web = models.CharField(max_length=100, null=True, verbose_name='Site Web')
    # Lien vers le pays
    pays = models.ForeignKey('Pays', on_delete=models.CASCADE, null=True, verbose_name='Pays')
    ville = models.CharField(max_length=100, null=True, verbose_name='Ville')
    adresse_geo = models.CharField(max_length=100, null=True, verbose_name='Adresse Géographique')
    adresse_bp = models.CharField(max_length=100, null=True, verbose_name='Boîte Postale')
    gmaps_link = models.CharField(max_length=255, null=True, verbose_name='Lien Google Maps')
    effectif = models.IntegerField(null=True, verbose_name='Effectif')


    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Enregistrement'
        verbose_name_plural = 'Enregistrements'

    def __str__(self):
        """ les champs a retourner """
        return self.raisonsociale


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

    def __str__(self):
        return self.transaction

# TODO: ajouter a l'admin (SousFinalite, Role, PersConcernee, User, Habilitation, JournalTransaction)