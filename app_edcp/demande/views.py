from django.db.models import Max
from django.shortcuts import redirect, render, get_object_or_404
from options.models import Status
from base_edcp.models import User, GroupExtension
from demande.models import Demande, ValidationDemande
from demande.forms import ValidateForm

# Create your views here.
def demandes_all(request):
  """Affiche la liste des demandes à traiter"""
  demandes = Demande.objects.all()
  context = {'demandes': demandes, 'show': 'all'}

  return render(request, 'demande/demande_list_all.html', context)


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
          analyse.status, created = Status.objects.get_or_create(label=f'analyse_attente_validation_{next_level}', defaults={'description': 'Analyse terminée'})
        
        if niv_validation_actuel == niv_validation_requis:
          analyse.status, created = Status.objects.get_or_create(label='analyse_terminee', defaults={'description': 'Analyse terminée'})
      
      else:
        analyse.niv_validation = 0
        analyse.status, created = Status.objects.get_or_create(label='analyse_attente_corrections', defaults={'description': 'Analyse en attente de corrections'})

      analyse.save()

      return redirect('dashboard:demande:list_all') 
  pass