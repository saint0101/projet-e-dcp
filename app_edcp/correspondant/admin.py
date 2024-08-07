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
    readonly_fields = ('created_at',)  # Le champ 'created_at' est en lecture seule

    # Configuration des champs dans le formulaire d'édition
    """ fieldsets = (
        (None, {
            'fields': ('user', 'organisation', 'created_at', 'created_by', 'type_dpo', 'is_active', 'is_approved')
        }),
        ('Informations complémentaires', {
            'fields': ('qualifications', 'exercice_activite', 'moyens_materiels', 'moyens_humains', 'experiences'),
            'classes': ('collapse',),  # Ajoute un accordéon pour les informations complémentaires
        }),
    ) """
    
    """ def has_add_permission(self, request):
        # Optionnel : empêcher l'ajout de nouveaux correspondants via l'admin
        return False

    def has_change_permission(self, request, obj=None):
        # Optionnel : personnaliser les permissions de modification
        if obj is not None and obj.created_by != request.user:
            return False
        return super().has_change_permission(request, obj) """


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

  # Éditer le type du client
  fieldsets = (
      (None, {
          'fields': ('label', 'description')
      }),
  )