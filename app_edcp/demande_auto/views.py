from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django import forms
from .models import TypeDemandeAuto, DemandeAuto
from .forms import CreateDemandeForm, FORM_STRUCTURE
from base_edcp.models import Enregistrement

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande autorisation """
    return render(request, 'demande_auto/index.html')


def create(request):
    context = {}
    form = CreateDemandeForm(request)
    """ Pour le multisteps"""
    """ rendered_form = form.render('forms/multisteps_form.html', context={'form': form, 'form_structure': FORM_STRUCTURE}) """
    # context['form'] = form
    # context['form_structure'] = FORM_STRUCTURE
    # return render(request, "index.html", context)

    if request.method == 'POST':
      form = CreateDemandeForm(request.POST)
      if form.is_valid():
        pass

    types_demandes = TypeDemandeAuto.objects.all()
    context['form'] = form
    context['types_demandes'] = types_demandes
    
    return render(request, 'demande_auto/nouvelle_demande.html', context=context)



""" class demandeCreateView(CreateView):
  # form_class = CreateDemandeForm
  model = DemandeAuto
  template_name = 'demande_auto/nouvelle_demande.html'
  fields = '__all__'
  # success_url = 'demande_auto:index'


  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['request'] = self.request  # Pass the request object to the form
    return kwargs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['types_demandes'] = TypeDemandeAuto.objects.all()
    return context
  
  def get_success_url(self):
    # Redirect to the detail view of the created object
    return reverse('dashboard:demande_auto:edit', kwargs={'pk': self.object.pk}) """
  
  

class demandeUpdateView(UpdateView):
   fields = '__all__'
   template_name = 'demande_auto/demande_edit.html'

   
  