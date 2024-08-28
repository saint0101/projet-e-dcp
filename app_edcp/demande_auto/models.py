from django.db import models
from base_edcp.models import User, Enregistrement
from options.models import OptionModel
from demande.models import Demande, Status



  
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
    
    class Meta:
      verbose_name = 'Demande d\'autorisation'
      verbose_name_plural = 'Demandes d\'autorisation'

    def __str__(self):
      return f"{self.type_demande} #{self.pk}"
    

class DemandeAutoTraitement(DemandeAuto):
  """ Sous-classe de demande d'autorisation pour les traitements """
  fondement_juridique = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    verbose_name='Fondement Juridique'
  )
  procedures = models.TextField(
    null=True,
    blank=True,
    max_length=500,
    verbose_name='Procédures'
  )
  mesures_securite = models.TextField(
    null=True,
    blank=True,
    max_length=500,
    verbose_name='Mesures de Securité'
  )
  @classmethod
  def get_type_demande(cls):
    return TypeDemandeAuto.objects.get(label='traitement')


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