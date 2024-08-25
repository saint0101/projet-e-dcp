from django.contrib import admin
from django.conf import settings

from correspondant import models

# Register your models here.

@admin.register(models.Correspondant)
class CorrespondantAdmin(admin.ModelAdmin):
    """Correspondant"""
    ordering = ['id']  # Ordonne les correspondants par ID
    list_display = ['user', 'organisation', 'created_at', 'created_by', 'type_dpo', 'is_active', 'is_approved']
    # search_fields = ['user__nom', 'user__prenoms', 'organisation__nom']  # Ajoute un champ de recherche
    # list_filter = ['is_active', 'is_approved', 'type_dpo', 'organisation']  # Ajoute des filtres
   



@admin.register(models.TypeDPO)
class TypeDPOAdmin(admin.ModelAdmin):
  """Type de correspondant"""
  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['label', 'description']  # Affiche informatons de la table

  # Éditer le type du client
  """ fieldsets = (
      (None, {
          'fields': ('label', 'description')
      }),
  ) """

@admin.register(models.QualificationsDPO)
class QualificationsDPOAdmin(admin.ModelAdmin):
  """Qualifications du correspondant"""
  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['label', 'description']  # Affiche informatons de la table

  # Éditer le type du client
  """ fieldsets = (
      (None, {
          'fields': ('label', 'description')
      }),
  ) """

@admin.register(models.ExerciceActivite)
class ExerciceActiviteAdmin(admin.ModelAdmin):
  """Mode d'exercice de l'activité"""
  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['label', 'description']  # Affiche informatons de la table


@admin.register(models.MoyensDPO)
class MoyensDPOAdmin(admin.ModelAdmin):
  """Moyens du DPO"""
  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['label', 'description']  # Affiche informatons de la table
