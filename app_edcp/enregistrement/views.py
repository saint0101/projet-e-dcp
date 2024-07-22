from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from base_edcp.models import Enregistrement

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande enregistrenent """
    return render(request, 'enregistrement/index.html')

class EnregCreateView(CreateView):
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_create.html'
    fields = [
        'typeclient',
        'raisonsociale',
        'representant',
        'secteur',
        'secteur_description',
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
    ]

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
        # return reverse('mymodel_detail', kwargs={'pk': self.object.pk})
        return reverse('dashboard:index')
    

class EnregListView(ListView):
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_list.html'
    context_object_name = 'enregistrements'


class EnregDetailView(DetailView):
    model = Enregistrement
    template_name = 'enregistrement/enregistrement_detail.html'
    context_object_name = 'enregistrement'