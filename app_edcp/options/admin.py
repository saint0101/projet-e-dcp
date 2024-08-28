from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
  """ Status des demandes """
  ordering = ['id']
  list_display = ['label', 'description', 'is_sensible', 'ordre']


@admin.register(models.GroupName)
class GroupNameAdmin(admin.ModelAdmin):
  """ Noms de groupes d'utilisateurs """
  ordering = ['id']
  list_display = ['label', 'description', 'is_sensible', 'ordre']


@admin.register(models.TypeClient)
class TypeClientAdmin(admin.ModelAdmin):
  """ definir la page de l'administrateur """

  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['label', 'description', 'sensible', 'ordre']  # Affiche informatons de la table


@admin.register(models.TypePiece)
class TypePieceAdmin(admin.ModelAdmin):
  """ definir la page de gestion des types de pièces pour l'administrateur """

  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['label', 'description', 'sensible', 'ordre']  # Affiche informatons de la table


@admin.register(models.Secteur)
class SecteurAdmin(admin.ModelAdmin):
  """ definir la page de l'administrateur """

  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['label', 'sensible', 'ordre']  # Affiche informatons de la table


@admin.register(models.Pays)
class PaysAdmin(admin.ModelAdmin):
  """ definir la page de l'administrateur """

  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['label']  # Affiche informatons de la table