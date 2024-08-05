from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages


MAIL_CONTENTS = {
  'enregistrement_new': {
    'subject': 'Enregistrement effectué',
    'template': 'emails/enregistrement_new.html'
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

def send_email(request, mail_content, recipient_list, context):
  email_from = settings.EMAIL_HOST_USER 
  print('EMAIL from : ', email_from)
  message = render_to_string(mail_content['template'], context)
  print('EMAIL message : ', message)
  
  try:
    send_mail(mail_content['subject'], message, email_from, recipient_list, fail_silently=False)
    print('EMAIL envoyé')
    messages.success(request, 'Un email de confirmation vous a été envoyé.')

  except Exception as e:
    print('EMAIL ERREUR : ', e)
    messages.error(request, 'Une erreur est survenue lors de l\'envoi de l\'e-mail : \n' + str(e))
  