from django.contrib import messages
from base_edcp.emails import send_email
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django import forms
from .models import *
from .forms import CreateDemandeForm, UpdateDemandeForm, UpdateDemandeTraitementForm, UpdateDemandeTransfertForm, UpdateDemandeVideoForm, UpdateDemandeBioForm
from .forms_structures import FORM_STRUCTURE_TRAITEMENT, FORM_STRUCTURE_TRANSFERT, FORM_STRUCTURE_VIDEO, FORM_STRUCTURE_BIOMETRIE
from base_edcp.models import Enregistrement

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande autorisation """
    return render(request, 'demande_auto/index.html')


class DemandeListView(ListView):
  model = DemandeAuto
  template_name = 'demande_auto/demande_list.html'
  context_object_name = 'demandes'

  def get_queryset(self):
    """ Filtre les demandes en fonction des droits de l'utilisateur """
    queryset = super().get_queryset()
    # Si l'utilisateur n'est pas un membre du personnel, filtre pour ne montrer que ses propres enregistrements
    if not self.request.user.is_staff:
        return queryset.filter(user=self.request.user)
    return queryset
  

def detail(request, pk):
  context = get_form_context(pk)
  return render(request, "demande_auto/demande_detail.html", context)


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


def get_update_form(object, request=None):
  form_structure = []
  form = None
  if object.type_demande.label == 'traitement':
    print ('update traitement')
    form_structure = FORM_STRUCTURE_TRAITEMENT
    if request:
      form = UpdateDemandeTraitementForm(request.POST, instance=object)
    else:
      form = UpdateDemandeTraitementForm(instance=object)

  if object.type_demande.label == 'transfert':
    print ('update transfert')
    form_structure = FORM_STRUCTURE_TRANSFERT
    if request:
      form = UpdateDemandeTransfertForm(request.POST, instance=object)
    else:
      form = UpdateDemandeTransfertForm(instance=object)

  if object.type_demande.label == 'videosurveillance':
    print ('update videosurveillance')
    form_structure = FORM_STRUCTURE_VIDEO
    if request:
      form = UpdateDemandeVideoForm(request.POST, instance=object)
    else:
      form = UpdateDemandeVideoForm(instance=object)

  if object.type_demande.label == 'biometrie':
    print ('update biometrie')
    form_structure = FORM_STRUCTURE_BIOMETRIE
    if request:
      form = UpdateDemandeBioForm(request.POST, instance=object)
    else:
      form = UpdateDemandeBioForm(instance=object)

  return form, form_structure

def get_form_context(obj_id, request=None):
  obj = get_object_or_404(DemandeAuto, pk=obj_id)
  type_demande_label = obj.type_demande.label
  form_structure = []
  form = None
  object = None
  context = {}
  if type_demande_label == 'traitement':
    print ('update traitement')
    form_structure = FORM_STRUCTURE_TRAITEMENT
    object = get_object_or_404(DemandeAutoTraitement, pk=obj_id)
    if request:
      form = UpdateDemandeTraitementForm(request.POST, instance=object)
    else:
      form = UpdateDemandeTraitementForm(instance=object)

  if type_demande_label == 'transfert':
    print ('update transfert')
    form_structure = FORM_STRUCTURE_TRANSFERT
    object = get_object_or_404(DemandeAutoTransfert, pk=obj_id)
    if request:
      form = UpdateDemandeTransfertForm(request.POST, instance=object)
    else:
      form = UpdateDemandeTransfertForm(instance=object)

  if type_demande_label == 'videosurveillance':
    print ('update videosurveillance')
    form_structure = FORM_STRUCTURE_VIDEO
    object = get_object_or_404(DemandeAutoVideo, pk=obj_id)
    if request:
      form = UpdateDemandeVideoForm(request.POST, instance=object)
    else:
      form = UpdateDemandeVideoForm(instance=object)

  if type_demande_label == 'biometrie':
    print ('update biometrie')
    form_structure = FORM_STRUCTURE_BIOMETRIE
    object = get_object_or_404(DemandeAutoBiometrie, pk=obj_id)
    if request:
      form = UpdateDemandeBioForm(request.POST, instance=object)
    else:
      form = UpdateDemandeBioForm(instance=object)
  
  rendered_form = form.render('forms/multisteps_form.html', context={'form': form, 'form_structure': form_structure})

  context['demande'] = object
  context['raw_form'] = form
  context['form'] = rendered_form
  context['form_structure'] = form_structure
  context['historique'] = HistoriqueDemande.objects.filter(demande=object)
  
  return context

def update(request, pk):
  form_structure = []
  context = {}
  # form = None
  
  # object = DemandeAuto.objects.get(pk=pk)
  #object = get_object_or_404(DemandeAuto, pk=pk)
  #form, form_structure = get_update_form(object)

  if request.method == 'POST':
    # form, form_structure = get_update_form(object, request)
    # print ('form : ', form)
    context = get_form_context(pk, request)
    if context['raw_form'].is_valid():
      # print('form valid. trying save')
      context['raw_form'].save()
      messages.success(request, 'La demande a bien été enregistrée.')
      return redirect('dashboard:demande_auto:edit', pk=context['demande'].id)
    
    else:
      print('form not valid')
      print(context['raw_form'].errors)
      messages.error(request, 'La demande n\'a pas pu être enregistrée. Veuillez vérifier les données du formulaire et réessayer.')
      return render(request, "demande_auto/demande_edit.html", context)

  # rendered_form = form.render('forms/multisteps_form.html', context={'form': form, 'form_structure': form_structure})
  """ context['form'] = rendered_form
  context['demande'] = object
  context['historique'] = HistoriqueDemande.objects.filter(demande=object) """
  #context['form_structure'] = FORM_STRUCTURE
  context = get_form_context(pk)
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
  
  def get_form(self, form_class=None):
    form = super().get_form(form_class)
    type_demande_label = self.object.type_demande.label
    list_finalites = TypeDemandeAuto.objects.get(label=type_demande_label).finalites.all()
    form.fields['finalite'].queryset = list_finalites
    
    list_sousfinalites = SousFinalite.objects.filter(finalite__in=list_finalites)
    #form.fields['sous_finalites'].widget = forms.CheckboxSelectMultiple(attrs={'required': True}, choices=[(sousfinalite.id, sousfinalite.label) for sousfinalite in list_sousfinalites])
    # form.fields['sous_finalites'].initial = 0
    # form.fields['sous_finalites'].widget = forms.CheckboxSelectMultiple(attrs={'required': True})
    form.fields['sous_finalites'].queryset = SousFinalite.objects.filter(finalite__in=list_finalites)
    # form.fields['personnes_concernees'].widget = forms.CheckboxSelectMultiple(attrs={'required': True})
    # form_html = form.render()  # Renders the form with the default rendering or custom template
    rendered_form = form.render('forms/multisteps_form.html', context={'form': form, 'form_structure': self.context_form_structure})
    return rendered_form

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['historique'] = HistoriqueDemande.objects.filter(demande=self.object)
    context['form_structure'] = self.context_form_structure
    return context
  


   
  