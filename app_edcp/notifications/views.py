from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

# Lors d'un événement, par exemple après la sauvegarde d'un objet :
from django.db.models.signals import post_save
from django.dispatch import receiver
from base_edcp.models import Enregistrement
from correspondant.models import DesignationDpoMoral


@login_required
def notification_list(request):
    """ Vue pour afficher la liste des notifications """

    # Récupération des notifications non lues de l'utilisateur connecté à partir de la base de données.
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})


@login_required
def mark_as_read(request, notification_id):
    """ 
        Vue pour marquer une notification comme lue 
    """

    # La requête vérifie que la notification appartient à l'utilisateur actuel (request.user).
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True  # Marque la notification comme lue
    notification.save()  # Sauvegarde le changement dans la base de données
    return redirect('notification_list')


# models.py
def create_notification(user, message):
    """
        Creer une notification
    """
    notification = Notification(user=user, message=message)
    notification.save()


@login_required
def header_notifications(request):
    """
     Récupérer les notifications non lues pour l'utilisateur connecté
    """
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return {'notifications': notifications}


@login_required
def mark_notification_as_read(request, notification_id):
    """
        Récupère la notification de l'utilisateur en fonction de son ID (notification_id) et vérifie qu'elle
        appartient à l'utilisateur connecté. Si la notification n'existe pas pour cet utilisateur,
        une erreur sera levée (par exemple, une exception DoesNotExist).
    """
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('some_view')  # Rediriger vers la vue appropriée après la lecture
