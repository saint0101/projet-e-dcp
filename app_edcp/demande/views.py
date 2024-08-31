import json
import base64
from datetime import datetime
# django
from django.db.models import Max, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
# apps
from base_edcp.models import User, GroupExtension
from base_edcp.emails import send_email, send_email_with_attachment, MAIL_CONTENTS
from base_edcp.pdfs import generate_pdf, PDF_TEMPLATES
from options.models import Status
from demande.models import (
  Demande, 
  CategorieDemande,
  ValidationDemande, 
  HistoriqueDemande,
  ReponseDemande,
  CritereEvaluation, ActionDemande, Commentaire, TypeReponse, AnalyseDemande
)
from demande.forms import ProjetReponseModelForm, ProjetReponseForm, ValidateForm, CommentaireForm, generate_analyse_form

## Functions

""" TO DELETE """
def test_pdf(request):
  return render(request, 'pdfs/correspondant/test_pdf.html')


def get_demande_url(demande):
  """ Renvoie l'url de la page de la demande, en fonction de sa catégorie. """
  
  if demande.categorie.label == 'designation_dpo': # si désignation de correspondant
      return 'dashboard:correspondant:'
  
  if demande.categorie.label == 'demande_autorisation': # si demande d'autorisation
      return 'dashboard:demande_auto:'


def user_has_niv_validation(user, required_level):
  """ Renvoie True si l'utilisateur a le niveau de validation requis. #IA generated """
  # Get all groups the user belongs to
  user_groups = user.groups.all() 
  # Filter GroupExtension instances by the user's groups and the required validation level
  matching_groups = GroupExtension.objects.filter(group__in=user_groups, niv_validation=required_level)
  # Check if there are any matching groups
  return matching_groups.exists()


def user_get_niv_validation(user):
  """ Renvoie la liste des niveaux de validation de l'utilisateur. #IA generated """
 
  user_groups = user.groups.all() # Get all groups the user belongs to
  group_extensions = GroupExtension.objects.filter(group__in=user_groups) # Filter GroupExtension instances by the user's groups and the required validation level

  # Création de la liste des niveaux de validation
  return group_extensions.values_list('niv_validation', flat=True)


def get_niv_validation_max(user):
  """ Retourne le plus haut niveau de validation de l'utilisateur selon les différents groupes auxquels il appartient. #IA generated """
  user_groups = user.groups.all() # Get all groups the user belongs to
  group_extensions = GroupExtension.objects.filter(group__in=user_groups) # Get all GroupExtension instances for these groups

  # Find the maximum validation_level
  if group_extensions.exists():
    niveau_max = group_extensions.aggregate(niveau_max=Max('niv_validation'))['niveau_max']
    return niveau_max
  
  else:
    return 0  # or a default value like 0 if no group extension is found


def can_validate(user, demande):
    """ Renvoie True si l'utilisateur a le niveau nécessaire pour valider une demande. """
    niv_validation = get_niv_validation_max(user)
    return niv_validation >= demande.analyse.niv_validation


def can_terminate(user, demande):
    """ Renvoie True si l'utilisateur a le niveau nécessaire pour terminer une demande. """
    niv_validation = get_niv_validation_max(user)
    return niv_validation == demande.categorie.niv_validation



### VUES

def demandes_all(request):
  """Affiche la liste des demandes """
  niv_validation = get_niv_validation_max(request.user) # récupération du niveau de validation de l'utilisateur
  context = {'demandes': Demande.objects.exclude(status__label='brouillon').order_by('-created_at')} # récupération de la liste des demandes, de la plus récente à la plus ancienne
  context['user_niv_validation'] = niv_validation

  return render(request, 'demande/demande_list_all.html', context)


def demandes_a_traiter(request):
  """
  Affiche la liste des demandes à traiter.
  Seuls les 'agents' et 'superviseurs' peuvent traiter les demande.
  Le superviseur peut traiter les demandes et valider celles de niveau 1.
  Les autres proifils (validateurs 1 à 5) ne peuvent que valider les analyses et projets de réponse.
  """
  demandes = None
  niv_validation = get_niv_validation_max(request.user)
  print('get_niv_validation_max : ', user_get_niv_validation(request.user))

  # si l'utilisateur est un agent (niveau 0)
  if niv_validation == 0:
    # filtrage des demandes : sans analyse (None) ou analyse en cours (analyse niveau 0)
    demandes = Demande.objects.filter(Q(analyse=None) | Q(analyse__niv_validation=0)).exclude(status__label='brouillon').order_by('-created_at')

  # si l'utilisateur est un superviseur (niveau 1)
  if niv_validation == 1:
    # filtrage des demandes : sans analyse (None) ou analyse en cours ou à valider (analyse niveau 0 ou 1)
    demandes = Demande.objects.filter(Q(analyse=None) | Q(analyse__niv_validation__in=[0, 1])).exclude(status__label='brouillon').order_by('-created_at')

  # si l'utilisateur est un validateur (niveau 2 à 5)  
  elif niv_validation > 1:
    niv_validations = user_get_niv_validation(request.user)
    # filtrage des demandes avec les niveau de validation de l'utilisateur
    demandes = Demande.objects.filter(analyse__niv_validation__in=niv_validations).exclude(status__label='brouillon').order_by('-created_at')
  
  context = {'demandes': demandes}
  context['user_niv_validation'] = niv_validation

  return render(request, 'demande/demande_list_all.html', context)


