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



@admin.register(models.EchelleNotation)
class EchelleNotationAdmin(admin.ModelAdmin):
    """ Echelle de notation des demandes d'autorisation """
    ordering = ['valeur']
    list_display = ['valeur', 'label', 'description']



@admin.register(models.DemandeAuto)
class DemandeAutoAdmin(admin.ModelAdmin):
    """ Demande d'autorisation """
    ordering = ['id']
    list_display = ['created_at', 'type_demande', 'status','organisation', 'created_by', 'finalite']



@admin.register(models.FondementJuridique)
class FondementJuridiqueAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']


@admin.register(models.ModeRecueilConsent)
class ModeRecueilConsentAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']


@admin.register(models.ModeTransfert)
class ModeTransfertAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']


@admin.register(models.TypeDestinataireTransfert)
class TypeDestinataireTransfertAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']


@admin.register(models.TransfertDonnees)
class TransfertDonneesAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['created_at', 'pays', 'destinataire', 'mode_transfert', 'type_destinataire']


@admin.register(models.CategorieDonnees)
class CategorieDonneesAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']


@admin.register(models.TypeDonnees)
class TypeDonneesAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['label', 'categorie_donnees', 'description', 'is_sensible', 'ordre']


@admin.register(models.ModeInterconnexion)
class ModeInterconnexionAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']


@admin.register(models.InterConnexion)
class InterconnexionAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['created_at', 'destinataire', 'mode_interconnexion',]

# admin.site.unregister(models.Status, StatusAdmin)