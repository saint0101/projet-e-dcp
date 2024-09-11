from django.contrib import admin
from notifications import models

# Register your models here.

# module notificaton
@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    """ definir la page de l'administrateur """

    ordering = ['id']  # Ordonne les notifications par ID
    list_display = ['user', 'message', 'created_at', 'is_read']  # Affiche les utilisateurs par user et message
    search_fields = ('user__username', 'message')
