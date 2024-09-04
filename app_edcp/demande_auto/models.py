from django.db import models
from django.core.validators import FileExtensionValidator

from base_edcp.models import User, Enregistrement
from base_edcp import validators
from options.models import Pays
from options.models import OptionModel
from demande.models import Demande, Status
# from .forms import TraitementFormDisabled, TransfertFormDisabled, VideoFormDisabled, BiometrieFormDisabled



  
class TypeDemandeAuto(OptionModel):
  """ Type de demande d'autorisation """
  finalites = models.ManyToManyField(
    'Finalite',
    verbose_name='Finalités liées à ce type de demande',
    related_name='types_demande',
  )

  class Meta:
    verbose_name = 'Type de demande'
    verbose_name_plural = 'Types de demande'


class Finalite(OptionModel):
  """ Finalité du traiment """
  pass


class SousFinalite(OptionModel):
  """ Sous-finalité du traitement """
  finalite = models.ForeignKey(
    'Finalite',
    on_delete=models.CASCADE,
    verbose_name='Finalité',
  )



class PersConcernee(OptionModel):
  """ Catégorie de personne concernée """
  class Meta:
    verbose_name = 'Catégorie de personnes concernées'
    verbose_name_plural = 'Catégories de personnes concernées'



class FondementJuridique(OptionModel):
  """ Fondement juridique """
  class Meta:
    verbose_name = 'Fondement juridique'
    verbose_name_plural = 'Fondements juridiques'


class ModeRecueilConsent(OptionModel):
  """ Table de recueil des concentement"""
  class Meta:
    verbose_name = 'Mode de recueil de consentement'
    verbose_name_plural = 'Modes de recueil de consentement'


class ModeTransfert(OptionModel):
  class Meta:
    verbose_name = 'Mode de transfert des données'
    verbose_name_plural = 'Modes de transfert des données'


class TypeDestinataireTransfert(OptionModel):
  class Meta:
    verbose_name = 'Type de destinataire des données'
    verbose_name_plural = 'Types de destinataire des données'


class TransfertDonnees(models.Model):
  """ Table des transferts de donnees """
  # pays = models.CharField(max_length=255, verbose_name="Pays")
  created_at = models.DateTimeField( # date d'enregistrement.
    auto_now_add=True, 
    verbose_name='Date de Création'
  )
  pays = models.ForeignKey(
    Pays, 
    on_delete=models.SET_NULL,
    null=True, 
    verbose_name='Pays de destination'
    )
  destinataire = models.CharField(
    max_length=255, 
    blank=True,
    null=True,
    verbose_name="Destinataire données"
    )
  mode_transfert = models.ForeignKey(
    ModeTransfert,
    null=True,
    on_delete=models.SET_NULL, 
    verbose_name="Mode de transfert des données"
    )
  type_destinataire = models.ForeignKey(
    TypeDestinataireTransfert, 
    null=True,
    on_delete=models.SET_NULL,
    verbose_name="Type de Destinataire"
    )
  
  class Meta:
    verbose_name = 'Transfert de données'
    verbose_name_plural = 'Transferts de données'

  def __str__(self):
    return f"Transfert vers {self.destinataire} ({self.pays})"


class CategorieDonnees(OptionModel):
  """ Categorie de données """
  class Meta:
    verbose_name = 'Categorie de données'
    verbose_name_plural = 'Categories de données'


class TypeDonnees(OptionModel):
  """ Types de données personnelles """
  categorie_donnees = models.ForeignKey(
    CategorieDonnees, 
    on_delete=models.SET_NULL, 
    null=True,
    verbose_name="Categorie de données"
  )
  
  class Meta:
    verbose_name = 'Type de données personnelles'
    verbose_name_plural = 'Types de données personnelles'


class ModeInterconnexion(OptionModel):
  class Meta:
    verbose_name = 'Mode d\'interconnexion'
    verbose_name_plural = 'Modes d\'interconnexion'


