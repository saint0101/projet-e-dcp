from django.db import models
from base_edcp.models import User, Enregistrement


class TypeDPO(models.Model):
  """Type de correspondant"""
  label = models.CharField(max_length=100)
  description = models.CharField(max_length=100, null=True, verbose_name='Description du Type de Correspondant', blank=True)

  class Meta:
      """ définir le nom singulier et pluriel du modèle """
      verbose_name = 'Type de Correspondant'
      verbose_name_plural = 'Types de Correspondant'

  def __str__(self):
      """ les champs à retourner """
      return self.label


class QualificationsDPO(models.Model):
  """Type de correspondant"""
  label = models.CharField(max_length=100)
  description = models.CharField(max_length=100, null=True, verbose_name='Description du Type de Correspondant', blank=True)

  class Meta:
    """ définir le nom singulier et pluriel du modèle """
    verbose_name = 'Qualifications du Correspondant'

  def __str__(self):
    """ les champs à retourner """
    return self.label


class ExerciceActivite(models.Model):
  """Exercice de l'activité"""
  label = models.CharField(max_length=100)
  description = models.CharField(max_length=100, null=True, blank=True)

  class Meta:
    """ définir le nom singulier et pluriel du modèle """
    verbose_name = 'Mode d\'exercice de l\'activité'
    verbose_name_plural = 'Modes d\'exercice de l\'activité'

  def __str__(self):
      """ les champs à retourner """
      return self.label


class Correspondant(models.Model):
    """
    Correspondant à la protection des données
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Compte utilisateur',
        related_name='correspondant_profiles'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Crée par',
        null=True,
        blank=True,
        related_name='has_created'
    )
    organisation = models.ForeignKey(
        Enregistrement,
        on_delete=models.CASCADE,
        verbose_name='Organisation'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de désignation'
    )
    type_dpo = models.ForeignKey(
        TypeDPO,
        on_delete=models.CASCADE,
        verbose_name='Type de Correspondant',
        null=True,
        blank=True
    )
    qualifications = models.ForeignKey(
        QualificationsDPO,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Qualifications du Correspondant'
    )
    exercice_activite = models.ForeignKey(
        ExerciceActivite,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Exercice de l'activité"
    )
    moyens_materiels = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Moyens matériels mis à la disposition du Correspondant'
    )
    moyens_humains = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Moyens humains mis à la disposition du Correspondant'
    )
    experiences = models.TextField(
        null=True,
        blank=True,
        verbose_name='Experiences et diplômes'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Approuvé'
    )

    file_lettre_designation = models.FileField(
       null=True, 
       blank=True, 
       upload_to='correspondant/docs', 
       verbose_name='Lettre de désignation')
    
    file_lettre_acceptation = models.FileField(
       null=True, 
       blank=True, 
       upload_to='correspondant/docs', 
       verbose_name='Lettre d\'acceptation')
    
    file_attestation_travail = models.FileField(
       null=True, 
       blank=True, 
       upload_to='correspondant/docs', 
       verbose_name='Attestation de travail')
    
    file_casier_judiciaire = models.FileField(
       null=True, 
       blank=True, 
       upload_to='correspondant/docs', 
       verbose_name='Casier judiciaire',
       help_text='datant de moins de 3 mois')
    
    file_certificat_nationalite = models.FileField(
       null=True, 
       blank=True, 
       upload_to='correspondant/docs', 
       verbose_name='Certificat de nationalité')
    
    file_cv = models.FileField(
       null=True, 
       blank=True, 
       upload_to='correspondant/docs', 
       verbose_name='CV')

    class Meta:
        verbose_name = 'Correspondant à la protection des données'
        verbose_name_plural = 'Correspondants à la protection des données'

    def __str__(self):
        return f"{self.user.nom} ({self.user.prenoms})"
