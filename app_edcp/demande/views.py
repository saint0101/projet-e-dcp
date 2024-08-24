from multiprocessing import context
from django.shortcuts import render
from options.models import Status
from demande.models import Demande

# Create your views here.
def demandes_all(request):
  """Affiche la liste des demandes à traiter"""
  demandes = Demande.objects.all()
  context = {'demandes': demandes, 'show': 'all'}

  return render(request, 'demande/demande_list_all.html', context)