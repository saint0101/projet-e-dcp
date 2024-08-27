import json
from multiprocessing import context
# import secrets
# from traceback import format_list
# from django.forms import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.exceptions import PermissionDenied
# from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
import os
from django import forms
from options.models import Status
#from django.core.files.storage import FileSystemStorage
# from datetime import datetime
# from formtools.wizard.views import SessionWizardView
from .models import Correspondant, DesignationDpoMoral, TypeDPO
from .forms import DPOCabinetFormDisabled, DPODPOUpdateFormDisabled, DPOFormPage1, DPOCabinetForm, UserIsDPOForm, generate_analyse_form, DPOUpdateForm #, AnalyseDPOForm
from base_edcp.models import User, Enregistrement
# from connexion.forms import UserRegistrationForm
from user.utils import create_new_user, check_email
from base_edcp.emails import MAIL_CONTENTS, send_email
from demande.models import ActionDemande, AnalyseDemande, CategorieDemande, Commentaire, CritereEvaluation, HistoriqueDemande, ReponseDemande
from demande.forms import CommentaireForm, ValidateForm
from demande_auto.models import EchelleNotation
from datetime import datetime
from base_edcp.pdfs import generate_pdf, PDF_TEMPLATES
import base64

# Create your views here.

# user/views.py
def index(request):
    """
    Vue index correspondant du tableau de bord client.
    Affiche la liste des correspondants désignés par l'utilisateur,
    et la liste des organisations pour lesquels l'utilisateur n'a pas encore désigné de DPO.
    """
    dpos_physique = Correspondant.objects.filter(Q(user=request.user) | Q(created_by=request.user)).filter(is_personne_morale=False) # Filtre si l'utilisateur est lui-même un DPO ou s'il a désigné des DPO
    dpos_moral = Correspondant.objects.filter(created_by=request.user).filter(is_personne_morale=True)
    orgs_without_dpo = Enregistrement.objects.filter(user=request.user).filter(has_dpo=False) # Liste des organisations créées par l'utilisateur et qui n'ont pas de DPO
    context = {
        'correspondants_physique': dpos_physique,
        'correspondants_moral': dpos_moral,
        'orgs_without_dpo': orgs_without_dpo
    }

    return render(request, 'correspondant/index.html', context=context)


def approve(request, pk, approve):
    """ Vue d'approbation de correspondant """
    context = {}
    correspondant = Correspondant.objects.get(id=pk)
    # vérifie si l'utilisateur est un gestionnaire
    if request.user.is_staff: 
        # si l'action est une approbation (approve == 1)
        if approve == 1 :
            correspondant.is_approved = True
            messages.success(request, 'Correspondant approuvé.')

        # si l'action est un retrait de l'approbation (approve == 0)
        if approve == 0 :
            correspondant.is_approved = False
            messages.success(request, 'Approbation retirée.')

        # si l'action est un refus (approve == 2)
        if approve == 2 :
            correspondant.is_approved = False
            correspondant.is_rejected = True
            messages.success(request, 'Désignation refusée.')

        correspondant.save()
        # préparation du contexte pour l'envoi de l'email
        mail_context = {
            'correspondant': correspondant,
            'approved': approve
        }
        # envoi de l'email
        send_email(
            request=request, 
            mail_content=MAIL_CONTENTS['correspondant_approbation_client'], 
            recipient_list=[correspondant.created_by.email, correspondant.user.email], 
            context=mail_context,
            show_message=False
        )
    
    # si l'utilisateur n'est pas un gestionnaire
    else :
        messages.error(request, 'Vous n\'avez pas les droits pour effectuer cette action.')

    context['correspondant'] = correspondant
    return redirect('dashboard:correspondant:detail', pk=correspondant.id)


