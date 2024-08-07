# from email import message
# from django.forms import BaseModelForm
# from django.http import HttpResponse
from django.shortcuts import redirect #, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from base_edcp.models import Enregistrement, TypeClient
from correspondant.models import Correspondant
from .forms import EnregistrementForm
from dashboard.mixins import UserHasAccessMixin

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib import messages
from base_edcp.emails import MAIL_CONTENTS, send_email


# Vue d'index pour afficher la page d'accueil ou la vue d'enregistrement
@login_required(login_url=reverse_lazy('login'))
def index(request):
    """ Vue index pour afficher un enregistrement """
    # Rendu du template 'index.html' pour la vue d'accueil
    return redirect('dashboard:enregistrement:list')


def send_notification(enregistrement):
    """ Envoie une notification par e-mail après la sauvegarde d'un enregistrement """
    subject = 'Nouvel Enregistrement Créé'
    message = f"Un nouvel enregistrement a été créé avec les détails suivants :\n\n{enregistrement}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [enregistrement.user.email]
    print('EMAIL recipient_list : ', recipient_list)
    print('EMAIL from_email: ', recipient_list)
    try:
        send_mail(subject, message, from_email, recipient_list)
        print(f'Email envoyé avec succès à {recipient_list}')
    except BadHeaderError:
        # Gère les erreurs liées à des en-têtes d'e-mail incorrects
        print('Erreur d’en-tête d’e-mail.')
    except Exception as e:
        # Gère d'autres erreurs, comme les erreurs SMTP
        print(f'Une erreur est survenue lors de l’envoi de l’e-mail : {e}')


class EnregCreateView(CreateView):
    """ Vue de création d'un enregistrement """
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_create.html'
    form_class = EnregistrementForm

    def get_context_data(self, **kwargs):
        """ 
        Ajoute des données supplémentaires au contexte du template.
        Permet d'ajouter l'ID de l'objet TypeClient avec le label "Personne physique" au contexte.
        Utilisé pour l'affychage dynamique du formulaire d'enregistrement en cas de personne physique.
        """
        context = super().get_context_data(**kwargs)
        
        type_client = TypeClient.objects.filter(label="Personne physique").first() # Recherche de l'objet TypeClient avec le label "Personne physique"
        context['id_personnephysique'] = type_client.id if type_client else None # Ajoute l'ID de cet objet au contexte (ou None si non trouvé)
        
        return context

    def form_valid(self, form):
        """ Méthode appelée lorsque le formulaire est valide """
        obj = form.save(commit=False) # Sauvegarde l'objet avec les données du formulaire, sans le valider encore
        obj.user = self.request.user # Ajoute l'utilisateur courant comme auteur de l'enregistrement 
        obj.created_at = datetime.now() # Ajoute la date et l'heure actuelles de création
        response = super().form_valid(form) # Sauvegarde l'objet en appelant la méthode de la classe parente
        self.object = obj # Définit l'objet sauvegardé pour les actions post-sauvegarde

        # Ajouter des traitements post-sauvegarde ici si nécessaire
        
        # Appelle la fonction pour envoyer une notification
        print('Enregistrement sauvegardé : ', obj)
        # send_notification(obj)
        mail_context = {
            'organisation': obj,
        }
        print('sending email')
        send_email(self.request, MAIL_CONTENTS['enregistrement_new_client'], [obj.email_contact, self.request.user.email], mail_context)
        return response

    def get_success_url(self):
        """ URL de redirection après une soumission réussie du formulaire """
        # Redirige vers la vue de détail de l'enregistrement nouvellement créé
        messages.success(self.request, 'L\'enregistrement a bien été effectué.')
        return reverse('dashboard:enregistrement:detail', kwargs={'pk': self.object.pk})

class EnregListView(ListView):
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_list.html'
    context_object_name = 'enregistrements'

    def get_queryset(self):
        """ Filtre les enregistrements en fonction des droits de l'utilisateur """
        queryset = super().get_queryset()
        # Si l'utilisateur n'est pas un membre du personnel, filtre pour ne montrer que ses propres enregistrements
        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)
        return queryset

class EnregDetailView(UserHasAccessMixin, DetailView):
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_detail.html'
    context_object_name = 'enregistrement'

    def get_context_data(self, **kwargs):
        """ 
        Ajoute des données supplémentaires au contexte du template.
        Permet de récupérer le Correspondant de l'organisation à afficher;
        """
        context = super().get_context_data(**kwargs)
        org_id = super().get_object().pk # récupération de l'ID de l'organisation actuelle
        correspondant = Correspondant.objects.filter(organisation=org_id).first() # Recherche du premier Correspondant correspondant à l'ID de l'organisation
        # print('correspondant : ', correspondant)
        context['correspondant'] = correspondant
        return context


class EnregUpdateView(UserHasAccessMixin, UpdateView):
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_update.html'
    form_class = EnregistrementForm

    def get_context_data(self, **kwargs):
        """ 
        Ajoute des données supplémentaires au contexte du template.
        Permet d'ajouter l'ID de l'objet TypeClient avec le label "Personne physique" au contexte.
        Utilisé pour l'affychage dynamique du formulaire d'enregistrement en cas de personne physique.
        """
        context = super().get_context_data(**kwargs)
        type_client = TypeClient.objects.filter(label="Personne physique").first() # Recherche de l'objet TypeClient avec le label "Personne physique"
        # Ajoute l'ID de cet objet au contexte (ou None si non trouvé)
        context['id_personnephysique'] = type_client.id if type_client else None
        return context

    def get_success_url(self):
        """ URL de redirection après une mise à jour réussie de l'objet """
        # Redirige vers la vue de détail de l'enregistrement mis à jour
        return reverse('dashboard:enregistrement:detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        """ Passe des arguments supplémentaires au formulaire """
        kwargs = super().get_form_kwargs()
        # Vous pouvez ajouter ici des arguments supplémentaires pour le formulaire si nécessaire
        return kwargs
