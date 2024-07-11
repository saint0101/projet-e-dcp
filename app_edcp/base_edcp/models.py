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
        verbose_name_plural = 'Type Clients'

    def __str__(self):
        """ les champs a retourner """
        return self.label


class Secteur(models.Model):
    """ Table secteur d'activité """
    label = models.CharField(max_length=100, verbose_name='Secteur d\'Activité')
    sensible = models.BooleanField(verbose_name='Est Sensible')
    ordre = models.IntegerField(verbose_name='Ordre d\'Affichage')

    class Meta:
        """ définir le nom singulier et pluriel du modèle """
        verbose_name = 'Secteur'
        verbose_name_plural = 'Secteurs'

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


class Fonction(models.Model):
    """ Table Fonction """
    fonction = models.CharField(max_length=100)

    def __str__(self):
        """ les champs a retourner """
        return self.fonction


class FondJuridique(models.Model):
    """ Table Fond juridique """
    label = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        """ les champs a retourner """
        return self.label