from django.db import models
from base_edcp.models import User, Enregistrement


class OptionModel(models.Model):
  """
  Classe abstraite permettant de centraliser les options de liste déroulante.
  Héritée par les modèles finalité, sous-finalité, type de demande etc.
  """
  label = models.CharField(
    unique=True,
    max_length=100,
    verbose_name='Label', 
    help_text='Codification du champ, à écrire sous forme de slug'
  )
  is_sensible = models.BooleanField(
    default=False, 
    verbose_name='Sensible ?'
  )
  description = models.CharField(
    max_length=255, 
    null=True, 
    blank=True,
    verbose_name='Description du champ', 
    help_text='Description du champ, affichée sur les formulaire'
  )
  resume = models.TextField(
    max_length=500,
    null=True,
    blank=True,
    verbose_name='Résumé du champ (texte explicatif)',
    help_text='Paragraphe plus long que la description fournissant des détails sur le champ'
  )
  ordre = models.IntegerField(
    default=0, 
    verbose_name="Ordre d'affichage"
  )

  class Meta:
    abstract = True

  def __str__(self):
    """ les champs à retourner pour l'affichage """
    return self.description

  
  
class TypeDemandeAuto(OptionModel):
  finalites = models.ManyToManyField(
    'Finalite',
    verbose_name='Finalités liées à ce type de demande',
    related_name='types_demande',
  )

  class Meta:
    verbose_name = 'Type de demande'
    verbose_name_plural = 'Types de demande'


class Finalite(OptionModel):
  pass


class SousFinalite(OptionModel):
  finalite = models.ForeignKey(
    'Finalite',
    on_delete=models.CASCADE,
    verbose_name='Finalité',
  )

class ActionDemande(OptionModel):
  class Meta:
    verbose_name = 'Action effectuée'
    verbose_name_plural = 'Actions effectuées'


class PersConcernee(OptionModel):
  class Meta:
    verbose_name = 'Catégorie de personnes concernées'
    verbose_name_plural = 'Catégories de personnes concernées'


class Status(OptionModel):
  class Meta:
    verbose_name = 'Statut de demande'
    verbose_name_plural = 'Statuts de demandes'


def get_default_status():
  default_status = Status.objects.get(label='brouillon')
  return default_status.id


class DemandeAuto(models.Model):
    user = models.ForeignKey(
      User, 
      on_delete=models.CASCADE, 
      blank=True,
      verbose_name="Utilisateur"
    )
    organisation = models.ForeignKey(
      Enregistrement, 
      on_delete=models.CASCADE, 
      verbose_name='Organisation'
    )
    created_at = models.DateTimeField(
      auto_now_add=True, 
      verbose_name='Date de Création'
    )
    status = models.ForeignKey(
      'Status', 
      blank=True,
      on_delete=models.CASCADE, 
      verbose_name='Statut de la demande'
    )
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
      on_delete=models.CASCADE, 
      verbose_name="Type de Demande d'Autorisation"
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



class HistoriqueDemande(models.Model):
  demande = models.ForeignKey(
    'DemandeAuto',
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Demande d\'autorisation'
  )
  status = models.ForeignKey(
    'Status', 
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

  class Meta:
      verbose_name = 'Historique de la demande'
      verbose_name_plural = 'Historiques des demandes'

  def __str__(self):
    return f"{self.action.description}"


