from django.contrib import messages
from base_edcp.emails import send_email
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django import forms
from .models import *
from .forms import CommentaireForm, CreateDemandeForm, UpdateDemandeForm, UpdateDemandeTraitementForm, UpdateDemandeTransfertForm, UpdateDemandeVideoForm, UpdateDemandeBioForm
from .forms_structures import FORM_STRUCTURE_TRAITEMENT, FORM_STRUCTURE_TRANSFERT, FORM_STRUCTURE_VIDEO, FORM_STRUCTURE_BIOMETRIE
from base_edcp.models import Enregistrement

######## Fonctions utilitaires ########

def save_historique(demande, action_label, user):
  """
  Sauvegarde de l'historique d'une demande.
  Paramètres :
  -- demande - l'objet demande d'autorisation concerné
  -- action_label - le label de l'action effectuee
  -- user - l'utilisateur à l'origine de l'action
  """
  historique = HistoriqueDemande()
  historique.demande = demande
  historique.status = demande.status
  historique.action = ActionDemande.objects.get(label=action_label)
  historique.auteur = user
  historique.save()


def get_sous_finalites(request, pk):
  """ Vue qui renvoie la liste des sous-finalités pour une finalité sélectionnée, en JSON 
  Paramètres :
  -- request - l'objet requête.
  -- pk - id de la sous finalité. NE PAS SUPPRIMER MEME SI INUTILISE.
  """
  # si la requête est une requête AJAX
  if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
    id_finalite = request.GET.get('id_finalite') # récupération de l'ID de la finalité dans la requête
    sous_finalites = SousFinalite.objects.filter(finalite_id=id_finalite).values('id', 'label') # récupération des sous-finalités
    return JsonResponse({'sousFinalites': list(sous_finalites)}) # renvoi les sous finalités au format JSON


def get_form_context(obj_id, request=None):
  """ Initialise le formulaire de demande d'autorisation et le contexte.
  Paramètres :
  -- obj_id - l'ID de la demande d'autorisation.
  -- request - l'objet requête (facultatif). Doit être fourni pour l'initialisation du formulaire en cas de requête POST.
  Returns : dictionnaire constitué de 
  -- demande - l'objet demande d'autorisation initialisé avec le modèle correspondant (traitement, transfert etc.).
  -- raw_form - le formulaire de demande initialisé en fonction du type de demande et affiché sur une seule page.
  -- form_structure - le dictionnaire correspondant à la structure du formulaire en mode multisteps.
  -- form - le formulaire 'raw_form' affiché en multisteps en fonction de 'form_structure'.
  -- historique - l'historique des actions rattachées à la demande d'autorisation.
  """
  obj = get_object_or_404(DemandeAuto, pk=obj_id) # récupération de l'objet ou erreur 404 si inexistant
  type_demande_label = obj.type_demande.label # récupération du type de demande
  # initialisation des objets à retourner
  form_structure = []
  form = None
  object = None
  context = {}
  # Instanciations en fonction du type de demande
  if type_demande_label == 'traitement': 
    print ('update traitement')
    form_structure = FORM_STRUCTURE_TRAITEMENT
    object = get_object_or_404(DemandeAutoTraitement, pk=obj_id) # récupération de l'objet selon son type de demande
    if request:
      form = UpdateDemandeTraitementForm(request.POST, instance=object) # instanciation du formulaire
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
  
  # génération du formulaire sous forme de multisteps
  rendered_form = form.render('forms/multisteps_form.html', context={'form': form, 'form_structure': form_structure})

  # création du contexte
  context['demande'] = object
  context['raw_form'] = form
  context['form'] = rendered_form
  context['form_structure'] = form_structure
  context['historique'] = HistoriqueDemande.objects.filter(demande=object)
  
  return context


######## Vues #########

def index(request):
    """ Vue index demande autorisation """
    return render(request, 'demande_auto/index.html')

  
