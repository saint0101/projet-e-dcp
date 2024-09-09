from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from options.models import Status
from demande.models import Demande
from facturation.models import Facture, ModePaiement, Paiement
from facturation.forms import JustificatifPaiementForm

# Create your views here.



def create(request, demande_pk):
  demande = get_object_or_404(Demande, pk=demande_pk)

  if Facture.objects.filter(demande=demande).exists():
    Facture.objects.filter(demande=demande).delete()

  facture = Facture.objects.create(demande=demande)
  facture.created_by=request.user
  statut_impayee, created = Status.objects.get_or_create(label='facture_impayee', defaults={'description': 'Impayée'})
  facture.statut = statut_impayee
  facture.calcul_montant()
  facture.save()

  if facture:
    messages.success(request, 'Facture créée avec succès.')

  else:
    messages.error(request, 'Impossible de créer la facture.')

  return redirect('dashboard:demande:analyse', pk=demande_pk)


def detail_htmx(request, pk):
  facture = get_object_or_404(Facture, pk=pk)
  if facture.demande.created_by != request.user and not request.user.is_staff:
    return HttpResponse('Unauthorized', status=401)
  
  context = {
    'facture': facture
  }
  return render(request, 'facturation/partials/detail.html', context)


def create_paiement_caisse(request, pk):
  # demande = get_object_or_404(Demande, pk=demande_pk)
  facture = get_object_or_404(Facture, pk=pk)
  # paiement = Paiement(facture=facture)
  form = JustificatifPaiementForm()

  if facture.demande.created_by != request.user:
    return HttpResponse('Unauthorized', status=401)
  
  if request.method == 'POST':
    form = JustificatifPaiementForm(request.POST, request.FILES)
    
    if form.is_valid():
      """ paiement = form.cleaned_data
      paiement['facture'] = facture
      paiement['created_by'] = request.user
      paiement.save() """
      paiement = form.save(commit=False)
      paiement.facture = facture
      paiement.created_by = request.user
      paiement.mode_paiement, created = ModePaiement.objects.get_or_create(label='caisse', defaults={'description': 'Paiement à la caisse'})
      paiement.save()
      messages.success(request, 'Paiement enregistré.')
      return redirect(facture.demande.get_url_name() + ':detail', pk=facture.demande.id)
 
  context = {
    'demande': facture.demande,
    'facture': facture,
    'form': form
  }

  return render(request, 'facturation/paiement_create.html', context) 




class CreatePaiementView(CreateView):
  template_name = 'facturation/paiement_create.html'
  model = Paiement
  form_class = JustificatifPaiementForm
