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




@admin.register(models.DesignationDpoMoral)
class DesignationDpoMoralAdmin(admin.ModelAdmin):
    """Correspondant"""
    ordering = ['-created_at']  # Ordonne les correspondants par ID
    list_display = ['organisation', 'cabinet', 'created_at', 'created_by', 'is_active', 'is_approved', 'is_rejected']
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



@admin.register(models.AgrementDCP)
class AgrementDCPAdmin(admin.ModelAdmin):
  """Agrements DCP"""
  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['label', 'description']  # Affiche informatons de la table



@admin.register(models.CabinetDPO)
class CabinetDPOAdmin(admin.ModelAdmin):
  """Cabinets personnes morales"""
  ordering = ['-created_at']  # Ordonne les notifications par ID
  list_display = ['raisonsociale', 'created_at', 'representant', 'rccm', 'telephone', 'email_contact', 'ville' ]