class InterConnexion(models.Model):
  created_at = models.DateTimeField( # date d'enregistrement.
    auto_now_add=True, 
    verbose_name='Date de Création'
  )
  destinataire = models.CharField(
    max_length=100, 
    null=True,
    verbose_name="Destinataire des données"
    )
  mode_interconnexion = models.ForeignKey(
    ModeInterconnexion,
    null=True,
    on_delete=models.SET_NULL, 
    verbose_name="Mode d'interconnexion"
    )
  description = models.CharField(
    max_length=255, 
    blank=True,
    null=True,
    verbose_name="Description de l'interconnexion"
    )
  
  class Meta:
    verbose_name = 'Interconnexion'
    verbose_name_plural = 'Interconnexions'


class EchelleNotation(OptionModel):
  """ Echelle de notation des demandes d'autorisation """
  valeur = models.IntegerField(
    default=0,
    verbose_name='Valeur'
  )

  class Meta:
    verbose_name = 'Echelle de notation'
    verbose_name_plural = 'Echelles de notation'


def get_default_status():
  """ Renvoie le statut par défaut que doit avoir une nouvelle demande d'autorisation """
  default_status = Status.objects.get(label='brouillon')
  return default_status.id


class DemandeAuto(Demande):
    """ Demande d'autorisation """
    """ user = models.ForeignKey(
      User, 
      on_delete=models.CASCADE, 
      blank=True,
      verbose_name="Utilisateur"
    )
    organisation = models.ForeignKey(
      Enregistrement, 
      on_delete=models.CASCADE, 
      verbose_name='Organisation',
      blank=True,
    )
    created_at = models.DateTimeField(
      auto_now_add=True, 
      verbose_name='Date de Création'
    )
    status = models.ForeignKey(
      Status, 
      blank=True,
      on_delete=models.CASCADE, 
      verbose_name='Statut de la demande'
    ) """
    finalite = models.ForeignKey(
      'Finalite', 
      null=True,
      blank=True,
      on_delete=models.CASCADE, 
      verbose_name='Finalité'
    )
    sous_finalites = models.ManyToManyField(
      'SousFinalite', 
      blank=True,
      verbose_name='Sous-finalités'
    )
    description_traitement = models.TextField(
      blank=True, 
      null=True, 
      verbose_name='Description du traitement'
    )
    type_demande = models.ForeignKey(
      'TypeDemandeAuto', 
      on_delete=models.PROTECT, 
      verbose_name="Type de Demande d'Autorisation",
      blank=True
    )
    summary = models.TextField(
      blank=True, 
      null=True, 
      verbose_name='Description du traitement'
    )
    personnes_concernees = models.ManyToManyField(
      'PersConcernee',
      blank=True,
      verbose_name='Personnes Concernées'
    )
    consent_docs = models.BooleanField(
      default=False, 
      verbose_name='Consentement Documents'
    )

    """ Autres champs à prévoir """
    # traitement_sensible = models.BooleanField(default=False, verbose_name='Traitement Sensible')
    # procedure_droit_persones = models.TextField(blank=True, null=True, verbose_name='Procédure Droit des Personnes')
    # finalite = models.ForeignKey('Finalite', on_delete=models.CASCADE, verbose_name='Finalité')
    # legitimite = models.ForeignKey('Legitimite', on_delete=models.CASCADE, verbose_name='Légitimité')
    # modes_recueil_consent = models.ManyToManyField('ModeRecueilConsent', verbose_name='Modes de Recueil de Consentement')
    # 
    # transferts = models.ManyToManyField('Transfert', verbose_name='Transferts')
    # donnees_traitees = models.ManyToManyField('DonneeTraitee', verbose_name='Données Traitées')
    # interco = models.ManyToManyField('Interco', verbose_name='Interconnexions')
    # securite = models.ForeignKey('Securite', on_delete=models.CASCADE, verbose_name='Sécurité')
    
    def get_url_name(self):
      return 'dashboard:demande_auto'
    

    def get_instance_form(self):
      print('getting instance form : ', self.type_demande.label)
      from .forms import TraitementFormDisabled, TransfertFormDisabled, VideoFormDisabled, BiometrieFormDisabled
      type_demande_label = self.type_demande.label
      
      if type_demande_label == 'traitement': 
        return TraitementFormDisabled(instance=self)

      if type_demande_label == 'transfert':
        return TransfertFormDisabled(instance=self)

      if type_demande_label == 'videosurveillance':
        return VideoFormDisabled(instance=self)

      if type_demande_label == 'biometrie':
        return BiometrieFormDisabled(instance=self)


    class Meta:
      verbose_name = 'Demande d\'autorisation'
      verbose_name_plural = 'Demandes d\'autorisation'

    def __str__(self):
      return f"Autorisation de {self.type_demande} #{self.num_demande}"
    

