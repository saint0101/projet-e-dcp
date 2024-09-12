from django.db import models
from django.core.validators import FileExtensionValidator

from base_edcp import validators
from base_edcp.models import User
from demande.models import Demande
from options.models import OptionModel, Status


# Create your models here.
class Facture(models.Model):
  created_by = models.ForeignKey(
    User, 
    on_delete=models.PROTECT, 
    null=True,
    blank=True,
    verbose_name="Créateur de la facture",
    related_name='facture_created'
  )
  created_at = models.DateTimeField(
    auto_now_add=True, 
    verbose_name='Date d\'émission'
  )
  demande = models.ForeignKey(
    Demande, 
    on_delete=models.PROTECT, 
    verbose_name='Demande facturée'
  )
  montant = models.BigIntegerField(
    default=0,
    verbose_name='Montant de la facture'
  )
  restant = models.BigIntegerField(
    default=0,
    verbose_name='Reste à payer'
  )
  statut = models.ForeignKey(
    Status,
    on_delete=models.PROTECT,
    blank=True,
    null=True,
    verbose_name='Statut de la facture',
  )
  is_paid = models.BooleanField(
    default=False,
    verbose_name='Est payée'
  )

  def calcul_montant(self):
    if self.demande.categorie.label == 'demande_autorisation':
      self.montant = self.demande.categorie.montant
      self.restant = self.montant
      print('montant ', self.montant)
      self.save(update_fields=['montant'])

  def get_montant_cfa(self):
    montant_formate = f"{self.montant:,}".replace(',', ' ')
    return montant_formate + ' CFA'
  

  def get_num_facture(self):
    return f'{str(self.id):>04}-{self.demande.id}'

  def __str__(self):
    # montant_formate = format(self.montant, ',').replace(',', ' ')
    montant_formate = f"{self.montant:,}".replace(',', ' ')
    return f'Facture N° {str(self.id):>04}-{self.demande.id}'
    


class Paiement(models.Model):
  created_by = models.ForeignKey(
    User, 
    on_delete=models.PROTECT, 
    null=True,
    blank=True,
    verbose_name="Utilisateur effectuant le paiement",
    related_name='paiement_created'
  )
  created_at = models.DateTimeField(
    auto_now_add=True, 
    verbose_name='Date de paiement'
  )
  facture = models.ForeignKey(
    Facture, 
    on_delete=models.PROTECT, 
    verbose_name='Facture'
  )
  montant = models.BigIntegerField(
    default=0,
    verbose_name='Montant du paiement'
  )
  mode_paiement = models.ForeignKey(
    'ModePaiement', 
    blank=True,
    on_delete=models.PROTECT, 
    verbose_name='Mode de paiement'
  )
  is_valid = models.BooleanField(
    default=False,
    verbose_name='Est valide'
  )
  file_justificatif = models.FileField(
    null=True,
    blank=True,
    upload_to='docs/facturation',
    verbose_name='Justificatif de paiement',
    validators=[validators.validate_files, FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
    help_text='Formats acceptés images et documents PDF : jpg, jpeg, png, pdf. Taille limite: 8 Mb.'
  )

  def get_montant_cfa(self):
    montant_formate = f"{self.montant:,}".replace(',', ' ')
    return montant_formate + ' CFA'



class ModePaiement(OptionModel):
  """ Mode de paiement """

  class Meta:
    verbose_name = 'Mode de paiement'
    verbose_name_plural = 'Modes de paiement'
