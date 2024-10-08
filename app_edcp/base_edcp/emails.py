"""
Fonction pour l'envoi des mails de notification.
Définit également un dictionnaire pour les sujets et templates.
"""

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages


MAIL_CONTENTS = {
  # Notification client pour l'enregistrement d'une nouvelle organisation
  'enregistrement_new_client': {
    'subject': 'Enregistrement effectué',
    'template': 'emails/enregistrement/enregistrement_new.html'
  },
  # Notification client pour la création d'un compte utilisateur pour le DPO
  'correspondant_new_compte': {
    'subject': 'Création de compte utilisateur',
    'template': 'emails/correspondant/new_compte_client.html'
  },
  # Notification client pour la finalisation de la désignation du DPO
  'correspondant_designation_client': {
    'subject': 'Désignation de Correspondant',
    'template': 'emails/correspondant/designation_client.html'
  },
  # Notification gestionnaire pour la désignation d'un nouveau DPO
  'correspondant_designation_mgr': {
    'subject': 'Désignation de Correspondant',
    'template': 'emails/correspondant/designation_mgr.html'
  },
  # Notification client pour l'approbation ou le refus d'un DPO désigné
  'correspondant_approbation_client': {
    'subject': 'Approbation du Correspondant',
    'template': 'emails/correspondant/approbation_client.html'
  },
}

def send_email(request, mail_content, recipient_list, context, show_message=True):
  """ Fonction d'envoi d'email.
  Paramètres :
  - request -- l'objet request de la requête HTTP
  - mail_content -- le dictionnaire contenant le sujet et le template de l'email (voir MAIL_CONTENTS plus haut)
  - recipient_list -- la liste des destinataires de l'email, sous forme de tableau
  - context -- le contexte de l'email sous forme de dictionnaire. Utilisé pour passer des variables au template
  - show_message -- indique si un message doit être affiché ou non sous forme d'alerte Toast (default True)
  """
  email_from = settings.EMAIL_HOST_USER # récupère l'adresse email par défaut 
  print('EMAIL from : ', email_from) 
  current_site = get_current_site(request) # recuperation de l'adresse du site
  context['domain'] = "http://" + current_site.domain # constitution de l'url du site. Utilisée dans les mails pour former les liens

  html_message = render_to_string(mail_content['template'], context) # contenu du mail au format HTML
  text_message = strip_tags(html_message) # contenu du mail au format texte
  print('EMAIL message : ', text_message)
  
  # tentative d'envoi du mail
  try:
    send_mail(
      subject=mail_content['subject'], 
      message=text_message,
      html_message=html_message, 
      from_email=email_from, 
      recipient_list=recipient_list, 
      fail_silently=False # indique si l'échec de l'envoi doit générer une erreur
    )
    print('EMAIL envoyé')
    if show_message: # si l'affichage d'alerte est activé
      messages.success(request, 'Un email de confirmation vous a été envoyé.')

  # en cas d'erreur d'envoi du mail
  except Exception as e:
    print('EMAIL ERREUR : ', e)
    if show_message:
      messages.error(request, 'Une erreur est survenue lors de l\'envoi de l\'e-mail : \n' + str(e))
  