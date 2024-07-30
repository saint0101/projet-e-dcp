from django.contrib import admin
from django.conf import settings

from .models import Correspondant, TypeDPO, QualificationsDPO, ExerciceActivite

# Register your models here.

class CorrespondantAdmin(admin.ModelAdmin):
  """Correspondant"""
  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['user', 'organisation', 'created_at', 'created_by', 'type_dpo', 'is_active', 'is_approved']  # Affiche informatons de la table

  # Éditer le type du client
  """ fieldsets = (
    (None, {
        'fields': '__all__'
    }),
  ) """


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


class ExerciceActiviteAdmin(admin.ModelAdmin):
  """Mode d'exercice de l'activité"""
  ordering = ['id']  # Ordonne les notifications par ID
  list_display = ['label', 'description']  # Affiche informatons de la table

  # Éditer le type du client
  """ fieldsets = (
      (None, {
          'fields': ('label', 'description')
      }),
  ) """


admin.site.register(Correspondant, CorrespondantAdmin)
admin.site.register(TypeDPO, TypeDPOAdmin)
admin.site.register(QualificationsDPO, QualificationsDPOAdmin)
admin.site.register(ExerciceActivite, ExerciceActiviteAdmin)