def mes_demandes(request):
  """ Affiche la liste des demandes de l'utilisateur. """
  demandes = Demande.objects.filter(created_by=request.user).order_by('-created_at')
  context = {'demandes': demandes}
  return render(request, 'demande/mes_demandes.html', context)



def analyse_demande(request, pk, action=None):
  """ Vue d'analyse de la demande """
  object = get_object_or_404(Demande, pk=pk)
  demande, form_demande = object.get_form_and_instance()
  analyse = demande.analyse
  AnalyseDemandeForm = generate_analyse_form(demande.categorie, analyse)
	
	# si aucune analyse n'a encore été créée pour cette demande
  if not analyse :
    status_brouillon, created = Status.objects.get_or_create(label='brouillon', defaults={'description': 'Brouillon'})
    status_encours, created = Status.objects.get_or_create(label='analyse_en_cours', defaults={'description': 'Analyse en cours'})
    # action_changement, created = ActionDemande.objects.get_or_create(label='changement_statut', defaults={'description': 'Changement de statut'})

    # création de l'analyse
    analyse = AnalyseDemande.objects.create(created_by=request.user, status=status_brouillon)
    demande.analyse = analyse
    demande.status = status_encours
    demande.save()
    demande.save_historique(action_label='changement_statut', user=request.user)

	# si le formulaire d'analyse a été envoyé
  if request.method == 'POST':
    form = AnalyseDemandeForm(request.POST)
    if form.is_valid():
      form_data = form.cleaned_data

      # enregistrement de l'analyse
      analyse.observations = form.cleaned_data['observations']
      analyse.prescriptions = form.cleaned_data['prescriptions']
      analyse.avis_juridique = form.cleaned_data['avis_juridique']
      analyse.updated_at = datetime.now()
      analyse.updated_by = request.user

      # enregistrement de l'évaluation. Ce champ est stocké sous forme de texte sérialisé (JSON)
      evaluation = {}
      # pour chaque critère d'évaluation défini pour cette catégorie de demande, si le champ est renseigné, il est enregistré
      for field in CritereEvaluation.objects.filter(categorie_demande=demande.categorie):
          if field.label in form_data.keys() :
            evaluation[field.label] = form_data[field.label]
      serialized_data = json.dumps(evaluation) # conversion en JSON
      # print('serialized_data : ', serialized_data)
      analyse.evaluation = serialized_data # enregstrement du champ

      analyse.save()
      return redirect(f'{demande.get_url_name()}:analyse', pk=pk)

  form = AnalyseDemandeForm(initial=analyse.__dict__) # initialisation du formulaire d'analyse

  # initialisation du formulaire d'affichage du DPO en fonction de son type
  # form_demande = demande.get_instance_form()
  # print('form_demande : ', form_demande)

  form_projet_reponse = ProjetReponseModelForm(demande=demande) # initialisation du formulaire de projet de reponse

  form_comment = CommentaireForm() # initialisation du formulaire de commentaires
  # préparation du contexte
  context = {
    'form': form,
    'form_demande': form_demande,
    'form_comment': form_comment,
    'form_projet_reponse': form_projet_reponse,
    'demande': demande,
    'analyse': analyse,
    'can_validate': can_validate(request.user, demande),
    'can_terminate': can_terminate(request.user, demande),
    'commentaires': demande.get_commentaires(),
    'historique': demande.get_historique(),
    'validations': analyse.validations.all(),
    'action': action,
  }  

	# si l'action est une validation de demande
  if action == 'validate': 
    form_validation = ValidateForm()
    context['form_validation'] = form_validation

  # Si un projet de réponse existe pour cette demande
  if demande.analyse.projet_reponse:
    pdf_path = demande.analyse.projet_reponse.fichier_reponse.path # récupération de l'adresse du fichier
    with open(pdf_path, 'rb') as pdf_file: # ouverture du fichier PDF
      # Convert pdf to a string
      pdf_content = base64.b64encode(pdf_file.read()).decode()
      context['projet_reponse_pdf'] = pdf_content

  return render(request, 'demande/demande_analyse.html', context=context)


