# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model
from base_edcp.models import User


class Notification(models.Model):
    """ Table notification """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='Utilisateur') # Référence à l'utilisateur recevant la notification
    message = models.TextField() # message de notification
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date et heure de création')  # Date et heure de création de la notification
    is_read = models.BooleanField(default=False, verbose_name='Est lu')    # Indique si la notification a été lue

    def __str__(self):
        """ les champs à retourner """
        return f'Notification pour {self.user} - {self.message}'
    
    class Meta:
        ordering = ['-created_at']