from django.contrib import admin
from . import models

# Register your models here.



@admin.register(models.ActionDemande)
class ActionDemandeAdmin(admin.ModelAdmin):
    """ Actions effectuées """
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']



@admin.register(models.CategorieDemande)
class CategorieDemandeAdmin(admin.ModelAdmin):
    """ Catégories de demande """
    ordering = ['id']
    list_display = ['label', 'description', 'niv_validation', 'is_sensible', 'ordre']



@admin.register(models.CritereEvaluation)
class CritereEvaluationAdmin(admin.ModelAdmin):
    """ Actions effectuées """
    ordering = ['id']
    list_display = ['categorie_demande', 'label', 'field_name', 'field_type']


# @admin.register(models.HistoriqueDemande)
class HistoriqueAdmin(admin.ModelAdmin):
    """ Historique des demandes """
    ordering = ['id']
    list_display = ['created_at', 'demande', 'status','action', 'auteur']