def designate(request, org):
    """
    Vue de désignation du DPO.
    Renvoie un premier formulaire pour la création du compte utilisateur du DPO,
    puis redirige vers la vue UpdateView pour l'édition du DPO créé
    """
    context = {}
    organisation = Enregistrement.objects.get(id=org) # récupération de l'organisation pour laquelle le DPO va être désigné

    # if request.is_ajax() :
    # vérifie si la requête reçue est une requête AJAX. Utilisé pour la vérification de la disponibilité de l'adresse email
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        email = request.GET.get('email')
        print(f'Ajax request received {email}')
        
        return check_email(email) # appel de la fonction de vérification de l'email et renvoi de la valeur

    # si le formulaire de création de compte utilisateur a été soumis
    if request.method == 'POST':
        form_page1 = DPOFormPage1(request.POST) # récupération des données du formulaire
        form_user_is_dpo = UserIsDPOForm(request.POST)

        # si le formulaire de choix a été soumis et est valide,
        #    l'utilisateur courant fait donc une auto-désignation
        #    le DPO est alors créé avec pour "user" l'utilisateur courant
        if 'submit_user_is_dpo_form' in request.POST and form_user_is_dpo.is_valid(): 
            dpo = Correspondant.objects.create(
                user=request.user, 
                organisation=organisation, 
                created_by=request.user, 
                categorie=CategorieDemande.objects.get(label='designation_dpo'),
                type_dpo=TypeDPO.objects.get(label='personne_physique'),
                status=Status.objects.get(label='demande_attente_traitement'),
            ) # création du DPO
            Enregistrement.objects.filter(id=org).update(has_dpo=True) # mise à jour de l'organsiation avec --> has_dpo = True
            messages.success(request, 'Le Correspondant a bien été créé.')
            dpo.save_historique(action_label='creation', user=request.user)
            return redirect('dashboard:correspondant:edit', pk=dpo.id, is_new=True) # redirection vers la vue UpdateView avec l'id du DPO créé
        
        # si le formulaire de création de compte a été soumis et est valide,
        #    l'utilisateur courant désigne quelqu'un d'autre comme DPO.
        #    le DPO est alors enregistré avec le compte nouvellement créé
        elif 'submit_designation_form' in request.POST and form_page1.is_valid(): 
            user, password = create_new_user(form_page1.cleaned_data) # appel de la fonction de création d'un nouvel utilisateur
            # si l'utilisateur a bien été créé
            if user:
                print(f'Password check : {password}')
                # envoi du mail de notification à l'utilisateur nouvellement créé
                send_email(
                    request=request,
                    mail_content=MAIL_CONTENTS['correspondant_new_compte'],
                    recipient_list=[user.email],
                    show_message=False,
                    context={
                        'user': user,
                        'organisation': organisation,
                        'password': password
                    },
                )
                dpo = Correspondant.objects.create(
                  user=user, 
                  organisation=organisation, 
                  created_by=request.user, 
                  categorie=CategorieDemande.objects.get(label='designation_dpo'),
                  type_dpo=TypeDPO.objects.get(label='personne_physique'),
                  status=Status.objects.get(label='demande_attente_traitement'),
                ) # création du DPO
                Enregistrement.objects.filter(id=org).update(has_dpo=True) # mise à jour de l'organsiation avec --> has_dpo = True

                print(f'DPO {dpo} created')
                messages.success(request, 'Le Correspondant a bien été créé.')
                dpo.save_historique(action_label='creation', user=request.user)

                """ mail_context = {
                    'correspondant': dpo,
                }
                send_email(request, MAIL_CONTENTS['correspondant_designation_client'], [dpo.user.email, request.user.email], mail_context) 
                """
                return redirect('dashboard:correspondant:edit', pk=dpo.id, is_new=True) # redirection vers la vue UpdateView avec l'id du DPO créé

            # si l'utilisateur n'a pas pu être créé
            else:
                context['errors'] = 'Une erreur est survenue lors de la creation du Correspondant.'
                context['form_page1'] = form_page1
                context['form_user_is_dpo'] = form_user_is_dpo
                return render(request, 'correspondant/designation.html', context=context)
        
        # si le formulaire de création d'utilisateur n'est pas valide
        else:
            context['errors'] = form_page1.errors # ajout des erreurs du formulaire au contexte
            context['form_page1'] = form_page1 # ajout du formulaire au contexte
            context['form_user_is_dpo'] = UserIsDPOForm(initial={'user_is_dpo': False}) # ajout du formulaire au contexte
    
    # si le formulaire de création de compte utilisateur n'a pas encore été soumis (la page vient d'être ouverte)
    else:
        form_page1 = DPOFormPage1() # initialisation du formulaire
        form_user_is_dpo = UserIsDPOForm() # initialisation du formulaire

        context['organisation'] = organisation # ajout de l'organisation au contexte
        context['form_page1'] = form_page1 # ajout du formulaire au contexte
        context['form_user_is_dpo'] = form_user_is_dpo # ajout du formulaire au contexte

    return render(request, 'correspondant/designation.html', context=context) # renvoi de la vue


