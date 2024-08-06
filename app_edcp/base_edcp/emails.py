from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages


MAIL_CONTENTS = {
  'enregistrement_new_client': {
    'subject': 'Enregistrement effectué',
    'template': 'emails/enregistrement/enregistrement_new.html'
  },
  'correspondant_new_compte': {
    'subject': 'Création de compte utilisateur',
    'template': 'emails/correspondant/new_compte_client.html'
  },
  'correspondant_designation_client': {
    'subject': 'Désignation de Correspondant',
    'template': 'emails/correspondant/designation_client.html'
  },
  'correspondant_approbation': {
    'subject': '',
    'template': 'emails/enregistrement.html'
  },
}

def send_email(request, mail_content, recipient_list, context, show_message=True):
  email_from = settings.EMAIL_HOST_USER 
  current_site = get_current_site(request)
  context['domain'] = "http://" + current_site.domain

  print('EMAIL from : ', email_from)
  html_message = render_to_string(mail_content['template'], context)
  text_message = strip_tags(html_message)
  print('EMAIL message : ', text_message)
  
  try:
    send_mail(
      subject=mail_content['subject'], 
      message=text_message,
      html_message=html_message, 
      from_email=email_from, 
      recipient_list=recipient_list, 
      fail_silently=False
    )
    print('EMAIL envoyé')
    if show_message:
      messages.success(request, 'Un email de confirmation vous a été envoyé.')

  except Exception as e:
    print('EMAIL ERREUR : ', e)
    if show_message:
      messages.error(request, 'Une erreur est survenue lors de l\'envoi de l\'e-mail : \n' + str(e))
  