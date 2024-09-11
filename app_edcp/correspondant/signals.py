from re import I
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from notifications.models import Notification

# Lors d'un événement, par exemple après la sauvegarde d'un objet :
from django.db.models.signals import post_save
from django.dispatch import receiver
from correspondant.models import DesignationDpoMoral, QualificationsDPO, Correspondant
from notifications.views import create_notification


@receiver(post_save, sender=Correspondant)
def send_notification_on_save_dpo(sender, instance, created, **kwargs):
    """
    Fonction appelée après la création d'une instance de Correspondant.
    Si la demande est nouvellement créée, une notification est envoyée à l'utilisateur.
    """
    if created:
        create_notification(instance.user, "Une nouvelle désignation d'un Correspondant moral a été effectuée.")


@receiver(post_save, sender=DesignationDpoMoral)
def send_notification_on_save_dpo(sender, instance, created, **kwargs):
    """
    Fonction appelée après la création d'une instance de DesignationDpoMoral.
    Si la demande est nouvellement créée, une notification est envoyée à l'utilisateur.
    """
    if created:
        create_notification(instance.user, "Une nouvelle désignation d'un DPO moral a été effectuée.")


@receiver(post_save, sender=QualificationsDPO)
def send_notification_on_save_dpo(sender, instance, created, **kwargs):
    """
    Fonction appelée après la création d'une instance de QualificationsDPO.
    Si la demande est nouvellement créée, une notification est envoyée à l'utilisateur.
    """
    if created:
        create_notification(instance.user, "Une nouvelle désignation QualificationsDPO a été effectuée.")
