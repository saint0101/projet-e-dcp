import os
import django
from django.core.mail import send_mail
from django.conf import settings


# Définir la variable d'environnement DJANGO_SETTINGS_MODULE pour pointer vers le fichier de configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')  # Remplacez 'projet.settings' par le chemin correct vers vos settings

# Initialiser Django
django.setup()

# Paramètres de l'e-mail
mail_subject = 'Test Email'
message = 'This is a test email.'
email_from = settings.EMAIL_HOST_USER
recipient_list = ['fouriersaint@gmail.com']

try:
    send_mail(mail_subject, message, email_from, recipient_list, fail_silently=False)
    print('Test mail envoyé avec succès')
except Exception as e:
    print('Erreur lors de l\'envoi de l\'e-mail:', e)