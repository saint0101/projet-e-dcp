from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

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


# modeule enregistreprement d'un utilisateur
class UserAdmin(BaseUserAdmin):
    """
    Définit les pages d'administration pour les utilisateurs.
    """
    ordering = ['id']  # Ordonne les utilisateurs par ID
    list_display = ['email', 'login', 'organisation', 'consentement']  # Affiche les utilisateurs par e-mail et login

    # Éditer l'utilisateur
    fieldsets = (
        (None, {'fields': ('email', "password")}),  # Informations de connexion
        (
            _('Personal Info'),  # Titre pour les champs d'informations personnelles
            {
                'fields': (
                    'nom',
                    'prenoms',
                    'organisation',
                    'telephone',
                    'fonction',
                    'consentement',
                    'login',
                    'avatar',
                )
            }
        ),
        (
            _('Permissions'),  # Titre pour les champs de permission
            {
                'fields': (
                    'is_active',    # Active ou désactive le compte
                    'is_staff',     # Accorde l'accès au site d'administration
                    'is_superuser', # Accorde tous les accès
                )
            }
        ),
        (_('Dates importantes'), {'fields': ('last_login',)}),  # Date de dernière connexion
    )
    readonly_fields = ['last_login']  # Affiche la dernière connexion en lecture seule

    # Ajout d'un utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'nom',
                'prenoms',
                'organisation',
                'telephone',
                'fonction',
                'consentement',
                'login',
                'avatar',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


class SousFinaliteAdmin(admin.ModelAdmin):
    """ Definir la table sous finalite dans l'espace admin """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['label', 'sensible', 'ordre', 'finalite']  # Affiche informatons de la table

    # Éditer le type des sous finalite
    fieldsets = (
        (None, {
            'fields': ('label', 'sensible', 'ordre', 'finalite')
        }),
    )


class RoleAdmin(admin.ModelAdmin):
    """ Definir la table Role dans l'espace admin """

    ordering = ['id']  # Ordonne les Role par ID
    list_display = ['role']  # Affiche informatons de la table

    # Éditer le type des sous finalite
    fieldsets = (
        (None, {
            'fields': ('role', ) # Utilisez un tuple même pour un seul champ
        }),
    )


class PersConcerneeAdmin(admin.ModelAdmin):
    """ Definir la table Role dans l'espace admin """

    ordering = ['id']  # Ordonne les personne concernee par ID
    list_display = ['label', 'sensible', 'ordre']  # Affiche informatons de la table

    # Éditer le type des personne concernee
    fieldsets = (
        (None, {
            'fields': ('label', 'sensible', 'ordre') # Utilisez un tuple même pour un seul champ
        }),
    )


class HabilitationAdmin(admin.ModelAdmin):
    """ Definir la table Habilitation dans l'espace admin """

    ordering = ['id']  # Ordonne les Habilitation par ID
    list_display = ['role', 'fonction', 'created']  # Affiche informatons de la table

    # Éditer le type des Habilitation
    fieldsets = (
        (None, {
            'fields': ('role', 'fonction', 'created') # Utilisez un tuple même pour un seul champ
        }),
    )


class JournalTransactionAdmin(admin.ModelAdmin):
    """ Definir la table JournalTransaction dans l'espace admin """

    ordering = ['id']  # Ordonne les JournalTransaction par ID
    list_display = ['transaction', 'cible', 'created', 'user']  # Affiche informatons de la table

    # Éditer le type des JournalTransaction
    fieldsets = (
        (None, {
            'fields': ('transaction', 'cible', 'created', 'user') # Utilisez un tuple même pour un seul champ
        }),
    )


# Enregistrer le modèle Habilitation avec l'interface d'administration
admin.site.register(models.JournalTransaction, JournalTransactionAdmin)

# Enregistrer le modèle Habilitation avec l'interface d'administration
admin.site.register(models.Habilitation, HabilitationAdmin)

# Enregistrer le modèle PersConcernee avec l'interface d'administration
admin.site.register(models.PersConcernee, PersConcerneeAdmin)

# Enregistrer le modèle role avec l'interface d'administration
admin.site.register(models.Role, RoleAdmin)

# Enregistrer le modèle sous finalite avec l'interface d'administration
admin.site.register(models.SousFinalite, SousFinaliteAdmin)

# Enregistrer le modèle CustomUser avec l'interface d'administration
admin.site.register(models.User, UserAdmin)

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
