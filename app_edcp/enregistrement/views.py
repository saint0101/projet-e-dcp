from django.shortcuts import render
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