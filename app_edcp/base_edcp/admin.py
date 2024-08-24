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
    list_display = ['nom', 'prenoms', 'email', 'is_superuser', 'is_staff', 'is_active', 'is_dpo',]  # Affiche les utilisateurs par e-mail et login

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
                    'email_verified',
                    'must_reset'
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
                'email_verified',
                'must_reset',
            ),
        }),
    )


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    """ Definir la table Role dans l'espace admin """

    ordering = ['id']  # Ordonne les Role par ID
    list_display = ['role']  # Affiche informatons de la table


@admin.register(models.GroupExtension)
class GroupExtensionAdmin(admin.ModelAdmin):
    """ Definir la table GroupExtension dans l'espace admin """
    ordering = ['niv_validation']  # Ordonne les GroupExtension par ID
    list_display = ['group_name', 'group', 'niv_validation']  # Affiche les GroupExtension


# module notificaton
@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['user', 'message', 'created_at', 'is_read']  # Affiche les utilisateurs par user et message
    search_fields = ('user__username', 'message')



# module Enregistrement
@admin.register(models.Enregistrement)
class EnregistrementAdmin(admin.ModelAdmin):
    """ Page d'administration pour Enregistrement """

    ordering = ['id']  # Ordonne les enregistrements par ID
    list_display = ['user', 'created_at', 'typeclient', 'raisonsociale', 'representant', 'rccm', 'secteur', 'telephone', 'email_contact', 'ville' ]


@admin.register(models.JournalTransaction)
class JournalTransactionAdmin(admin.ModelAdmin):
    """ Definir la table JournalTransaction dans l'espace admin """

    ordering = ['id']  # Ordonne les JournalTransaction par ID
    list_display = ['transaction', 'cible', 'created', 'user']  # Affiche informatons de la table
    search_fields = ('transaction', 'cible')

