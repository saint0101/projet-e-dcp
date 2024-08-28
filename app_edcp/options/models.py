from django.db import models

# Create your models here.

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


class Status(OptionModel):
  """ Statut de demande d'autorisation """
  class Meta:
    verbose_name = 'Statut de demande ou d\'analyse'
    verbose_name_plural = 'Statuts de demandes ou d\'analyses'


class GroupName(OptionModel):
  class Meta:
    verbose_name = 'Nom de groupe d\'utilisateurs'
    verbose_name_plural = 'Noms de groupes d\'utilisateurs'



class TypeClient(models.Model):
    """ Table du type des clients """
    label = models.CharField(max_length=100, verbose_name='Type de Client')
    description = models.CharField(max_length=100, null=True, verbose_name='Description du Type de Client', blank=True)
    sensible = models.BooleanField(null=True, verbose_name='Est Sensible', default=False)
    ordre = models.IntegerField(null=True, verbose_name='Ordre d\'Affichage', default=0)

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Type Client'
        verbose_name_plural = 'Types Clients'

    def __str__(self):
        """ les champs a retourner """
        return self.label


class TypePiece(models.Model):
    """ Table du type de pièces d'identité """
    label = models.CharField(max_length=100, verbose_name='Type de pièce d\'identité')
    description = models.CharField(max_length=100, null=True, verbose_name='Description du Type de pièce', blank=True)
    sensible = models.BooleanField(null=True, verbose_name='Est Sensible', default=False)
    ordre = models.IntegerField(null=True, verbose_name='Ordre d\'affichage', default=0)

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Type de pièce'
        verbose_name_plural = 'Types de pièces'

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

