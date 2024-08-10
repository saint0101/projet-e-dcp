from django.contrib import admin
from demande_auto import models



@admin.register(models.TypeDemandeAuto)
class TypeDemandeAdmin(admin.ModelAdmin):
    """ Types de demande d'autorisation """
    ordering = ['ordre']  # Ordonne les correspondants par ID
    list_display = ['label', 'description', 'is_sensible', 'ordre']


@admin.register(models.Finalite)
class FinaliteAdmin(admin.ModelAdmin):
    """ Finalités de traitement """
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']


@admin.register(models.SousFinalite)
class SousFinaliteAdmin(admin.ModelAdmin):
    """ Sous-finalités de traitement """
    ordering = ['id']
    list_display = ['finalite','label', 'description', 'is_sensible', 'ordre']



@admin.register(models.PersConcernee)
class PersConcerneeAdmin(admin.ModelAdmin):
    """ Personnes concernées """
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']



@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    """ Status des demandes """
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']


# admin.site.unregister(models.Status, StatusAdmin)