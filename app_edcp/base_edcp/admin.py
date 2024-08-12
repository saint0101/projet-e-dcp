from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from base_edcp import models


# module enregistreprement d'un utilisateur
@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """
    Définit les pages d'administration pour les utilisateurs.
    """
    ordering = ['id']  # Ordonne les utilisateurs par ID
    list_display = ['nom', 'prenoms', 'email']  # Affiche les utilisateurs par e-mail et login

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
                    'username',
                    'avatar',
                    'is_dpo',
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
                'username',
                'avatar',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

@admin.register(models.Role)
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


# module TypeClient
@admin.register(models.TypeClient)
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

@admin.register(models.TypePiece)
class TypePieceAdmin(admin.ModelAdmin):
    """ definir la page de gestion des types de pièces pour l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['label', 'description', 'sensible', 'ordre']  # Affiche informatons de la table

    # Éditer le type du client
    fieldsets = (
        (None, {
            'fields': ('label', 'description', 'sensible', 'ordre')
        }),
    )


# module Secteur
@admin.register(models.Secteur)
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
@admin.register(models.Pays)
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
@admin.register(models.CasExemption)
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
@admin.register(models.CategorieDCP)
class CategorieDCPAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['categoriedcp']  # Affiche informatons de la table
    search_fields = ('categorie',)

    # Éditer le champ CategorieDCPAdmin
    fieldsets = (
        (None, {
            'fields': ('categoriedcp', )
        }),
    )


# module CategorieTrait
@admin.register(models.CategorieTrait)
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


@admin.register(models.DemandeAuto)
class DemandeAutoAdmin(admin.ModelAdmin):
    list_display = ('user', 'organisation_id', 'organisation_name', 'consent_dcp', 'consent_docs', 'summary', 'traitement_sensible', 'finalite', 'legitimite', 'status', 'type_demande')
    search_fields = ('organisation_name', 'summary')
    list_filter = ('finalite', 'legitimite', 'status', 'type_demande')


# module Fonction
@admin.register(models.Fonction)
class FonctionAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les fonction par ID
    list_display = ['fonction']  # Affiche informatons de la table
    search_fields = ('fonction',)

    # Éditer le champ CategorieTraitAdmin
    fieldsets = (
        (None, {
            'fields': ('fonction', )
        }),
    )


# module Finalite
@admin.register(models.Finalite)
class FinaliteAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les fonction par ID
    list_display = ['label', 'description']  # Affiche informatons de la
    search_fields = ('label',)
    # Éditer le champ FinaliteAdmin
    fieldsets = (
        (None, {
            'fields': ('label', 'sensible', )
        }),
    )


# module
@admin.register(models.FondJuridique)
class FondJuridiqueAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les fonction par ID
    list_display = ['label', 'description',]  # Affiche informatons de la table
    search_fields = ('label',)

    # Éditer le champ FinaliteAdmin
    fieldsets = (
        (None, {
            'fields': ('label', 'description', )
        }),
    )


# module notificaton
@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['user', 'message', 'created_at', 'is_read']  # Affiche les utilisateurs par user et message
    search_fields = ('user__username', 'message')

    # Éditer l'utilisateur
    fieldsets = (
        (None, {
            'fields': ('user', 'message', 'is_read')
        }),
    )


# module Enregistrement
@admin.register(models.Enregistrement)
class EnregistrementAdmin(admin.ModelAdmin):
    """ Page d'administration pour Enregistrement """

    ordering = ['id']  # Ordonne les enregistrements par ID
    list_display = ['user', 'created_at', 'typeclient', 'raisonsociale', 'representant', 'rccm', 'secteur', 'presentation', 'telephone', 'email_contact', 'site_web', 'pays',
                    'ville', 'adresse_geo', 'adresse_bp', 'gmaps_link', 'effectif', ]

    """ fieldsets = (
        (None, {
            'fields': ('user', 'typeclient', 'raisonsociale', 'representant', 'rccm', 'secteur', 'presentation', 'telephone', 'email_contact', 'site_web', 'pays',
                       'ville', 'adresse_geo', 'adresse_bp', 'gmaps_link', 'effectif', 'has_dpo')
        }),
    ) """


# module Autorisation
@admin.register(models.Autorisation)
class AutorisationAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['enregistrement', 'numero_autorisation', 'created_at']  # Affiche informatons de la table
    search_fields = ('enregistrement', 'numero_autorisation')

    # Éditer le type du client
    fieldsets = (
        (None, {
            'fields': ('enregistrement', 'numero_autorisation', )
        }),
    )

