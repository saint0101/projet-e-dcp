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
from .forms import DPOFormPage1, UserIsDPOForm
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
    """
    Fonction de vérification de l'existence d'un email dans la base de données
    Returns : objet JSON
    """
    # si l'utilisateur avec l'email fourni en paramètre existe dans la BD
    if User.objects.filter(email=email).exists():
        print(f'email found : {email}')
        # récupération de l'utilisateur
        user=User.objects.get(email=email)
        print(f'user : {user}')
        print(f'is_dpo : {user.is_dpo}')

        # renvoi de l'objet JSON
        return JsonResponse({
            'email_exists': True, 
            'is_dpo': user.is_dpo
            })
    # renvoi de l'objet JSON si l'email n'existe pas
    print(f'email not found : {email}')
    return JsonResponse({'email_exists': False})


def create_new_user(data):
    """
    Fonction de création d'un nouvel utilisateur.
    Crée un mot de passe aléatoire par défaut.
    """
    # à remplacer par l'ajout d'une méthode random pour le mot de passe.
    random_password = 'pbkdf2_sha256$600000$aM8OOxx8RVXcAA8ISDbNC5$CgJsb4SLOpQgiw8SEGEsO27PR07iW8YSL2kwA6ZVV8o='
    # Création d'un nouvel utilisateur
    new_user = User.objects.create_user(
        nom=data['nom'], 
        prenoms=data['prenoms'], 
        telephone=data['telephone'], 
        email=data['email'], 
        password=random_password, 
        is_dpo=True, is_active=True, 
        email_verified=False)

    return new_user


def designate(request, org):
    """
    Vue de désignation du DPO.
    Renvoie un premier formulaire pour la création du compte utilisateur du DPO,
    puis redirige vers la vue UpdateView pour l'édtion du DPO créé
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
        # l'utilisateur courant fait donc une auto-désignation
        # le DPO est alors créé avec pour user l'utilisateur courant
        if 'submit_user_is_dpo_form' in request.POST and form_user_is_dpo.is_valid(): 
            dpo = Correspondant.objects.create(user=request.user, organisation=organisation, created_by=request.user) # création du DPO
            Enregistrement.objects.filter(id=org).update(has_dpo=True) # mise à jour de l'organsiation avec --> has_dpo = True

            return redirect('dashboard:correspondant:edit', pk=dpo.id, is_new=True) # redirection vers la vue UpdateView avec l'id du DPO créé
        
        # si le formulaire de création de compte a été soumis et est valide,
        # l'utilisateur courant désigne quelqu'un d'autre comme DPO.
        # le DPO est alors enregistré avec le compte nouvellement créé
        elif 'submit_designation_form' in request.POST and form_page1.is_valid(): 
            user = create_new_user(form_page1.cleaned_data) # appel de la fonction de création d'un nouvel utilisateur
            # si l'utilisateur a bien été créé
            if user:
                dpo = Correspondant.objects.create(user=user, organisation=organisation, created_by=request.user) # création du DPO
                Enregistrement.objects.filter(id=org).update(has_dpo=True) # mise à jour de l'organsiation avec --> has_dpo = True

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


class DPOUpdateView(UpdateView):
    model = Correspondant
    fields = ['qualifications', 'exercice_activite', 'moyens_materiels', 'moyens_humains', 'experiences']
    template_name = 'correspondant/correspondant_edit.html'

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


class DPODetailView(DetailView):
    model = Correspondant
    template_name = 'correspondant/correspondant_detail.html'
    context_object_name = 'correspondant'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.filter(created_by=self.request.user)

        return queryset
    

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
