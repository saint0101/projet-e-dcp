from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django import forms
from .models import DemandeAutoTraitement, DemandeAutoTransfert, DemandeAutoVideo, DemandeAutoBiometrie, TypeDemandeAuto, Status, DemandeAuto
from .forms import CreateDemandeForm, FORM_STRUCTURE
from base_edcp.models import Enregistrement

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande autorisation """
    return render(request, 'demande_auto/index.html')


def create(request):
    context = {}
    form = CreateDemandeForm()
    form.fields['organisation'].queryset = Enregistrement.objects.filter(user=request.user)
    """ Pour le multisteps"""
    """ rendered_form = form.render('forms/multisteps_form.html', context={'form': form, 'form_structure': FORM_STRUCTURE}) """
    # context['form'] = form
    # context['form_structure'] = FORM_STRUCTURE
    # return render(request, "index.html", context)

    if request.method == 'POST':
      form = CreateDemandeForm(request.POST)
      if form.is_valid():
        form.cleaned_data['user'] = request.user
        form.cleaned_data['status'] = Status.objects.get(label='brouillon')
        demande = None
        if form.cleaned_data['type_demande'] == DemandeAutoTraitement.get_type_demande():
           demande = DemandeAutoTraitement.objects.create(**form.cleaned_data)
        
        if form.cleaned_data['type_demande'] == DemandeAutoTransfert.get_type_demande():
           demande = DemandeAutoTransfert.objects.create(**form.cleaned_data)

        if form.cleaned_data['type_demande'] == DemandeAutoVideo.get_type_demande():
           demande = DemandeAutoVideo.objects.create(**form.cleaned_data)

        if form.cleaned_data['type_demande'] == DemandeAutoBiometrie.get_type_demande():
           demande = DemandeAutoBiometrie.objects.create(**form.cleaned_data)

        return redirect('dashboard:demande_auto:edit', pk=demande.id)        

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
  model = DemandeAuto
  fields = '__all__'
  template_name = 'demande_auto/demande_edit.html'

  def get_object(self, queryset=None):
    object = super().get_object(queryset=queryset)

    if object.type_demande.label == 'traitement':
      print ('update traitement')
      self.model = DemandeAutoTraitement

    if object.type_demande.label == 'transfert':
      print ('update transfert')
      self.model = DemandeAutoTransfert

    if object.type_demande.label == 'videosurveillance':
      print ('update videosurveillance')
      self.model = DemandeAutoVideo

    if object.type_demande.label == 'biometrie':
      print ('update biometrie')
      self.model = DemandeAutoBiometrie

    # Now, call the original get_object method
    return object


   
  