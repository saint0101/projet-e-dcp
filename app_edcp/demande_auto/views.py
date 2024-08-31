from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView

# CommentaireForm, CreateDemandeForm, UpdateDemandeForm, UpdateDemandeTraitementForm, UpdateDemandeTransfertForm, UpdateDemandeVideoForm, UpdateDemandeBioForm
from .forms_structures import FORM_STRUCTURE_TRAITEMENT, FORM_STRUCTURE_TRANSFERT, FORM_STRUCTURE_VIDEO, FORM_STRUCTURE_BIOMETRIE
from base_edcp.models import Enregistrement
from demande.views import save_historique
from demande.models import CategorieDemande, Status, Commentaire, AnalyseDemande, HistoriqueDemande, ActionDemande
from demande.forms import CommentaireForm
from .models import (
  DemandeAuto, 
  DemandeAutoTraitement, 
  DemandeAutoTransfert, 
  DemandeAutoVideo, 
  DemandeAutoBiometrie,
  TypeDemandeAuto,
  SousFinalite)
from .forms import (
  CreateDemandeForm, 
  ChangeStatusForm, 
  UpdateDemandeForm,
  UpdateDemandeTraitementForm,
  UpdateDemandeTransfertForm,
  UpdateDemandeVideoForm,
  UpdateDemandeBioForm,
  AnalyseDemandeForm)

######## Fonctions utilitaires ########


def get_sous_finalites(request, pk):
  """ Vue qui renvoie la liste des sous-finalités pour une finalité sélectionnée, en JSON 
  Paramètres :
  -- request - l'objet requête.
  -- pk - id de la sous finalité. NE PAS SUPPRIMER MEME SI INUTILISE.
  """
  # si la requête est une requête AJAX
  if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
    id_finalite = request.GET.get('id_finalite') # récupération de l'ID de la finalité dans la requête
    if id_finalite and int(id_finalite) > 0:
      sous_finalites = SousFinalite.objects.filter(finalite_id=int(id_finalite)).values('id', 'label') # récupération des sous-finalités
      return JsonResponse({'sousFinalites': list(sous_finalites)}) # renvoi les sous finalités au format JSON

    return JsonResponse({'sousFinalites': []})

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
  demande = context['demande']
  form_comment = CommentaireForm() # initialisation du formulaire de commentaire
  form_status = ChangeStatusForm(initial={'status': demande.status}) # initialisation du formulaire de changement de status

  # si une requête a été soumise
  if request.method == 'POST':
    # si la requête est un ajout de commentaire
    # avec ou sans suspension de la demande
    """ if 'form_comment_submit' in request.POST or 'form_comment_submit_suspend' in request.POST:
      form_comment = CommentaireForm(request.POST) # récupération des données du formulaire
      if form_comment.is_valid():
        # si le formulaire est valide, sauvegarde du commentaire
        commentaire = form_comment.save(commit=False)
        commentaire.demande = context['demande']
        commentaire.auteur = request.user
        # si l'agent a cliqué sur 'envoyer et suspendre la demande'
        if 'form_comment_submit_suspend' in request.POST:
          context['demande'].status = Status.objects.get(label='attente_complement') # suspension de la demande
          context['demande'].save()
          save_historique(context['demande'], 'changement_statut', request.user)
        commentaire.save() 
        form_comment = CommentaireForm()
      else:
        # context['form_comment'] = form_comment
        print('erreur : ', form_comment.errors)
        messages.error(request, f'{form_comment.errors}')
     """
    if 'form_status_submit' in request.POST:
      form_status = ChangeStatusForm(request.POST) # instanciation du formulaire
      if form_status.is_valid():
        demande.status = form_status.cleaned_data['status'] # suspension de la demande
        demande.save()
        save_historique(context['demande'], 'changement_statut', request.user)
        messages.success(request, 'Statut de la demande mis à jour')

  context['form_comment'] = form_comment # affichage du formulaire de commentaires
  context['commentaires'] = demande.get_commentaires() # récuperation des commentaires sur la demande
  context['historique'] = demande.get_historique() # récuperation de l'historique de la demande
  context['form_status'] = form_status # affichage du formulaire de changement de statut
  context['analyse_exists'] = AnalyseDemande.objects.filter(demande=context['demande']).exists() # si l'analyse a déjà commencé

  return render(request, "demande_auto/demande_detail.html", context)