def designate_cabinet(request, org):
  """
  Vue de désignation du DPO.
  Renvoie un premier formulaire pour la création du compte utilisateur du DPO,
  puis redirige vers la vue UpdateView pour l'édition du DPO créé
  """
  context = {}
  organisation = Enregistrement.objects.get(id=org) # récupération de l'organisation pour laquelle le DPO va être désigné
  form = DPOCabinetForm()

  if request.method == 'POST':
    form = DPOCabinetForm(request.POST)
    if form.is_valid():
      dpo = form.save(commit=False)
      correspondant = Correspondant.objects.create(
        user = dpo.cabinet.user,
        created_by = request.user,
        organisation = organisation,
        cabinet = dpo.cabinet,
        categorie = CategorieDemande.objects.get(label='designation_dpo'),
        is_personne_morale = True,
        type_dpo=TypeDPO.objects.get(label='personne_morale'),
        status=Status.objects.get(label='demande_attente_traitement'),
      )
      """ correspondant.organisation = organisation
      correspondant.categorie = CategorieDemande.objects.get(label='designation_dpo'),
      correspondant.created_by = request.user
      correspondant.is_personne_morale = True
      correspondant.save() """

      messages.success(request, 'La désignation du Correspondant a bien été enregistrée.')
      correspondant.save_historique(action_label='creation', user=request.user)
      
      Enregistrement.objects.filter(id=org).update(has_dpo=True) # mise à jour de l'organsiation avec --> has_dpo = True
      # send_email()
      # context
      return redirect('dashboard:correspondant:detail', pk=correspondant.id) #
    
    else:
      context['errors'] = form.errors

  context['form'] = form
  return render(request, 'correspondant/designation_cabinet.html', context=context)


def designation_detail(request, pk):
   pass


def analyse(request, pk, action=None):
  correspondant = get_object_or_404(Correspondant, pk=pk)
  analyse = correspondant.analyse
  AnalyseDPOForm = generate_analyse_form(CategorieDemande.objects.get(label='designation_dpo'), analyse)
  
  if not analyse :
    status_brouillon, created = Status.objects.get_or_create(label='brouillon', defaults={'description': 'Brouillon'})
    status_encours, created = Status.objects.get_or_create(label='analyse_en_cours', defaults={'description': 'Analyse en cours'})
    # action_changement, created = ActionDemande.objects.get_or_create(label='changement_statut', defaults={'description': 'Changement de statut'})
    
    analyse = AnalyseDemande.objects.create(created_by=request.user, status=status_brouillon)
    correspondant.analyse = analyse
    correspondant.status = status_encours
    correspondant.save()
    correspondant.save_historique(action_label='changement_statut', user=request.user)

  if request.method == 'POST':
    form = AnalyseDPOForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data

      analyse.observations = form.cleaned_data['observations']
      analyse.prescriptions = form.cleaned_data['prescriptions']
      analyse.avis_juridique = form.cleaned_data['avis_juridique']
      analyse.updated_at = datetime.now()
      analyse.updated_by = request.user

      evaluation = {}
      for field in CritereEvaluation.objects.filter(categorie_demande=CategorieDemande.objects.get(label='designation_dpo')):
          if field.label in form_data.keys() :
            evaluation[field.label] = form_data[field.label]
      serialized_data = json.dumps(evaluation)
      print('serialized_data : ', serialized_data)
      analyse.evaluation = serialized_data

      analyse.save()
      return redirect('dashboard:correspondant:analyse', pk=pk)

  form = AnalyseDPOForm(initial=analyse.__dict__)
  if correspondant.is_personne_morale:
    form_dpo = DPOCabinetFormDisabled(instance=correspondant)
  else:
    form_dpo = DPODPOUpdateFormDisabled(instance=correspondant)

  form_comment = CommentaireForm()
  context = {
    'form': form,
    'form_dpo': form_dpo,
    'form_comment': form_comment,
    'correspondant': correspondant,
    'analyse': analyse,
    'commentaires': Commentaire.objects.filter(demande=correspondant).order_by('created_at'),
    'validations': analyse.validations.all(),
    'action': action,
    'historique': HistoriqueDemande.objects.filter(demande=correspondant)
  }  

  if action == 'validate':
    form_validation = ValidateForm()
    context['form_validation'] = form_validation

  if action == 'show_comments':
    context['show_comments'] = True

  if correspondant.analyse.projet_reponse:
    pdf_path = correspondant.analyse.projet_reponse.fichier_reponse.path
    with open(pdf_path, 'rb') as pdf_file:
        # Convert pdf to a string
        pdf_content = base64.b64encode(pdf_file.read()).decode()
        context['projet_reponse_pdf'] = pdf_content

  return render(request, 'correspondant/correspondant_analyse.html', context=context)