def detail(request, pk):
  """ Vue de détail d'une demande d'autorisation """
  context = get_form_context(pk) # récupération du contexte à envoyer au template
  form_comment = CommentaireForm() # initialisation du formulaire de commentaire

  # si une requête a été soumise
  if request.method == 'POST':
    # si la requête est un ajout de commentaire
    if 'form_comment_submit' in request.POST:
      form_comment = CommentaireForm(request.POST) # récupération des données du formulaire
      if form_comment.is_valid():
        # si le formulaire est valide, sauvegarde du commentaire
        commentaire = form_comment.save(commit=False)
        commentaire.demande = context['demande']
        commentaire.auteur = request.user
        commentaire.save() 
        form_comment = CommentaireForm()
      else:
        # context['form_comment'] = form_comment
        print('erreur : ', form_comment.errors)
        messages.error(f'{form_comment.errors}')

  context['form_comment'] = form_comment # affichage du formulaire de commentaires
  context['commentaires'] = Commentaire.objects.filter(demande=context['demande']) # récuperation des commentaires sur la demande
  print(context['commentaires'])

  return render(request, "demande_auto/demande_detail.html", context)


def create(request):
    """ Vue de création d'une nouvelle demande d'autorisation """
    context = {}
    form = CreateDemandeForm() # initialisation du formulaire
    form.fields['organisation'].queryset = Enregistrement.objects.filter(user=request.user) # filtrage des organisations affichées (uniquement celles de l'utilisateur)

    """ rendered_form = form.render('forms/multisteps_form.html', context={'form': form, 'form_structure': FORM_STRUCTURE}) """

    if request.method == 'POST':
      form = CreateDemandeForm(request.POST)
      if form.is_valid():
        form.cleaned_data['user'] = request.user # assignation de l'utilisateur
        form.cleaned_data['status'] = Status.objects.get(label='brouillon') # ajout du statut par défaut (brouillon)

        demande = None # initialisation de la demande
        # instantiation du modèle approprié en fonction du type de la demande
        if form.cleaned_data['type_demande'] == DemandeAutoTraitement.get_type_demande():
           demande = DemandeAutoTraitement.objects.create(**form.cleaned_data)
        
        if form.cleaned_data['type_demande'] == DemandeAutoTransfert.get_type_demande():
           demande = DemandeAutoTransfert.objects.create(**form.cleaned_data)

        if form.cleaned_data['type_demande'] == DemandeAutoVideo.get_type_demande():
           demande = DemandeAutoVideo.objects.create(**form.cleaned_data)

        if form.cleaned_data['type_demande'] == DemandeAutoBiometrie.get_type_demande():
           demande = DemandeAutoBiometrie.objects.create(**form.cleaned_data)

        save_historique(demande, 'creation', request.user) # création de l'historique

        return redirect('dashboard:demande_auto:edit', pk=demande.id)        

    types_demandes = TypeDemandeAuto.objects.all() # récupération des types demandes
    context['form'] = form
    context['types_demandes'] = types_demandes
    
    return render(request, 'demande_auto/nouvelle_demande.html', context=context)


def update(request, pk):
  """ Vue de modification d'une demande d'autorisation """

  if request.method == 'POST':
    context = get_form_context(pk, request) # récupération du contexte avec la requête associée
    if context['raw_form'].is_valid(): # si le formulaire est valide
      context['raw_form'].save() # sauvegarde de la modification
      messages.success(request, 'La demande a bien été enregistrée.')
      return redirect('dashboard:demande_auto:edit', pk=context['demande'].id)
    
    else:
      print('form not valid')
      print(context['raw_form'].errors)
      messages.error(request, 'La demande n\'a pas pu être enregistrée. Veuillez vérifier les données du formulaire et réessayer.')
      return render(request, "demande_auto/demande_edit.html", context)

  context = get_form_context(pk) # récupération du contexte sans requête associée
  return render(request, "demande_auto/demande_edit.html", context)


########## Class Based Views ###########

class DemandeListView(ListView):
  """ Liste des demandes d'autorisation """
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


######## TO DELETE ###########@

"""
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
 """ 


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


"""
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
"""