def submit_analyse(request, pk):
  pass


def handle_validation(request, pk):
  """ Traitement de la validation d'une demande. """
  if request.method == 'POST':
    form = ValidateForm(request.POST)
    if form.is_valid():
      demande = get_object_or_404(Demande, pk=pk)
      niv_validation_requis = demande.categorie.niv_validation # niveau de validation requis pour cette catégorie de demande
      niv_validation_actuel = get_niv_validation_max(request.user) # niveau de validation de l'utilisateur actuel
      analyse = demande.analyse
      
      # si l'utilisateur a validé l'analyse, l'avis est mis à True sinon False 
      if 'submit_form_accept' in request.POST :
        avis = True
      elif 'submit_form_reject' in request.POST :
        avis = False
      
      # enregistrement de la validation
      validation = ValidationDemande.objects.create(
        created_by=request.user,
        niveau_validation = niv_validation_actuel,
        observations=form.cleaned_data['observations'],
        avis=avis
      )
      analyse.validations.add(validation)

      # Si l'avis est positif
      if avis:
        analyse.niv_validation = niv_validation_actuel # mise à jour du niveau de validation de l'analyse
        
        # si l'analyse n'a pas encore atteint le niveau requis
        if niv_validation_actuel < niv_validation_requis: 
          next_level = niv_validation_actuel + 1 
          analyse.niv_validation = next_level # incrémentation du niveau de validation
          # mise à jour du statut de l'analyse avec le niveau de validation attendu
          analyse.status, created = Status.objects.get_or_create(label=f'analyse_attente_validation_{next_level}', defaults={'description': 'En attente de validation niv. ' + str(next_level)})
        
        # si l'analyse a atteint le niveau de validation requis
        if niv_validation_actuel == niv_validation_requis:
          # l'analyse est marquée comme terminée
          analyse.is_closed = True
          analyse.status, created = Status.objects.get_or_create(label='analyse_terminee', defaults={'description': 'Analyse terminée'}) 
          demande.status, created = Status.objects.get_or_create(label='traitement_termine', defaults={'description': 'Traitement terminé'}) 

          """ A modifier """
          demande.reponse_ok = demande.analyse.avis_juridique 
          
          mail_context = {
            'demande': demande,
          }
          send_email_with_attachment(
            request=request, 
            mail_content=MAIL_CONTENTS['correspondant_approbation_reponse'], 
            recipient_list=[demande.organisation.email_contact, request.user.email], # à compléter
            context=mail_context
          ) 
      
      # sinon si l'avis est négatif
      else:
        analyse.niv_validation = 0 # retour de l'analyse au niveau 0
        analyse.is_locked = False # déverrouillage de l'analyse pour qu'elle puisse être modifiée
        analyse.status, created = Status.objects.get_or_create(label='analyse_attente_corrections', defaults={'description': 'Analyse en attente de corrections'})

      analyse.save()
      demande.save()
      demande.save_historique(action_label='changement_statut', user=request.user, status=analyse.status, is_private=True)

      return redirect('dashboard:demande:liste_a_traiter') 


def add_commentaire(request, pk):
  """ 
  Ajout de commentaire à la demande.
  Valable pour les gestionnaires et les usagers.
  """
  demande = get_object_or_404(Demande, pk=pk)
  context = {}
  
  if request.method == 'POST':
    form_comment = CommentaireForm(request.POST) # récupération des données du formulaire
    
    # si le formulaire est valide, sauvegarde du commentaire
    if form_comment.is_valid():
      commentaire = form_comment.save(commit=False)
      commentaire.demande = demande
      commentaire.auteur = request.user

      # si l'agent a cliqué sur 'envoyer et suspendre la demande', le staut de la demande est mis à jour
      if 'form_comment_submit_suspend' in request.POST:
        demande.status = Status.objects.get(label='demande_attente_complement') # suspension de la demande
        demande.save()
        messages.success(request, 'Statut de la demande mis à jour.')

      commentaire.save() # enregistrement du commentaire
      demande.save_historique('commentaires', request.user, demande.status)
      messages.success(request, 'Message envoyé.')


    # sinon si le formulaire n'est pas valide, affichage des erreurs  
    else:
      # context['form_comment'] = form_comment
      print('erreur : ', form_comment.errors)
      messages.error(request, f'{form_comment.errors}')

  context['demande'] = demande
  context['commentaires'] = demande.get_commentaires()
  context['messages'] = messages.get_messages(request)
  return render(request, 'demande/commentaires_list.html', context=context)
  # return HttpResponse('Ok')