def generate_response(request, pk):
    correspondant = get_object_or_404(Correspondant, pk=pk)
    context = {
        'pk': pk,
        'correspondant': correspondant,
        'url_path': 'dashboard:correspondant:detail',
    }
    pdf_file = generate_pdf(request, PDF_TEMPLATES['correspondant_approbation'], context)
    # print('generating pdf : ', pdf_file)
    projet_reponse = ReponseDemande.objects.create()
    projet_reponse.fichier_reponse.save('projet_reponse.pdf', pdf_file)
    projet_reponse.intitule = 'Lettre d\'approbation'
    # projet_reponse.fichier_reponse = pdf_file
    projet_reponse.save()
    correspondant.analyse.projet_reponse = projet_reponse
    correspondant.analyse.save()
    messages.success(request, 'Projet de réponse généré.')

    return redirect('dashboard:correspondant:analyse', pk=pk)


def submit_analyse(request, pk):
    correspondant = get_object_or_404(Correspondant, pk=pk)
    analyse = correspondant.analyse

    if analyse :
      status, created = Status.objects.get_or_create(
          label='attente_validation_1',
          defaults={'description': 'En attente de validation niv. 1'}    
      )
      analyse.status = status
      analyse.is_locked = True
      analyse.niv_validation = 1
      analyse.save()
      correspondant.save_historique(action_label='changement_statut', user=request.user, status=analyse.status, is_private=True)

    return redirect('dashboard:correspondant:detail', pk=pk)


class DPOUpdateCabinet(UpdateView):
  model = Correspondant
  form_class = DPOCabinetForm
  template_name = 'correspondant/correspondant_edit.html'
  context_object_name = 'correspondant'

  def get_success_url(self):
    # Redirect to the detail view of the created object
    messages.success(self.request, 'Désignation du correspondant mise à jour.')
    return reverse('dashboard:correspondant:detail', kwargs={'pk': self.object.pk})
    


class DPOUpdateView(UpdateView):
  model = Correspondant
  """ fields = [
      'is_active',
      'qualifications', 
      'exercice_activite', 
      'moyens_dpo', 
      'experiences',
      'file_lettre_designation',
      'file_lettre_acceptation',
      'file_attestation_travail',
      'file_casier_judiciaire',
      'file_certificat_nationalite',
      'file_cv',
  ] """
  form_class = DPOUpdateForm
  template_name = 'correspondant/correspondant_edit.html'
  context_object_name = 'correspondant'
  
  def form_valid(self, form):
      """Méthode appelée lorsque le formulaire est valide"""
      obj = form.save(commit=False) # Sauvegarde l'objet avec les données du formulaire, sans le valider encore
      obj.profile_completed = True # Marque le profil comme complet
      response = super().form_valid(form) # Sauvegarde l'objet en appelant la méthode de la classe parente
      self.object = obj # Définit l'objet sauvegardé pour les actions post-sauvegarde
      
      messages.success(self.request, 'Informations enregistrées avec succès.')

      # s'il s'agit d'une nouvelle désignation de correspondant
      if self.kwargs.get('is_new'):
          # notification du correspondant et de l'utilisateur qui l'a désigné
          send_email(
              request=self.request, 
              mail_content=MAIL_CONTENTS['correspondant_designation_client'], 
              recipient_list=[obj.user.email, self.request.user.email], 
              context={'correspondant': obj}
          )
          # notification de l'Autorité de Protection
          send_email(
              request=self.request, 
              mail_content=MAIL_CONTENTS['correspondant_designation_mgr'], 
              recipient_list=[settings.EMAIL_HOST_USER ], 
              context={'correspondant': obj},
              show_message=False
          )

      return response
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['is_new'] = self.kwargs.get('is_new') # permet de vérifier si le formulaire est affiché suite à la création d'un DPO
    return context

  def get_success_url(self):
    # Redirect to the detail view of the created object
    return reverse('dashboard:correspondant:detail', kwargs={'pk': self.object.pk})


