from django.shortcuts import render, HttpResponse, redirect
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from connexion.forms import UserRegistrationForm



def index(request):
    """
    Vue d'index du module de connexion, redirige vers l'url de login.
    """
    return redirect('login')



def signup(request):
    """
    Vue de gestion de l'inscription.
    Affiche le formulaire d'inscription et enregistre l'utilisateur dans la base de données.
    Si l'enregsitrement est réussi, l'utilisateur est redirigé vers la page de login.
    En cas d'erreur, les informations sont envoyées au template dans le contexte pour être affichées.
    """
    
    context = {}

    if request.method == 'POST':
        user = UserRegistrationForm(request.POST)
        if user.is_valid():
            user.save()
            # return HttpResponse('Bienvenue !')
            context['message'] = 'Inscription effectuée avec succès !'
            # return redirect('connexion:login')
            form = AuthenticationForm()
            context['form'] = form
            return render(request, 'registration/login.html', context=context)
        
        else:
            context['errors'] = user.errors

    # form = UserCreationForm()
    form = UserRegistrationForm()
    context['form'] = form

    return render(request, 'connexion/signup.html', context=context)