def add_commentaire_old(request, pk):
  """ 
  Ajout de commentaire à la demande.
  Valable pour les gestionnaires et les usagers.
  """
  demande = get_object_or_404(Demande, pk=pk)
  context = {}
  
  if request.method == 'POST':
    form_comment = CommentaireForm(request.POST) # récupération des données du formulaire
    
    # si le formulaire est valide, sauvegarde du commentaire
    if form_comment.is_valid():
      commentaire = form_comment.save(commit=False)
      commentaire.demande = demande
      commentaire.auteur = request.user

      # si l'agent a cliqué sur 'envoyer et suspendre la demande', le staut de la demande est mis à jour
      if 'form_comment_submit_suspend' in request.POST:
        demande.status = Status.objects.get(label='demande_attente_complement') # suspension de la demande
        demande.save()

      commentaire.save() # enregistrement du commentaire
      demande.save_historique('commentaires', request.user, demande.status)

    # sinon si le formulaire n'est pas valide, affichage des erreurs  
    else:
      # context['form_comment'] = form_comment
      print('erreur : ', form_comment.errors)
      messages.error(request, f'{form_comment.errors}')
  
  # calcul de l'URL de redirection
  url_parameter = 'analyse' if request.user.is_staff else 'detail' # si l'utilisateur est un usager, redirection vers la page de détail sinon celle d'analyse
  url = get_demande_url(demande) + url_parameter
  print ('demande url : ', url)

  return redirect(url, pk=demande.pk, action='show_comments') # paramètre show_comments utilisé pour déclencher l'affichage des commentaires (masqués par défaut)



def generate_response(request, pk, template):
  """ Vue de génération du projet de réponse. """

  if request.method == 'POST':
    form = ProjetReponseForm(request.POST)
    
    if form.is_valid():
      demande = get_object_or_404(Demande, pk=pk)
      url_path = get_demande_url(demande) + 'detail' # url de la page de détail de la demande. utilisée pour la génération du QR code
      # préparation du contexte avec les éléments à afficher dans le projet de réponse
      context = {
          'pk': pk,
          'demande': demande,
          'url_path': url_path,
          'type_reponse': form.cleaned_data['type_reponse'],
          'titre_destinataire': form.cleaned_data['titre_destinataire'],
          'adresse_destinataire': form.cleaned_data['adresse_destinataire'],
      }
      pdf_file = generate_pdf(request, PDF_TEMPLATES[template], context) # génération du fichier PDF
      
      # si un projet de réponse existe déjà, il est utilisé sinon un projet de réponse est créé
      if demande.analyse.projet_reponse:
        projet_reponse = demande.analyse.projet_reponse
      else :
        projet_reponse = ReponseDemande.objects.create()
      
      # enregistrement du projet de réponse
      projet_reponse.fichier_reponse.save(f'projet_reponse_{template}.pdf', pdf_file)
      projet_reponse.intitule = 'Lettre d\'approbation'
      projet_reponse.save()
      # mise à jour de l'analyse
      demande.analyse.projet_reponse = projet_reponse
      demande.analyse.save()

      messages.success(request, 'Projet de réponse généré.')

  return redirect('dashboard:correspondant:analyse', pk=pk)


def delete_demande(request, pk):
  if request.method == 'DELETE':
    demande = get_object_or_404(Demande, pk=pk)

    if not demande.created_by == request.user:
      messages.error(request, 'Vous n\'avez pas l\'autorisation de supprimer cette demande.') 

    if demande.status and not demande.status.label == 'brouillon' or demande.is_locked:
      messages.error(request, 'Vous ne pouvez pas supprimer une demande en cours de traitement ou déjà traitée.')
    
    if demande.status and demande.status.label == 'brouillon' and not demande.is_locked:
      nb_deleted, entries_deleted = demande.delete()
      if nb_deleted > 0:
        messages.success(request, f'Demande "{demande}" supprimée.')
      else:
        messages.error(request, f'Impossible de supprimer la demande "{demande}".')

    demandes = Demande.objects.filter(created_by=request.user).order_by('-created_at')
    context = {'demandes': demandes}
    return render(request, 'demande/partials/list_demandes_user.html', context=context)
  
  return HttpResponse('Bad request.')
       
    



""" TO DELETE (déplacé dans le modèle Demande)"""
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
