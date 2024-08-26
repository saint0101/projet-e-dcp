from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from base_edcp.models import User, Enregistrement
from options.models import OptionModel, Status
from base_edcp import validators
from django.core.validators import FileExtensionValidator


# Create your models here.
class Demande(models.Model):
  """ Modèle parent des demandes (autorisations, désignation DPO, etc.) """

  created_by = models.ForeignKey(
    User, 
    on_delete=models.CASCADE, 
    blank=True,
    verbose_name="Utilisateur effectuant la demande",
    related_name='demande_created'
  )
  updated_by = models.ForeignKey(
    User, 
    on_delete=models.CASCADE, 
    null=True,
    blank=True,
    verbose_name="Utilisateur ayant effectué la dernière mises à jour.",
    related_name='demande_updated'
  )
  created_at = models.DateTimeField(
    auto_now_add=True, 
    verbose_name='Date de Création'
  )
  updated_at = models.DateTimeField(
    null=True,
    blank=True,
    auto_now_add=True, 
    verbose_name='Date de mise à jour',
  )
  organisation = models.ForeignKey(
    Enregistrement, 
    on_delete=models.CASCADE, 
    verbose_name='Organisation',
    blank=True,
  )
  num_demande = models.CharField(
    max_length=100,
    null=True,
    blank=True,
    verbose_name='Numéro de la demande',
  )
  status = models.ForeignKey(
    Status, 
    null=True,
    blank=True,
    on_delete=models.CASCADE, 
    verbose_name='Statut de la demande'
  )
  categorie = models.ForeignKey(
    'CategorieDemande', 
    null=True,
    blank=True,
    on_delete=models.CASCADE, 
    verbose_name='Categorie de la demande'
  )
  analyse = models.ForeignKey(
    'AnalyseDemande',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    verbose_name='Analyse de la demande'
  )
  finished_at = models.DateTimeField(
    null=True,
    blank=True,
    verbose_name='Date de fin de traitement.'
  )
  is_locked = models.BooleanField(
    default=False,
    verbose_name='Est verrouillée (en cours de validation)'
  )

  class Meta:
    verbose_name = 'Demande générale'
    verbose_name_plural = 'Demandes générales'

  def save_historique(self, action_label, user, status=None, is_private=False):
    """
    Sauvegarde de l'historique d'une demande.
    Paramètres :
    -- demande - l'objet demande d'autorisation concerné
    -- action_label - le label de l'action effectuee
    -- user - l'utilisateur à l'origine de l'action
    """
    action, created = ActionDemande.objects.get_or_create(label=action_label)
    historique = HistoriqueDemande()
    historique.demande = self
    historique.status = status if status else self.status
    historique.action = action
    historique.auteur = user
    historique.is_private = is_private
    historique.save()

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if not self.num_demande:
      date_demande = self.created_at if self.created_at else datetime.now()
      #f'{str(i):<5}'
      self.num_demande = f'{date_demande.year}{date_demande.month:>02}{date_demande.day:>02}-{str(self.id):>06}'
      print('num_demande : ', self.num_demande)
    super().save(update_fields=['num_demande'])

  def __str__(self):
    return f"{self.categorie} #{self.pk}"


""" @receiver(pre_save, sender=Demande)
def create_num_demande(sender, instance, **kwargs):
    # Modify the instance's fields before saving
    if not instance.num_demande:
      date_demande = instance.created_at
      #f'{str(i):<5}'
      instance.num_demande = f'{date_demande.year}{date_demande.month}{date_demande.day}-{str(instance.id):>06}'
      print('num_demande : ', instance.num_demande) """


class CategorieDemande(OptionModel):
  """ Categorie de demande """
  niv_validation = models.IntegerField(
    default=1,
    verbose_name='Niveau de validation'
  )
  intitule_reponse = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    verbose_name='Intitulé de la réponse pour ce type de demande'
  )

  class Meta:
    verbose_name = 'Categorie de demande'
    verbose_name_plural = 'Categories de demandes'