@admin.register(models.SousFinalite)
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


@admin.register(models.PersConcernee)
class PersConcerneeAdmin(admin.ModelAdmin):
    """ Definir la table Role dans l'espace admin """

    ordering = ['id']  # Ordonne les personne concernee par ID
    list_display = ['label', 'sensible', 'ordre']  # Affiche informatons de la table
    search_fields = ('label',)

    # Éditer le type des personne concernee
    fieldsets = (
        (None, {
            'fields': ('label', 'sensible', 'ordre') # Utilisez un tuple même pour un seul champ
        }),
    )

@admin.register(models.Habilitation)
class HabilitationAdmin(admin.ModelAdmin):
    """ Definir la table Habilitation dans l'espace admin """

    ordering = ['id']  # Ordonne les Habilitation par ID
    list_display = ['role', 'fonction', 'created']  # Affiche informatons de la table
    search_fields = ('role', 'fonction')

    # Éditer le type des Habilitation
    fieldsets = (
        (None, {
            'fields': ('role', 'fonction', 'created') # Utilisez un tuple même pour un seul champ
        }),
    )


@admin.register(models.JournalTransaction)
class JournalTransactionAdmin(admin.ModelAdmin):
    """ Definir la table JournalTransaction dans l'espace admin """

    ordering = ['id']  # Ordonne les JournalTransaction par ID
    list_display = ['transaction', 'cible', 'created', 'user']  # Affiche informatons de la table
    search_fields = ('transaction', 'cible')

    # Éditer le type des JournalTransaction
    fieldsets = (
        (None, {
            'fields': ('transaction', 'cible', 'created', 'user') # Utilisez un tuple même pour un seul champ
        }),
    )


@admin.register(models.Legitimite)
class LegitimiteAdmin(admin.ModelAdmin):
    list_display = ('label', 'description')
    search_fields = ('label',)

@admin.register(models.ModeRecueilConsent)
class ModeRecueilConsentAdmin(admin.ModelAdmin):
    list_display = ('label', 'description')
    search_fields = ('label',)

@admin.register(models.Transfert)
class TransfertAdmin(admin.ModelAdmin):
    list_display = ('pays', 'destinataire', 'mode', 'type_destinataire')
    search_fields = ('pays', 'destinataire')
    list_filter = ('pays',)


@admin.register(models.Donnee)
class DonneeAdmin(admin.ModelAdmin):
    list_display = ('label', 'sensible', 'duree_conservation')
    search_fields = ('label',)

@admin.register(models.DonneeTraitee)
class DonneeTraiteeAdmin(admin.ModelAdmin):
    list_display = ('label', 'sensible', 'duree_conservation', 'id_categorie')
    search_fields = ('label',)
    filter_horizontal = ('donnees',)

@admin.register(models.Interco)
class IntercoAdmin(admin.ModelAdmin):
    list_display = ('destinataire', 'mode', 'description')
    search_fields = ('destinataire',)

@admin.register(models.SupportCollecte)
class SupportCollecteAdmin(admin.ModelAdmin):
    list_display = ('label', 'description')
    search_fields = ('label',)

@admin.register(models.Authentication)
class AuthenticationAdmin(admin.ModelAdmin):
    list_display = ('label', 'description')
    search_fields = ('label',)

@admin.register(models.Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = ('label', 'description')
    search_fields = ('label',)

@admin.register(models.Hebergement)
class HebergementAdmin(admin.ModelAdmin):
    list_display = ('label', 'description')
    search_fields = ('label',)

@admin.register(models.SecuritePhysique)
class SecuritePhysiqueAdmin(admin.ModelAdmin):
    list_display = ('label', 'description')
    search_fields = ('label',)

@admin.register(models.Securite)
class SecuriteAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    filter_horizontal = ('supports_collecte', 'authentications', 'backups', 'hebergement', 'protect_physique')

@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('label', 'description')
    search_fields = ('label',)

@admin.register(models.TypeDemandeAutorisation)
class TypeDemandeAutorisationAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)


# modifier le titre de l'espace admin de django
admin.site.site_header = "Administration de e-DCP"
admin.site.site_title = "e-DCP Admin"
admin.site.index_title = "Bienvenue dans l'administration de e-DCP"