class DPOListView(ListView):
    model = Correspondant
    template_name = 'correspondant/correspondant_list.html'
    context_object_name = 'correspondants'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset



def correspondant_detail(request, pk, action=None):
  template_name = 'correspondant/correspondant_detail.html'
  context = {}
  correspondant = get_object_or_404(Correspondant, pk=pk)
  if not (correspondant.created_by == request.user or correspondant.user == request.user) and not request.user.is_staff:
      raise PermissionDenied
  
  historique = HistoriqueDemande.objects.filter(demande=correspondant)
  commentaires = Commentaire.objects.filter(demande=correspondant).order_by('created_at')
  print('commentaires : ', commentaires)
  form_comment = CommentaireForm()

  context['correspondant'] = correspondant
  context['historique'] = historique
  context['commentaires'] = commentaires
  context['form_comment'] = form_comment

  if action == 'show_comments':
    context['show_comments'] = True

  return render(request, template_name, context=context)


class DPODetailView(DetailView):
    model = Correspondant
    template_name = 'correspondant/correspondant_detail.html'
    context_object_name = 'correspondant'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.filter(created_by=self.request.user)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        historique = HistoriqueDemande.objects.filter(demande=self.object)
        commentaires = Commentaire.objects.filter(demande=self.object).order_by('created_at')
        print('commentaires : ', commentaires)
        form_comment = CommentaireForm()
        
        context['historique'] = historique
        context['commentaires'] = commentaires
        context['form_comment'] = form_comment

        return context

    

"""TO DELETE"""
""" class CreateDPOWizardView(SessionWizardView):
    template_name = 'correspondant/create_dpo.html'
    # form_list = [UserRegistrationForm, DPOForm]
    # form_list = [UserDPOForm, DPOForm]
    # form_list = [CreateUserDPOForm, DPOForm]
    form_list = [DPOFormPage1, DPOFormPage2]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    def done(self, form_list, **kwargs):
        # Process the forms
        for form in form_list:
            print(form.cleaned_data)
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        }) """


"""TO DELETE"""
""" class DPOCreateView(CreateView):
    model = Correspondant
    template_name = 'correspondant/correspondant_create.html'
    # fields = ['raisonsociale', 'dpo', 'user']

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
 """


"""TO DELETE"""
""" def createDPO(request):
    context = {}
    if request.method == 'POST':
        user_form = CreateUserDPOForm(request.POST)
        dpo_form = DPOForm()
        if user_form.is_valid():
            # user_form = CreateUserDPOForm(request.POST)
            if user_form.cleaned_data['is_first_step'] == 'True':
            # if request.get('is_first_step') == 'True':
                new_user = User()
                new_user.nom = user_form.cleaned_data['nom']
                new_user.prenoms = user_form.cleaned_data['prenoms']
                new_user.email = user_form.cleaned_data['email']
                new_user.telephone = user_form.cleaned_data['telephone']
                new_user.fonction = user_form.cleaned_data['fonction']
                new_user.organisation = user_form.cleaned_data['organisation']
                new_user.password = '@dmin09MP'

                context['new_user'] = new_user
                context['is_first_step'] = False
                context['dpo_form'] = dpo_form
                
                dpo = dpo_form.save(commit=False)
                dpo.user = user
                dpo.save()
                return render(request, 'correspondant/create_dpo_new.html', context=context)
    else:
        user_form = CreateUserDPOForm()
        dpo_form = DPOForm()
        context['is_first_step'] = True
        context['user_form'] = user_form
        context['dpo_form'] = dpo_form
        
    return render(request, 'correspondant/create_dpo_new.html', context=context) """