class CritereEvaluation(models.Model):
  """ Critère d'évaluation d'une demande. Représente des champs de formulaire à affcher pour constituer une grille d'évaluation. """
  FIELD_TYPES = [
    ('text', 'Champ de texte'), 
    ('number', 'Valeur numérique'), 
    ('select', 'Liste déroulante'),
    ('checkbox', 'Case à cocher'),
    ('textarea', 'Zone de texte'),
  ]

  NOTATIONS = [
    (0, 'Insatisfaisant'),
    (5, 'Partiellement satisfaisant'),
    (10, 'Satisfaisant'),
  ]
  
  categorie_demande = models.ForeignKey(
    'CategorieDemande', 
    null=True,
    blank=True,
    on_delete=models.CASCADE, 
    verbose_name='Categorie de demande pour laquelle ce critère d\'evaluation est applicable'
  )
  label = models.CharField(
    null=True,
    max_length=255, 
    verbose_name="Identifiant du champ",
    help_text="Doit être indiqué sous forme de slug (pas de caractère speciaux et des espaces au lieu des tirets)"
  )
  field_name = models.CharField(
    max_length=255,
    verbose_name="Nom du champ à afficher sur le formulaire d'évaluation"
  )
  field_type = models.CharField(
    max_length=255,
    verbose_name="Type du champ",
    choices=FIELD_TYPES,
    default='select'
  )
  field_required = models.BooleanField(
    default=True,
    verbose_name="Champ obligatoire"
  )

  def __str__(self):
    return self.label
  


class AnalyseDemande(models.Model):
  """ Analyse d'une demande """
  created_by = models.ForeignKey(
    User, 
    on_delete=models.CASCADE, 
    blank=True,
    verbose_name="Agent en charge de la demande",
    related_name='analyse_created',
  )
  created_at = models.DateTimeField(
    auto_now_add=True, 
    verbose_name='Date de Création'
  )
  updated_by = models.ForeignKey(
    User, 
    on_delete=models.CASCADE, 
    null=True,
    blank=True,
    verbose_name="Agent auteur de la dernière mise à jour de l'analyse",
    related_name='analyse_updated',
  )
  updated_at = models.DateTimeField(
    auto_now_add=True, 
    verbose_name='Date de Création'
  )
  status = models.ForeignKey(
    Status, 
    null=True,
    blank=True,
    on_delete=models.CASCADE, 
    verbose_name='Statut de la demande'
  )
  evaluation = models.TextField(
    null=True,
    blank=True,
    verbose_name="Evaluation de la demande",
    help_text="Contenu de l'évaluation selon les critères définis et sous forme sérialisée."
  )
  observations = models.TextField(
    null=True,
    blank=True,
    verbose_name="Observations sur la demande",
  )
  prescriptions = models.TextField(
    null=True,
    blank=True,
    verbose_name="Prescriptions et recommandations",
  )
  avis_juridique = models.BooleanField(
    default=False,
    verbose_name="Avis juridique (autoriser ou non)"
  )
  avis_technique = models.BooleanField(
    default=False,
    verbose_name="Avis technique (autoriser ou non)"
  )
  projet_reponse = models.ForeignKey(
    'ReponseDemande',
    null=True,
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Réponse apportée à la demande'
  )
  niv_validation = models.IntegerField(
    default=0,
    verbose_name='Niveau de validation actuel de l\'analyse'
  )
  validations = models.ManyToManyField(
    'ValidationDemande',
    blank=True,
    verbose_name='Liste des validations',
  )
  validation_niv1 = models.ForeignKey(
    'ValidationDemande',
    null=True,
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Validation de la demande - niveau 1',
    related_name='analyse_validate_niv1',
  )
  validation_niv2 = models.ForeignKey(
    'ValidationDemande',
    null=True,
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Validation de la demande - niveau 2',
    related_name='analyse_validate_niv2',
  )
  validation_niv3 = models.ForeignKey(
    'ValidationDemande',
    null=True,
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Validation de la demande - niveau 3',
    related_name='analyse_validate_niv3',
  )
  validation_niv4 = models.ForeignKey(
    'ValidationDemande',
    null=True,
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Validation de la demande - niveau 4',
    related_name='analyse_validate_niv4',
  )
  validation_niv5 = models.ForeignKey(
    'ValidationDemande',
    null=True,
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Validation de la demande - niveau 5',
    related_name='analyse_validate_niv5',
  )
  is_locked = models.BooleanField(
    default=False,
    verbose_name='Est verrouillée (en cours de validation)'
  )
  is_closed= models.BooleanField(
    default=False,
    verbose_name='Est terminée'
  )

  class Meta:
    verbose_name = 'Analyse d\'une demande'
    verbose_name_plural = 'Analyses des demandes'
    permissions = [
      ('can_validate_niv_1', 'Peut valider la demande - niveau 1'),
      ('can_validate_niv_2', 'Peut valider la demande - niveau 2'),
      ('can_validate_niv_3', 'Peut valider la demande - niveau 3'),
      ('can_validate_niv_4', 'Peut valider la demande - niveau 4'),
      ('can_validate_niv_5', 'Peut valider la demande - niveau 5'),
    ]


