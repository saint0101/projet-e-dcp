from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Demande)
class DemandeAdmin(admin.ModelAdmin):
    """ Demandes effectuées """
    ordering = ['created_at']
    list_display = ['id', 'created_at', 'organisation', 'created_by', 'categorie', 'status']



@admin.register(models.HistoriqueDemande)
class HistoriqueDemandeAdmin(admin.ModelAdmin):
    """ Historiqe """
    ordering = ['created_at']
    list_display = ['id', 'demande', 'status', 'action', 'auteur', 'is_private']


@admin.register(models.AnalyseDemande)
class AnalyseDemandeAdmin(admin.ModelAdmin):
    """ Analyses effectuées """
    ordering = ['created_at']
    list_display = ['created_at', 'created_by', 'status', 'avis_juridique', 'avis_technique']



@admin.register(models.ReponseDemande)
class ReponseDemandeAdmin(admin.ModelAdmin):
    """ Actions effectuées """
    ordering = ['id']
    list_display = ['created_at', 'fichier_reponse', 'signataire', ]


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



@admin.register(models.Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    """ Commentaires sur les demandes """
    ordering = ['-created_at']
    list_display = ['demande', 'created_at', 'auteur', 'objet', 'message', 'is_new']