from django.db import models
from django.core.validators import FileExtensionValidator
from base_edcp.models import User, Enregistrement
from demande.models import Demande
from options.models import OptionModel
from base_edcp import validators


class TypeDPO(OptionModel):
  """Type de correspondant"""
  # label = models.CharField(max_length=100)
  # description = models.CharField(max_length=100, null=True, verbose_name='Description du Type de Correspondant', blank=True)

  class Meta:
      verbose_name = 'Type de Correspondant'
      verbose_name_plural = 'Types de Correspondant'

  """ def __str__(self):
      return self.label """


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


class MoyensDPO(OptionModel):
  """ Moyens matériels et humains """
  class Meta:
    verbose_name = 'Moyens du DPO'
    verbose_name_plural = 'Moyens du DPO'


class AgrementDCP(OptionModel):
  """ agrement DCP """
  class Meta:
    verbose_name = 'Agrement DCP'
    verbose_name_plural = 'Agrements DCP'


class CabinetDPO(Enregistrement):
    agrements_dcp = models.ManyToManyField(
       AgrementDCP,
       blank=True,
    )

    class Meta:
        verbose_name = 'Correspondant personne morale'
        verbose_name_plural = 'Correspondants personnes morales'


class Correspondant(Demande):
    """
    Correspondant à la protection des données
    """
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Compte utilisateur',
        related_name='correspondant_profiles'
    )
    cabinet = models.ForeignKey(
        CabinetDPO,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Cabinet désigné',
        related_name='designations_correspondants'
    )
    """ created_by = models.ForeignKey(
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
        verbose_name='Organisation',
        related_name='correspondants'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de désignation'
    ) """
    type_dpo = models.ForeignKey(
        TypeDPO,
        on_delete=models.PROTECT,
        verbose_name='Type de Correspondant',
        null=True,
        blank=True
    )
    is_personne_morale = models.BooleanField(
        default=False,
        verbose_name='Est une personne morale (cabinet)'
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
    """ moyens_materiels = models.CharField(
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
    ) """
    moyens_dpo = models.ManyToManyField(
        MoyensDPO,
        blank=True,
        verbose_name='Moyens humains et matériels',
        help_text='Moyens mis à la disposition du Correspondant.'
    )
    experiences = models.TextField(
        null=True,
        blank=True,
        verbose_name='Experiences et diplômes'
    )
    profile_completed = models.BooleanField(
        default=False,
        verbose_name='Profil complet'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Approuvé'
    )
    is_rejected = models.BooleanField(
        default=False,
        verbose_name='Refusé'
    )
    commentaires = models.TextField(
       blank=True,
       null=True,
    )
    file_lettre_designation = models.FileField(
       null=True, 
       blank=True, 
       upload_to='docs/correspondant', 
       validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
       help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.',
       verbose_name='Lettre de désignation')
    
    file_lettre_acceptation = models.FileField(
       null=True, 
       blank=True, 
       upload_to='docs/correspondant', 
       validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
       help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.',
       verbose_name='Lettre d\'acceptation')
    
    file_attestation_travail = models.FileField(
       null=True, 
       blank=True, 
       upload_to='docs/correspondant', 
       validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
       help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.',
       verbose_name='Attestation de travail')
    
    file_casier_judiciaire = models.FileField(
       null=True, 
       blank=True, 
       upload_to='docs/correspondant', 
       verbose_name='Casier judiciaire',
       validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
       help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.')
    
    file_certificat_nationalite = models.FileField(
       null=True, 
       blank=True, 
       upload_to='docs/correspondant', 
       validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
       help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.',
       verbose_name='Certificat de nationalité')
    
    file_cv = models.FileField(
       null=True, 
       blank=True, 
       upload_to='docs/correspondant', 
       validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
       help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.',
       verbose_name='CV')
    
    file_contrat = models.FileField(
       null=True, 
       blank=True, 
       upload_to='docs/correspondant', 
       validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
       help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.',
       verbose_name='Contrat',
    )

    class Meta:
        verbose_name = 'Correspondant à la protection des données'
        verbose_name_plural = 'Correspondants à la protection des données'

    def __str__(self):
        if self.is_personne_morale:
           return f"{self.cabinet}"
        else:
            return f"{self.user.nom} {self.user.prenoms}"
    



class DesignationDpoMoral(Demande):
    cabinet = models.ForeignKey(
        CabinetDPO,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    commentaires = models.TextField(
       blank=True,
       null=True,
    )
    file_contrat = models.FileField(
       null=True, 
       blank=True, 
       upload_to='docs/correspondant', 
       validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
       help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.',
       verbose_name='Contrat',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Est actif'
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Approuvé'
    )
    is_rejected = models.BooleanField(
        default=False,
        verbose_name='Refusé'
    )

    class Meta:
        verbose_name = 'Désignation de DPO personne morale'
        verbose_name_plural = 'Désignations de DPO personnes morales'

