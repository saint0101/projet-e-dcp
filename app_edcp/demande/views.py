from django.db.models import Max, Q
from django.shortcuts import redirect, render, get_object_or_404
from options.models import Status
from base_edcp.models import User, GroupExtension
from demande.models import Demande, ValidationDemande
from demande.forms import ValidateForm

# Create your views here.
def demandes_all(request):
  """Affiche la liste des demandes """
  niv_validation = get_niv_validation_max(request.user)
  context = {'demandes': Demande.objects.all()}
  context['user_niv_validation'] = niv_validation

  return render(request, 'demande/demande_list_all.html', context)


def demandes_a_traiter(request):
  """Affiche la liste des demandes à traiter"""
  demandes = None
  print('get_niv_validation_max : ', user_get_niv_validation(request.user))

  if get_niv_validation_max(request.user) == 0:
    demandes = Demande.objects.filter(Q(analyse=None) | Q(analyse__niv_validation=0))

  if get_niv_validation_max(request.user) == 1:
    demandes = Demande.objects.filter(Q(analyse=None) | Q(analyse__niv_validation__in=[0, 1]))
    
  elif get_niv_validation_max(request.user) > 1:
    niv_validations = user_get_niv_validation(request.user)
    for niv in niv_validations:
      print('niv : ', niv)
    demandes = Demande.objects.filter(analyse__niv_validation__in=niv_validations)
  
  context = {'demandes': demandes}
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
          analyse.status, created = Status.objects.get_or_create(label=f'analyse_attente_validation_{next_level}', defaults={'description': 'En attente de validation niv. ' + next_level})
        
        if niv_validation_actuel == niv_validation_requis:
          analyse.status, created = Status.objects.get_or_create(label='traitement_termine', defaults={'description': 'Traitement terminé'})
      
      else:
        analyse.niv_validation = 0
        analyse.is_locked = False
        analyse.status, created = Status.objects.get_or_create(label='analyse_attente_corrections', defaults={'description': 'Analyse en attente de corrections'})

      analyse.save()

      return redirect('dashboard:demande:liste_a_traiter') 
  pass