def analyse(request, pk):
  """ Vue pour l'analyse d'une demande d'autorisation """
  context = get_form_context(pk) # récupération du contexte à envoyer au template
  analyse_exists = AnalyseDemande.objects.filter(demande=context['demande']).exists()
  analyse = {}
  if analyse_exists:
    analyse = AnalyseDemande.objects.get(demande=context['demande'])
    form_analyse = AnalyseDemandeForm(instance=analyse) # initialisation du formulaire d'analyse
  else:
    form_analyse = AnalyseDemandeForm()

  # si une requête a été soumise
  if request.method == 'POST':
    # si la requête est un ajout de commentaire
    if 'form_analyse_submit' in request.POST:
      if analyse_exists:
        form_analyse = AnalyseDemandeForm(request.POST, instance=analyse)
      else:
        form_analyse = AnalyseDemandeForm(request.POST) # récupération des données du formulaire
      if form_analyse.is_valid():
        # si le formulaire est valide, sauvegarde de l'analyse
        analyse = form_analyse.save(commit=False)
        analyse.demande = context['demande']
        analyse.agent = request.user
        analyse.status = Status.objects.get(label='analyse_en_cours')
        # changement du status de la demande si un des avis a été donné
        if analyse.avis_juridique and not analyse.avis_technique :
          analyse.status = Status.objects.get(label='attente_analyse_technique')

        if analyse.avis_technique and not analyse.avis_juridique :
          analyse.status = Status.objects.get(label='attente_analyse_juridique')
        
        if analyse.avis_juridique and analyse.avis_technique :
          analyse.status = Status.objects.get(label='analyse_terminee')

        analyse.save() 
        messages.success(request, 'Analyse enregistrée.')
        return redirect('dashboard:demande_auto:detail', pk=pk)
        # form_comment = CommentaireForm()
      else:
        # context['form_comment'] = form_comment
        print('erreur : ', form_analyse.errors)
        messages.error(request, f'{form_analyse.errors}')

  context['form_analyse'] = form_analyse # affichage du formulaire de commentaires
  context['show_form_analyse'] = True
  context['analyse'] = analyse

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
        form.cleaned_data['created_by'] = request.user # assignation de l'utilisateur
        form.cleaned_data['status'], created = Status.objects.get_or_create(label='brouillon', defaults={'description': 'Brouillon de la demande d’autorisation'})
        form.cleaned_data['categorie'], created = CategorieDemande.objects.get_or_create(label='demande_autorisation', defaults={'description': 'Demande d\'autorisation'})

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

        # demande.status, created = Status.objects.get_or_create(label='demande_attente_traitement')
        # demande.categorie, created = CategorieDemande.objects.get_or_create(label='demande_autorisation')
        # demande.save()
        if demande:
          demande.save_historique('creation', request.user, demande.status)
        #save_historique(demande, 'creation', request.user) # création de l'historique

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
      update_data = context['raw_form'].cleaned_data
      print('update data : ', update_data)
      context['raw_form'].save() # sauvegarde de la modification
      messages.success(request, 'La demande a bien été enregistrée.')

      # si l'utilisateur a cliqué sur 'enregistrer et quitter', retour à la vue de détail
      if 'form_submit_quit' in request.POST:
        return redirect('dashboard:demande_auto:detail', pk=context['demande'].id)
      else:
        return redirect('dashboard:demande_auto:edit', pk=context['demande'].id)
    
    else:
      print('form not valid')
      print(context['raw_form'].errors)
      messages.error(request, 'La demande n\'a pas pu être enregistrée. Veuillez vérifier les données du formulaire et réessayer.')
      return render(request, "demande_auto/demande_edit.html", context)

  context = get_form_context(pk) # récupération du contexte sans requête associée
  return render(request, "demande_auto/demande_edit.html", context)



def submit_demande(request, pk):
  """ Soumission d'une demande d'autorisation """
  demande = get_object_or_404(DemandeAuto, pk=pk)
  demande.status, created = Status.objects.get_or_create(label='demande_attente_traitement', defaults={'description': 'En attente de traitement'})
  demande.is_locked = True # verrouillage de la demande pour empâcher les modifications
  demande.save()
  demande.save_historique(action_label='changement_statut', user=request.user, status=demande.status)
  # demande.notify_by_email()
  return redirect('dashboard:demande_auto:edit', pk=demande.id)


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


class demandeUpdateView(UpdateView):
  model = DemandeAuto
  # fields = '__all__'
  form_class = UpdateDemandeForm
  template_name = 'demande_auto/demande_edit.html'
  context_object_name = 'demande'
  context_form_structure = []

  def get_object(self, queryset=None):
    object = super().get_object(queryset=queryset)

    if object.type_demande.label == 'traitement':
      print ('update traitement')
      self.context_form_structure = FORM_STRUCTURE_TRAITEMENT
      self.model = DemandeAutoTraitement
      self.form_class = UpdateDemandeTraitementForm

    if object.type_demande.label == 'transfert':
      print ('update transfert')
      self.context_form_structure = FORM_STRUCTURE_TRANSFERT
      self.model = DemandeAutoTransfert
      self.form_class = UpdateDemandeTransfertForm

    if object.type_demande.label == 'videosurveillance':
      print ('update videosurveillance')
      self.context_form_structure = FORM_STRUCTURE_VIDEO
      self.model = DemandeAutoVideo
      self.form_class = UpdateDemandeVideoForm

    if object.type_demande.label == 'biometrie':
      print ('update biometrie')
      self.context_form_structure = FORM_STRUCTURE_BIOMETRIE
      self.model = DemandeAutoBiometrie
      self.form_class = UpdateDemandeBioForm

    # Now, call the original get_object method
    return object
  
  """def get_form(self, form_class=None):
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
    return rendered_form"""


  def get_form(self, form_class=None):
    form = super().get_form(form_class)
    rendered_form = form.render('forms/multisteps_form.html', context={'form': form, 'form_structure': self.context_form_structure})
    return rendered_form


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    form = super().get_form()
    rendered_form = form.render('forms/multisteps_form.html', context={'form': form, 'form_structure': self.context_form_structure})

    context['rendered_form'] = rendered_form
    context['historique'] = HistoriqueDemande.objects.filter(demande=self.object)
    context['form_structure'] = self.context_form_structure
    return context
 


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