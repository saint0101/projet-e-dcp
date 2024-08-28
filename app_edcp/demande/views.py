from django.db.models import Max, Q
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
# apps
from base_edcp.models import User, GroupExtension
from base_edcp.emails import send_email, send_email_with_attachment, MAIL_CONTENTS
from base_edcp.pdfs import generate_pdf, PDF_TEMPLATES
from options.models import Status
from demande.models import Demande, ValidationDemande, HistoriqueDemande, ActionDemande, Commentaire, ReponseDemande, TypeReponse
from demande.forms import ValidateForm, CommentaireForm, ProjetReponseForm

## Functions

""" TO DELETE """
def test_pdf(request):
  return render(request, 'pdfs/correspondant/test_pdf.html')


def get_demande_url(demande):
  """ Renvoie l'url de la page de la demande, en fonction de sa catégorie. """
  print('demandes', demande.categorie.label)
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
    return None  # or a default value like 0 if no group extension is found


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
  context = {'demandes': Demande.objects.all().order_by('-created_at')} # récupération de la liste des demandes, de la plus récente à la plus ancienne
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
    demandes = Demande.objects.filter(Q(analyse=None) | Q(analyse__niv_validation=0)).order_by('-created_at')

  # si l'utilisateur est un superviseur (niveau 1)
  if niv_validation == 1:
    # filtrage des demandes : sans analyse (None) ou analyse en cours ou à valider (analyse niveau 0 ou 1)
    demandes = Demande.objects.filter(Q(analyse=None) | Q(analyse__niv_validation__in=[0, 1])).order_by('-created_at')

  # si l'utilisateur est un validateur (niveau 2 à 5)  
  elif niv_validation > 1:
    niv_validations = user_get_niv_validation(request.user)
    # filtrage des demandes avec les niveau de validation de l'utilisateur
    demandes = Demande.objects.filter(analyse__niv_validation__in=niv_validations).order_by('-created_at')
  
  context = {'demandes': demandes}
  context['user_niv_validation'] = niv_validation

  return render(request, 'demande/demande_list_all.html', context)


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
