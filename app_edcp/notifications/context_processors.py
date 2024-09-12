# appnotification/context_processors.py
from .models import Notification


def notifications_processor(request):
    """
        Définition d'un processeur de contexte qui rendra les notifications accessibles dans tous les templates de l'application.
    """
    # Vérifie si l'utilisateur est authentifié. Si l'utilisateur n'est pas connecté, 
    # il ne sera pas possible de récupérer ses notifications.
    if request.user.is_authenticated:
        # Récupère toutes les notifications non lues pour l'utilisateur connecté à partir de la base de données.
        # La requête filtre les objets Notification pour cet utilisateur (request.user) et dont 'is_read' est False.
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        
        return {'notifications': notifications}
    
    # Si l'utilisateur n'est pas authentifié, un dictionnaire vide est renvoyé, 
    # ce qui signifie qu'aucune notification ne sera disponible dans le contexte des templates.
    return {}