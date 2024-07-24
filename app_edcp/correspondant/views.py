from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from datetime import datetime
from .models import Correspondant
from .forms import DPOForm
from base_edcp.models import User, Enregistrement

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande correspondant """
    correspondants = Correspondant.objects.filter(user=request.user)
    orgs_without_dpo = Enregistrement.objects.filter(user=request.user).filter(has_dpo=False)
    context = {
        'correspondants': correspondants,
        'orgs_without_dpo': orgs_without_dpo
    }

    return render(request, 'correspondant/index.html', context=context)




class DPOListView(ListView):
    model = Correspondant
    template_name = 'correspondant/correspondant_list.html'
    context_object_name = 'correspondants'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset


class DPODetailView(DetailView):
    model = Correspondant
    template_name = 'correspondant/correspondant_detail.html'
    context_object_name = 'correspondant'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset
    

class DPOCreateView(CreateView):
    model = Correspondant
    template_name = 'correspondant/correspondant_create.html'
    # fields = ['raisonsociale', 'dpo', 'user']

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
    form_class = DPOForm
    # id_personnephysique = TypeClient.objects.filter(label="Personne physique").first().id
    # id_personnephysique = '1'
    # extra_context = {'id_personnephysique': id_personnephysique}

    def form_valid(self, form):
        # Add custom processing here
        obj = form.save(commit=False)
        
        # Ajout de l'utilisateur courant
        obj.user = self.request.user
        # obj.created_at = datetime.now()
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
        return reverse('dashboard:correspondant:detail', kwargs={'pk': self.object.pk})
        # return reverse('dashboard:index')

    def get_success_url(self):
        return '/correspondant/'