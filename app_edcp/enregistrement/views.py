from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from base_edcp.models import Enregistrement, TypeClient
from .forms import EnregistrementForm
from dashboard.mixins import UserHasAccessMixin

# Create your views here.

# user/views.py
@login_required(login_url=reverse_lazy('login'))
def index(request):
    """ Vue index demande enregistrenent """
    return render(request, 'enregistrement/index.html')

class EnregCreateView(CreateView):
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_create.html'
    """fields = [
        'typeclient',
        'raisonsociale',
        'representant',
        'secteur',
        'presentation',
        'telephone',
        'email_contact',
        'site_web',
        'pays',
        'ville',
        'adresse_geo',
        'adresse_bp',
        'gmaps_link',
        'effectif',
        'type_piece',
        'num_piece',
    ]"""
    form_class = EnregistrementForm
    id_personnephysique = TypeClient.objects.filter(label="Personne physique").first().id
    extra_context = {'id_personnephysique': id_personnephysique}

    def form_valid(self, form):
        # Add custom processing here
        obj = form.save(commit=False)
        
        # Ajout de l'utilisateur courant
        obj.user = self.request.user
        obj.created_at = datetime.now()
        # Call the super method to save the object
        response = super().form_valid(form)
        # Set the object instance for the response
        self.object = obj
        # Add any post-save processing here
        # For example, sending a notification
        # send_notification(obj)

        return response

    def get_success_url(self):
        # Redirect to the detail view of the created object
        return reverse('dashboard:enregistrement:detail', kwargs={'pk': self.object.pk})
        # return reverse('dashboard:index')
    

class EnregListView(ListView):
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_list.html'
    context_object_name = 'enregistrements'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset


class EnregDetailView(UserHasAccessMixin, DetailView):
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_detail.html'
    context_object_name = 'enregistrement'


class EnregUpdateView(UserHasAccessMixin, UpdateView):
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_update.html'
    id_personnephysique = TypeClient.objects.filter(label="Personne physique").first().id
    extra_context = {'id_personnephysique': id_personnephysique}
    # form_class = EnregistrementForm
    fields = [
        'typeclient',
        'raisonsociale',
        'representant',
        'secteur',
        'presentation',
        'telephone',
        'email_contact',
        'site_web',
        'pays',
        'ville',
        'adresse_geo',
        'adresse_bp',
        'gmaps_link',
        'effectif',
        'type_piece',
        'num_piece',
    ]

    def get_success_url(self):
        return reverse('dashboard:enregistrement:detail', kwargs={'pk': self.object.pk})