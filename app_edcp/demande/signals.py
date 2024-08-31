from django.db.models.signals import pre_save
from django.dispatch import receiver

from base_edcp.emails import send_automatic_email, MAIL_CONTENTS, DEMANDE_EMAILS_TEMPLATES
from .models import Demande



@receiver(pre_save, sender=Demande)
def notify_status_update(sender, instance, **kwargs):
  print('Pre save detected for ', instance)
  """ Envoie un mail et une notification à l'utilisateur demandeur et aux gestionnaires si la demande change de status.
  Fonction déclenchée avant la méthode save() de la demande.
  """
  if hasattr(instance, '_original_status') and instance._original_status != instance.status:
    print(f'Statut demande {instance} mis à jour : ', instance._original_status,  instance.status)
    notify_by_email(demande=instance)

  instance._original_status = instance.status


def notify_by_email(demande):
  print('notifying by email : ', demande)
  mail_context = {
    'demande': demande
  }
  categorie_label = demande.categorie.label
  status_label = demande.status.label
  print('categorie / status : ', categorie_label, status_label)

  if DEMANDE_EMAILS_TEMPLATES[categorie_label] and DEMANDE_EMAILS_TEMPLATES[categorie_label][status_label]:
    mail_content = DEMANDE_EMAILS_TEMPLATES[categorie_label][status_label]
    recipient_list = [demande.created_by.email, demande.organisation.email_contact]
    mail_context = {
      'demande': demande,
      'recipient_list': recipient_list
    }
    send_automatic_email(mail_content=mail_content, context=mail_context)