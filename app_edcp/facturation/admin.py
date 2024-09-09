from django.contrib import admin
from facturation import models

# Register your models here.

@admin.register(models.Facture)
class FactureAdmin(admin.ModelAdmin):
    """ Factures émises """
    ordering = ['id']
    list_display = ['id', 'created_at', 'created_by', 'demande', 'montant', 'statut', 'is_paid']


@admin.register(models.Paiement)
class PaiementAdmin(admin.ModelAdmin):
    """ Paiements effectués """
    ordering = ['id']
    list_display = ['created_at', 'created_by', 'facture', 'montant', 'mode_paiement', 'is_valid',]



@admin.register(models.ModePaiement)
class ModePaiementAdmin(admin.ModelAdmin):
    """ Personnes concernées """
    ordering = ['id']
    list_display = ['label', 'description', 'is_sensible', 'ordre']