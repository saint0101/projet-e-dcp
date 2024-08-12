from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django import forms
from .models import *
from .forms import CreateDemandeForm, UpdateDemandeTraitementForm, UpdateDemandeTransfertForm, UpdateDemandeVideoForm, UpdateDemandeBioForm
from .forms_structures import FORM_STRUCTURE_TRAITEMENT, FORM_STRUCTURE_TRANSFERT, FORM_STRUCTURE_VIDEO, FORM_STRUCTURE_BIOMETRIE
from base_edcp.models import Enregistrement

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande autorisation """
    return render(request, 'demande_auto/index.html')


def save_historique(demande, action_label, user):
  """ sauvegarde de l'historique d'une demande """
  historique = HistoriqueDemande()
  historique.demande = demande
  historique.status = demande.status
  historique.action = ActionDemande.objects.get(label=action_label)
  historique.auteur = user
  historique.save()

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

        # création de l'historique
        save_historique(demande, 'creation', request.user)

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
  

def get_sous_finalites(request, pk):
  if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
    id_finalite = request.GET.get('id_finalite')
    finalite = Finalite.objects.get(pk=id_finalite)
    print(f'Ajax request received {id_finalite}')
    sous_finalites = SousFinalite.objects.filter(finalite_id=id_finalite).values('id', 'label')
    return JsonResponse({'sousFinalites': list(sous_finalites)})



def update(request, pk):
  form_structure = []
  context = {}
  form = None
  object = DemandeAuto.objects.get(pk=pk)

  if object.type_demande.label == 'traitement':
    print ('update traitement')
    form_structure = FORM_STRUCTURE_TRAITEMENT
    form = UpdateDemandeTraitementForm(instance=object)

  if object.type_demande.label == 'transfert':
    print ('update transfert')
    form_structure = FORM_STRUCTURE_TRANSFERT
    form = UpdateDemandeTransfertForm(instance=object)

  if object.type_demande.label == 'videosurveillance':
    print ('update videosurveillance')
    form_structure = FORM_STRUCTURE_VIDEO
    form = UpdateDemandeVideoForm(instance=object)

  if object.type_demande.label == 'biometrie':
    print ('update biometrie')
    form_structure = FORM_STRUCTURE_BIOMETRIE
    form = UpdateDemandeBioForm(instance=object)

  rendered_form = form.render('forms/multisteps_form.html', context={'form': form, 'form_structure': form_structure})
  context['form'] = rendered_form
  context['demande'] = object
  context['historique'] = HistoriqueDemande.objects.filter(demande=object)
  #context['form_structure'] = FORM_STRUCTURE
  return render(request, "demande_auto/demande_edit.html", context)


class demandeUpdateView(UpdateView):
  model = DemandeAuto
  fields = '__all__'
  template_name = 'demande_auto/demande_edit.html'
  context_form_structure = []

  def get_object(self, queryset=None):
    object = super().get_object(queryset=queryset)

    if object.type_demande.label == 'traitement':
      print ('update traitement')
      self.context_form_structure = FORM_STRUCTURE_TRAITEMENT
      self.model = DemandeAutoTraitement

    if object.type_demande.label == 'transfert':
      print ('update transfert')
      self.context_form_structure = FORM_STRUCTURE_TRANSFERT
      self.model = DemandeAutoTransfert

    if object.type_demande.label == 'videosurveillance':
      print ('update videosurveillance')
      self.context_form_structure = FORM_STRUCTURE_VIDEO
      self.model = DemandeAutoVideo

    if object.type_demande.label == 'biometrie':
      print ('update biometrie')
      self.context_form_structure = FORM_STRUCTURE_BIOMETRIE
      self.model = DemandeAutoBiometrie

    # Now, call the original get_object method
    return object

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['historique'] = HistoriqueDemande.objects.filter(demande=self.object)
    context['form_structure'] = self.context_form_structure
    return context

   
  