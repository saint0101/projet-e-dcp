from re import I
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from notifications.models import Notification

# Lors d'un événement, par exemple après la sauvegarde d'un objet :
from django.db.models.signals import post_save
from django.dispatch import receiver
from base_edcp.models import Enregistrement
from correspondant.models import DesignationDpoMoral
from notifications.views import create_notification


@receiver(post_save, sender=Enregistrement)
def send_notification_on_save(sender, instance, created, **kwargs):
    """
    Fonction appelée après la création d'une instance de DemandeAutorisation.
    Si la demande est nouvellement créée, une notification est envoyée à l'utilisateur.
    """
    if created:
        create_notification(instance.user, "Un nouvel enregistrement a été créé.")
