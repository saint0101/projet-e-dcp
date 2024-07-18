from django.contrib import admin
from django.conf import settings

# Register your models here.
from base_edcp import models



# module TypeClient
class TypeClientAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['label', 'description', 'sensible', 'ordre']  # Affiche informatons de la table

    # Éditer le type du client
    fieldsets = (
        (None, {
            'fields': ('label', 'description', 'sensible', 'ordre')
        }),
    )


# module Secteur
class SecteurAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['label', 'sensible', 'ordre']  # Affiche informatons de la table

    # Éditer le type du client
    fieldsets = (
        (None, {
            'fields': ('label', 'sensible', 'ordre')
        }),
    )


# module Pays
class PaysAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['label']  # Affiche informatons de la table

    # Éditer le type du client
    fieldsets = (
        (None, {
            'fields': ('label', )
        }),
    )


# module CasExemption
class CasExemptionAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['casexemption']  # Affiche informatons de la table

    # Éditer le champ CasExemptionAdmin
    fieldsets = (
        (None, {
            'fields': ('casexemption', )
        }),
    )


# module CategorieDCP
class CategorieDCPAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['categoriedcp']  # Affiche informatons de la table

    # Éditer le champ CategorieDCPAdmin
    fieldsets = (
        (None, {
            'fields': ('categoriedcp', )
        }),
    )


# module CategorieTrait
class CategorieTraitAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les CategorieTrait par ID
    list_display = ['categorie']  # Affiche informatons de la table

    # Éditer le champ CategorieTraitAdmin
    fieldsets = (
        (None, {
            'fields': ('categorie', )
        }),
    )


# module Fonction
class FonctionAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les fonction par ID
    list_display = ['fonction']  # Affiche informatons de la table

    # Éditer le champ CategorieTraitAdmin
    fieldsets = (
        (None, {
            'fields': ('fonction', )
        }),
    )


# module Finalite
class FinaliteAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les fonction par ID
    list_display = ['label', 'sensible', 'ordre']  # Affiche informatons de la table

    # Éditer le champ FinaliteAdmin
    fieldsets = (
        (None, {
            'fields': ('label', 'sensible', )
        }),
    )


# module FondJuridique
class FondJuridiqueAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les fonction par ID
    list_display = ['label', 'description',]  # Affiche informatons de la table

    # Éditer le champ FinaliteAdmin
    fieldsets = (
        (None, {
            'fields': ('label', 'description', )
        }),
    )


# module notificaton
class NotificationAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['user', 'message', 'created_at', 'is_read']  # Affiche les utilisateurs par user et message

    # Éditer l'utilisateur
    fieldsets = (
        (None, {
            'fields': ('user', 'message', 'is_read')
        }),
    )


# module Enregistrement
class EnregistrementAdmin(admin.ModelAdmin):
    """ Page d'administration pour Enregistrement """

    ordering = ['id']  # Ordonne les enregistrements par ID
    list_display = ['user', 'created_at', 'typeclient', 'raisonsociale', 'representant', 'rccm', 'secteur',
                    'secteur_description', 'presentation', 'telephone', 'email_contact', 'site_web', 'pays',
                    'ville', 'adresse_geo', 'adresse_bp', 'gmaps_link', 'effectif', ]

    fieldsets = (
        (None, {
            'fields': ('user', 'typeclient', 'raisonsociale', 'representant', 'rccm', 'secteur',
                       'secteur_description', 'presentation', 'telephone', 'email_contact', 'site_web', 'pays',
                       'ville', 'adresse_geo', 'adresse_bp', 'gmaps_link', 'effectif',)
        }),
    )

# module Autorisation
class AutorisationAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['enregistrement', 'numero_autorisation', 'created_at']  # Affiche informatons de la table

    # Éditer le type du client
    fieldsets = (
        (None, {
            'fields': ('enregistrement', 'numero_autorisation', )
        }),
    )


# Enregistrer le modèle Autorisation avec l'interface d'administration
admin.site.register(models.Autorisation, AutorisationAdmin)

# Enregistrer le modèle RegistrationAdmin avec l'interface d'administration
admin.site.register(models.Enregistrement, EnregistrementAdmin)

# Enregistrer le modèle CustomUser avec l'interface d'administration
admin.site.register(models.Notification, NotificationAdmin)

# Enregistrer le modèle SecteurAdmin avec l'interface d'administration
admin.site.register(models.Secteur, SecteurAdmin)

# Enregistrer le modèle TypeClientAdmin avec l'interface d'administration
admin.site.register(models.TypeClient, TypeClientAdmin)

# Enregistrer le modèle PaysAdmin avec l'interface d'administration
admin.site.register(models.Pays, PaysAdmin)

# Enregistrer le modèle CasExemptionAdmin avec l'interface d'administration
admin.site.register(models.CasExemption, CasExemptionAdmin)

# Enregistrer le modèle CategorieDCPAdmin avec l'interface d'administration
admin.site.register(models.CategorieDCP, CategorieDCPAdmin)

# Enregistrer le modèle CategorieTraitAdmin avec l'interface d'administration
admin.site.register(models.CategorieTrait, CategorieTraitAdmin)

# Enregistrer le modèle FonctionAdmin avec l'interface d'administration
admin.site.register(models.Fonction, FonctionAdmin)

# Enregistrer le modèle FinaliteAdmin avec l'interface d'administration
admin.site.register(models.Finalite, FinaliteAdmin)

# Enregistrer le modèle FondJuridiqueAdmin avec l'interface d'administration
admin.site.register(models.FondJuridique, FondJuridiqueAdmin)


# Modifiez le titre de la page d'administration
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'Django administration')
# Modifiez le titre affiché en haut de chaque page d'administration
admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'Django administration')
# Modifiez le texte affiché en haut de l'index du site d'administration
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'Site administration')
