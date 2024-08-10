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
    sous_finalites = models.ForeignKey(
      'SousFinalite', 
      null=True,
      blank=True,
      on_delete=models.CASCADE, 
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
      return f"{self.type_demande} - {self.user.username}"
    

class DemandeAutoTraitement(DemandeAuto):
  @classmethod
  def get_type_demande(cls):
    return TypeDemandeAuto.objects.get(label='traitement')


class DemandeAutoTransfert(DemandeAuto):
  destination = models.CharField(
    null=True,
    blank=True,
    max_length=255,
  )
  @classmethod
  def get_type_demande(cls):
    return TypeDemandeAuto.objects.get(label='transfert')


class DemandeAutoVideo(DemandeAuto):
  @classmethod
  def get_type_demande(cls):
    return TypeDemandeAuto.objects.get(label='videosurveillance')
  

class DemandeAutoBiometrie(DemandeAuto):
  @classmethod
  def get_type_demande(cls):
    return TypeDemandeAuto.objects.get(label='biometrie')

