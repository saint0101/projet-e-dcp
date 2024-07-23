from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import Correspondant
from base_edcp.models import User, Enregistrement

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande correspondant """
    correspondants = Correspondant.objects.filter(user=request.user)
    orgs_without_dpo = Enregistrement.objects.filter(user=request.user).filter(has_dpo=False)
    context = {
        'correspondants': correspondants,
        'orgs_without_dpo': orgs_without_dpo
    }

    return render(request, 'correspondant/index.html', context=context)


class DPOListView(ListView):
    model = Correspondant
    template_name = 'correspondant/correspondant_list.html'
    context_object_name = 'correspondants'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset


class DPODetailView(DetailView):
    model = Correspondant
    template_name = 'correspondant/correspondant_detail.html'
    context_object_name = 'correspondant'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset