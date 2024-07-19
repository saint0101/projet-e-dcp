from django.shortcuts import render, HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from connexion.forms import UserRegistrationForm



# Create your views here.
def index(request):
    """ Vue index user """
    return render(request, 'connexion/index.html')


def signup(request):
    context = {}

    if request.method == 'POST':
        user = UserRegistrationForm(request.POST)
        if user.is_valid():
            user.save()
            return HttpResponse('Bienvenue !')
        
        else:
            context['errors'] = user.errors

    # form = UserCreationForm()
    form = UserRegistrationForm()
    context['form'] = form

    return render(request, 'connexion/signup.html', context=context)


def signup_basic(request):
    """ Vue inscription d'utilisateur """
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(password1, password2)

        if password1 != password2 : 
            return render(request, 'connexion/signup.html', {'error': 'Les mots de passe ne correspondent pas'})
        
        # User.objects.create_user(username = username, password = password1)
        return HttpResponse(f'Bienvenue {username}')

    return render(request, 'connexion/signup.html')
