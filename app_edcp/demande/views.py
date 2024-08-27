from django.db.models import Max, Q
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from urllib3 import Retry
from options.models import Status
from base_edcp.models import User, GroupExtension
from base_edcp.pdfs import generate_pdf, PDF_TEMPLATES
from demande.models import Demande, ValidationDemande, HistoriqueDemande, ActionDemande, Commentaire, ReponseDemande, TypeReponse
from demande.forms import ValidateForm, CommentaireForm, ProjetReponseForm

## Functions
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

def test_pdf(request):
  return render(request, 'pdfs/correspondant/test_pdf.html')

def get_demande_url(demande):
  """ Renvoie l'url de la page de la demande, en fonction de sa catégorie. """
  print('demandes', demande.categorie.label)
  if demande.categorie.label == 'designation_dpo':
      return 'dashboard:correspondant:'
  
  if demande.categorie.label == 'demande_autorisation':
      return 'dashboard:demande_auto:'

# Create your views here.
def demandes_all(request):
  """Affiche la liste des demandes """
  niv_validation = get_niv_validation_max(request.user)
  context = {'demandes': Demande.objects.all().order_by('-created_at')}
  context['user_niv_validation'] = niv_validation

  return render(request, 'demande/demande_list_all.html', context)


def demandes_a_traiter(request):
  """Affiche la liste des demandes à traiter"""
  demandes = None
  niv_validation = get_niv_validation_max(request.user)
  print('get_niv_validation_max : ', user_get_niv_validation(request.user))

  if niv_validation == 0:
    demandes = Demande.objects.filter(Q(analyse=None) | Q(analyse__niv_validation=0)).order_by('-created_at')

  if niv_validation == 1:
    demandes = Demande.objects.filter(Q(analyse=None) | Q(analyse__niv_validation__in=[0, 1])).order_by('-created_at')
    
  elif niv_validation > 1:
    niv_validations = user_get_niv_validation(request.user)
    for niv in niv_validations:
      print('niv : ', niv)
    demandes = Demande.objects.filter(analyse__niv_validation__in=niv_validations).order_by('-created_at')
  
  context = {'demandes': demandes}
  context['user_niv_validation'] = niv_validation
  return render(request, 'demande/demande_list_all.html', context)


def user_has_niv_validation(user, required_levels):
  # Get all groups the user belongs to
  user_groups = user.groups.all()

  # Filter GroupExtension instances by the user's groups and the required validation level
  matching_groups = GroupExtension.objects.filter(group__in=user_groups, niv_validation__in=required_levels)

  # Check if there are any matching groups
  return matching_groups.exists()


def user_get_niv_validation(user):
  # Get all groups the user belongs to
  user_groups = user.groups.all()

  # Filter GroupExtension instances by the user's groups and the required validation level
  group_extensions = GroupExtension.objects.filter(group__in=user_groups)

  # Check if there are any matching groups
  return group_extensions.values_list('niv_validation', flat=True)


def get_niv_validation_max(user):
    """ Retourne le plus haut niveau de validation de l'utilisateur selon les différents groupes auxquels il appartient. """
    user_groups = user.groups.all() # Get all groups the user belongs to
    group_extensions = GroupExtension.objects.filter(group__in=user_groups) # Get all GroupExtension instances for these groups

    # Find the maximum validation_level
    if group_extensions.exists():
        niveau_max = group_extensions.aggregate(niveau_max=Max('niv_validation'))['niveau_max']
        return niveau_max
    else:
        return None  # or a default value like 0 if no group extension is found


def handle_validation(request, pk):
  """Traitement de la validation d'une demande"""
  if request.method == 'POST':
    form = ValidateForm(request.POST)
    if form.is_valid():
      demande = get_object_or_404(Demande, pk=pk)
      niv_validation_requis = demande.categorie.niv_validation
      niv_validation_actuel = get_niv_validation_max(request.user)
      analyse = demande.analyse
      if 'submit_form_accept' in request.POST :
        avis = True
      elif 'submit_form_reject' in request.POST :
        avis = False
      validation = ValidationDemande.objects.create(
        created_by=request.user,
        niveau_validation = niv_validation_actuel,
        observations=form.cleaned_data['observations'],
        avis=avis
      )
      analyse.validations.add(validation)

      # Si l'avis est positif
      if avis:
        analyse.niv_validation = niv_validation_actuel
        
        if niv_validation_actuel < niv_validation_requis:
          next_level = niv_validation_actuel + 1
          analyse.niv_validation = next_level
          analyse.status, created = Status.objects.get_or_create(label=f'analyse_attente_validation_{next_level}', defaults={'description': 'En attente de validation niv. ' + str(next_level)})
        
        if niv_validation_actuel == niv_validation_requis:
          analyse.status, created = Status.objects.get_or_create(label='traitement_termine', defaults={'description': 'Traitement terminé'})
      
      else:
        analyse.niv_validation = 0
        analyse.is_locked = False
        analyse.status, created = Status.objects.get_or_create(label='analyse_attente_corrections', defaults={'description': 'Analyse en attente de corrections'})

      analyse.save()
      demande.save_historique(action_label='changement_statut', user=request.user, status=analyse.status, is_private=True)


      return redirect('dashboard:demande:liste_a_traiter') 
  pass



def add_commentaire(request, pk):
  demande = get_object_or_404(Demande, pk=pk)
  context = {}
  if request.method == 'POST':
    form_comment = CommentaireForm(request.POST) # récupération des données du formulaire
    if form_comment.is_valid():
      # si le formulaire est valide, sauvegarde du commentaire
      commentaire = form_comment.save(commit=False)
      commentaire.demande = demande
      commentaire.auteur = request.user
      # si l'agent a cliqué sur 'envoyer et suspendre la demande'
      if 'form_comment_submit_suspend' in request.POST:
        demande.status = Status.objects.get(label='demande_attente_complement') # suspension de la demande
        demande.save()
      commentaire.save() 
      demande.save_historique('commentaires', request.user, demande.status)
    else:
      # context['form_comment'] = form_comment
      print('erreur : ', form_comment.errors)
      messages.error(request, f'{form_comment.errors}')
  
  url_parameter = 'analyse' if request.user.is_staff else 'detail'
  url = get_demande_url(demande) + url_parameter
  print ('demande url : ', url)
  return redirect(url, pk=demande.pk, action='show_comments')



def generate_response(request, pk, template):
  if request.method == 'POST':
    form = ProjetReponseForm(request.POST)
    if form.is_valid():
      demande = get_object_or_404(Demande, pk=pk)
      url_path = get_demande_url(demande) + 'detail'
      context = {
          'pk': pk,
          'demande': demande,
          'url_path': url_path,
          'type_reponse': form.cleaned_data['type_reponse'],
          'titre_destinataire': form.cleaned_data['titre_destinataire'],
          'adresse_destinataire': form.cleaned_data['adresse_destinataire'],
      }
      pdf_file = generate_pdf(request, PDF_TEMPLATES[template], context)
      # print('generating pdf : ', pdf_file)
      projet_reponse = ReponseDemande.objects.create()
      projet_reponse.fichier_reponse.save(f'projet_reponse_{template}.pdf', pdf_file)
      projet_reponse.intitule = 'Lettre d\'approbation'
      # projet_reponse.fichier_reponse = pdf_file
      projet_reponse.save()
      demande.analyse.projet_reponse = projet_reponse
      demande.analyse.save()
      messages.success(request, 'Projet de réponse généré.')

  return redirect('dashboard:correspondant:analyse', pk=pk)