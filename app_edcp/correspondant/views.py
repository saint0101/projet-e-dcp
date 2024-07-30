from multiprocessing import context
from traceback import format_list
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.db.models import Q
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from formtools.wizard.views import SessionWizardView
from .models import Correspondant
from .forms import DPOForm, UserDPOForm, CreateUserDPOForm, DPOFormPage1, DPOFormPage2
from base_edcp.models import User, Enregistrement
from connexion.forms import UserRegistrationForm

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande correspondant """
    correspondants = Correspondant.objects.filter(Q(user=request.user) | Q(created_by=request.user))
    orgs_without_dpo = Enregistrement.objects.filter(user=request.user).filter(has_dpo=False)
    context = {
        'correspondants': correspondants,
        'orgs_without_dpo': orgs_without_dpo
    }

    return render(request, 'correspondant/index.html', context=context)


def check_email(email):
    if User.objects.filter(email=email).exists():
        user=User.objects.get(email=email)
        return JsonResponse({'email_exists': True}, {'is_dpo': user.is_dpo})

    print(f'email not found : {email}')
    return JsonResponse({'email_exists': False})


def designate(request, org):
    context = {}
    organisation = Enregistrement.objects.get(id=org)

    # if request.is_ajax():
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        email = request.GET.get('email')
        print(f'Ajax request received {email}')
        return check_email(email)

    if request.method == 'POST':
        form_page1 = DPOFormPage1(request.POST)
        if form_page1.is_valid():
            new_user = User()
            new_user.nom = form_page1.cleaned_data['nom']
            new_user.prenoms = form_page1.cleaned_data['prenoms']
            new_user.telephone = form_page1.cleaned_data['telephone']
            new_user.email = form_page1.cleaned_data['email']
            new_user.password = 'pbkdf2_sha256$600000$aM8OOxx8RVXcAA8ISDbNC5$CgJsb4SLOpQgiw8SEGEsO27PR07iW8YSL2kwA6ZVV8o='
            new_user.is_dpo = True
            new_user.is_active = True 
            new_user.email_verified = False
            new_user.save()

            user = User.objects.get(email=form_page1.cleaned_data['email'])
            if user:
                # dpo = Correspondant()
                # dpo.user = user
                # dpo.organisation = organisation
                # dpo.save()
                dpo = Correspondant.objects.create(user=user, organisation=organisation, created_by=request.user)
                Enregistrement.objects.filter(id=org).update(has_dpo=True)
                # form_page2 = DPOFormPage2()
                # context['form_page2'] = form_page2
                # return render(request, 'correspondant/designation_details.html', context=context)
                return redirect('dashboard:correspondant:edit', pk=dpo.id)

            else:
                context['errors'] = 'Une erreur est survenue lors de la creation du Correspondant.'
                return render(request, 'correspondant/designation.html', context=context)
        
        else:
            context['errors'] = new_user.errors
    
    else:
        form_page1 = DPOFormPage1()
        # form_page2 = DPOFormPage2()

        context['organisation'] = organisation
        context['form_page1'] = form_page1
        # context['form_page2'] = form_page2

    return render(request, 'correspondant/designation.html', context=context)


class DPOUpdateView(UpdateView):
    model = Correspondant
    fields = ['qualifications', 'exercice_activite', 'moyens_materiels', 'moyens_humains', 'experiences']
    template_name = 'correspondant/correspondant_edit.html'

    def get_success_url(self):
        # Redirect to the detail view of the created object
        return reverse('dashboard:correspondant:detail', kwargs={'pk': self.object.pk})


class CreateDPOWizardView(SessionWizardView):
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
        })


def createDPO(request):
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
                
                """ dpo = dpo_form.save(commit=False)
                dpo.user = user
                dpo.save() """
                return render(request, 'correspondant/create_dpo_new.html', context=context)
    else:
        user_form = CreateUserDPOForm()
        dpo_form = DPOForm()
        context['is_first_step'] = True
        context['user_form'] = user_form
        context['dpo_form'] = dpo_form
        
    return render(request, 'correspondant/create_dpo_new.html', context=context)


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
            return queryset.filter(created_by=self.request.user)

        return queryset
    

class DPOCreateView(CreateView):
    model = Correspondant
    template_name = 'correspondant/correspondant_create.html'
    # fields = ['raisonsociale', 'dpo', 'user']

    """fields = [
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
    ]"""
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