class DemandeAutoTraitement(DemandeAuto):
  """ Sous-classe de demande d'autorisation pour les traitements """
  autre_sous_finalites = models.CharField(
    max_length=255, null=True, blank=True,
    verbose_name='Autre sous-finalité'
  )
  fondement_juridique = models.ForeignKey(
    'FondementJuridique',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    max_length=255,
    verbose_name='Fondement Juridique'
  )
  description_fondement= models.TextField(
    null=True, blank=True,
    verbose_name='Description du fondement juridique'
  )
  mode_consentement = models.ManyToManyField(
    'ModeRecueilConsent',
    verbose_name='Modes de recueil du consentement'
  )
  autre_mode_consentement = models.CharField(
    max_length=255, null=True, blank=True,
    verbose_name='Autre mode de recueil du consentement'
  )
  procedures = models.TextField(
    null=True,
    blank=True,
    max_length=500,
    verbose_name='Procédures de gestion des droits des personnes'
  )
  donnees_traitees = models.ManyToManyField(
    'TypeDonnees',
    verbose_name='Données traitees'
  )
  autre_donnees_traitees = models.CharField(
    max_length=255, null=True, blank=True,
    verbose_name='Autre données traitées'
  )
  transferts = models.ManyToManyField(
    'TransfertDonnees',
    blank=True,
    verbose_name='Transferts de données'
  )
  interconnexions = models.ManyToManyField(
    'InterConnexion',
    blank=True,
    verbose_name='Interconnexions de données'
  )
  mesures_securite = models.TextField(
    null=True,
    blank=True,
    max_length=500,
    verbose_name='Mesures de Securité'
  )
  file_consentement = models.FileField(
    null=True,
    blank=True,
    upload_to='docs/demande_auto',
    verbose_name='Preuve du recueil du consentement',
    validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
    help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.'
  )
  file_cgu = models.FileField(
    null=True,
    blank=True,
    upload_to='docs/demande_auto',
    verbose_name='Conditions Générales d\'Utilisation',
    validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
    help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.'
  )
  
  @classmethod
  def get_type_demande(cls):
    return TypeDemandeAuto.objects.get(label='traitement')
  
  def get_instance_form(self):
    from .forms import TraitementFormDisabled
    return TraitementFormDisabled(instance=self)


class DemandeAutoTransfert(DemandeAuto):
  """ Sous-classe de demande d'autorisation pour les transferts de données """
  destination = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    verbose_name='Destination du transfert'
  )
  motif_transfert = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    verbose_name='Motif du Transfert'
  )
  mesures_securite = models.TextField(
    null=True,
    blank=True,
    max_length=500,
    verbose_name='Mesures de Securité'
  )

  @classmethod
  def get_type_demande(cls):
    return TypeDemandeAuto.objects.get(label='transfert')
  
  def get_instance_form(self):
    from .forms import TransfertFormDisabled
    return TransfertFormDisabled(instance=self)


class DemandeAutoVideo(DemandeAuto):
  """ Sous-classe de demande d'autorisation pour la vidéosurveillance """
  types_cameras = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    verbose_name='Types de cameras'
  )
  nb_cameras = models.IntegerField(
    null=True,
    blank=True,
    verbose_name='Nombre de cameras'
  )
  mesures_securite = models.TextField(
    null=True,
    blank=True,
    max_length=500,
    verbose_name='Mesures de Securité'
  )

  @classmethod
  def get_type_demande(cls):
    return TypeDemandeAuto.objects.get(label='videosurveillance')
  
  def get_instance_form(self):
    from .forms import VideoFormDisabled
    return VideoFormDisabled(instance=self)
  

class DemandeAutoBiometrie(DemandeAuto):
  """ Sous-classe de demande d'autorisation pour la biométrie """
  types_dispositifs = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    verbose_name='Types de dispositifs'
  )
  nb_dispositifs = models.IntegerField(
    null=True,
    blank=True,
    verbose_name='Nombre de dispositifs'
  )
  mesures_securite = models.TextField(
    null=True,
    blank=True,
    max_length=500,
    verbose_name='Mesures de Securité'
  )

  @classmethod
  def get_type_demande(cls):
    return TypeDemandeAuto.objects.get(label='biometrie')
  
  def get_instance_form(self):
    from .forms import BiometrieFormDisabled
    return BiometrieFormDisabled(instance=self)


""" class HistoriqueDemande(models.Model):
  # Historique des actions effectuées dans le traitement d'une demande d'autorisation
  demande = models.ForeignKey(
    'DemandeAuto',
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Demande d\'autorisation'
  )
  status = models.ForeignKey(
    Status, 
    blank=True,
    on_delete=models.CASCADE, 
    verbose_name='Statut de la demande'
  )
  action = models.ForeignKey(
    'ActionDemande',
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Action effectuée'
  )
  auteur = models.ForeignKey(
    User,
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Auteur'
  )
  created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='Date de Création'
  )
  is_private = models.BooleanField(
    default=False,
    verbose_name='Est confidentiel'
  )

  class Meta:
      verbose_name = 'Historique de la demande'
      verbose_name_plural = 'Historiques des demandes'

  def __str__(self):
    return f"{self.action.description}"
 """

"""
class AnalyseDemande(models.Model):
  # Analyse d'une demande
  demande = models.OneToOneField(
    'DemandeAuto',
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Demande d\'autorisation'
  )
  agent = models.ForeignKey(
    User,
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Agent en charge'
  )
  status = models.ForeignKey(
    Status,
    blank=True,
    null=True,
    on_delete=models.CASCADE,
    verbose_name='Statut de l\'analyse'
  )
  created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='Date de Création'
  )
  niveau_validation = models.IntegerField(
    blank=True,
    null=True,
    default=1,
    verbose_name='Niveau de validation requis'
  )
  critere_completude = models.IntegerField(
    blank=True,
    null=True,
    default=0,
    verbose_name='Complétude du dossier'
  )
  critere_docsvalides = models.IntegerField(
    blank=True,
    null=True,
    default=0,
    verbose_name='Validité des documents'
  )
  critere_finalite = models.IntegerField(
    blank=True,
    null=True,
    default=0,
    verbose_name='Principe de la finalité'
  )
  critere_transparence = models.IntegerField(
    blank=True,
    null=True,
    default=0,
    verbose_name='Principe de la transparence'
  )
  observations = models.TextField(
    blank=True,
    null=True,
    # max_length=1000,
  )
  prescriptions = models.TextField(
    blank=True,
    null=True,
    # max_length=1000,
  )
  avis_juridique = models.BooleanField(
    default=False,
    verbose_name='Aspects juridiques OK ?',
    help_text='Cocher pour autoriser le traitement'
  )
  avis_technique = models.BooleanField(
    default=False,
    verbose_name='Aspects techniques OK ? ',
    help_text='Cocher pour autoriser le traitement'
  )
  

  class Meta:
      verbose_name = 'Analyse de la demande'
      verbose_name_plural = 'Analyses des demandes'

  def __str__(self):
    return f"Analyse de : {self.demande}"
    """