class ReponseDemande(models.Model):
  signataire = models.ForeignKey(
    User, 
    on_delete=models.CASCADE, 
    null=True,
    blank=True,
    verbose_name="Validateur signant la réponse"
  )
  created_at = models.DateTimeField(
    auto_now_add=True, 
    verbose_name='Date de signature'
  )
  intitule = models.CharField(
    max_length=255,
    null=True,
    blank=True,
    verbose_name="Intitulé de la réponse",
  )
  num_autorisation = models.CharField(
    max_length=100,
    null=True,
    blank=True,
    verbose_name='Numéro de la demande',
  )  
  fichier_reponse = models.FileField(
    null=True, 
    blank=True, 
    upload_to='docs/reponses', 
    verbose_name='Fichier de la réponse', 
    validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
    help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.'
  )


class ValidationDemande(models.Model):
  created_at = models.DateTimeField(
    auto_now_add=True, 
    verbose_name='Date de signature'
  )
  created_by = models.ForeignKey(
    User, 
    on_delete=models.CASCADE, 
    null=True,
    blank=True,
    verbose_name="Agent effectuant la validation"
  )
  niveau_validation = models.IntegerField(
    default=1,
    verbose_name="Niveau de validation effectué"
  )
  avis = models.BooleanField(
    blank=True,
    null=True,
    verbose_name='Avis sur l\'analsye et le projet de réponse'
  )
  observations = models.TextField(
    null=True,
    blank=True,
    verbose_name="Observations sur l'analyse ou le projet de réponse"
  )


class HistoriqueDemande(models.Model):
  """ Historique des actions effectuées dans le traitement d'une demande """
  demande = models.ForeignKey(
    'Demande',
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Demande'
  )
  status = models.ForeignKey(
    Status, 
    blank=True,
    null=True,
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


class ActionDemande(OptionModel):
  """ Action effectuée sur une demande d'autorisation. Utilisée pour l'historique des traitements """
  class Meta:
    verbose_name = 'Action effectuée'
    verbose_name_plural = 'Actions effectuées'


class Commentaire(models.Model):
  """ Commentaires sur une demande"""
  demande = models.ForeignKey(
    'Demande',
    blank=True,
    on_delete=models.CASCADE,
    verbose_name='Demande d\'autorisation'
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
  objet = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    verbose_name='Objet du message'
  )
  message = models.TextField(
    null=True,
    blank=True,
    max_length=500,
    verbose_name='Contenu du message'
  )

  class Meta:
      verbose_name = 'Commentaire sur une demande'
      verbose_name_plural = 'Commentaires sur des demandes'

  def __str__(self):
    return f"{self.objet}"
  
