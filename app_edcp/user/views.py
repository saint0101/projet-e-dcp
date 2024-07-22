from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .forms import UserForm
from base_edcp.models import User

# Create your views here.

# user/views.py
def index(request):
    """ Vue index user """
    return render(request, 'user/index.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # L'utilisateur n'est pas encore actif jusqu'à ce que l'email soit vérifié
            user.save()

            # Envoi de l'email de confirmation
            current_site = get_current_site(request)
            mail_subject = 'Activez votre compte.'
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            print('verifier si le mail est envoyer')
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            print("info mail : ", email)
            email.send()

            return render(request, 'user/confirmation_sent.html')
        else:
            print(form.errors)  # Pour voir les erreurs de validation du formulaire
            print('Formulaire invalide')
    else:
        form = UserForm()

    return render(request, 'user/signup.html', {'form': form})


def activate_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  # Décode l'UID de l'utilisateur à partir de l'URL
        user = User.objects.get(pk=uid)  # Récupère l'utilisateur à partir de l'UID
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Vérifie si l'utilisateur existe et si le jeton est valide
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'user/activation_invalid.html')  # Affiche une page d'erreur si l'activation a échoué

