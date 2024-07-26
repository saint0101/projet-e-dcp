from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

from django.contrib.auth.models import User

# Obtention du modèle utilisateur configuré
User = get_user_model()

def index(request):
    """
    Vue d'index du module de connexion. Redirige l'utilisateur vers l'URL de login.
    """
    return redirect('login')
# views.py

def signup(request):
    """
    Vue pour l'inscription d'un nouvel utilisateur.
    Les utilisateurs doivent confirmer leur e-mail pour activer leur compte.
    """

    context = {}
    if request.method == 'POST':
        # Créer une instance de formulaire avec les données POST
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Créer l'utilisateur mais ne pas l'activer encore
            user = user_form.save(commit=False)
            user.is_active = False  # L'utilisateur doit confirmer son e-mail avant activation
            user.email_verified = False  # Assurez-vous que `email_verified` est défini
            user.save()

            # Préparer l'e-mail de confirmation
            current_site = get_current_site(request)
            mail_subject = 'Activez votre compte.'
            uid = urlsafe_base64_encode(str(user.pk).encode())  # Encode l'ID utilisateur
            token = default_token_generator.make_token(user)
            message = render_to_string('connexion/acc_active_email.html', {
                'user': user,  # Assurez-vous que l'objet utilisateur est passé correctement
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            """
            # Debugging
            # print('User id: ', user.pk)
            # print('User: ', user)
            # print('UID (encoded): ', uid)
            # print('Token: ', token)

            """
            email_from = settings.EMAIL_HOST_USER  # Adresse e-mail configurée dans settings
            recipient_list = [user.email]

            try:
                # Envoyer l'e-mail de confirmation
                send_mail(mail_subject, message, email_from, recipient_list)
                context['message'] = 'Un e-mail de confirmation a été envoyé à votre adresse e-mail.'
            except Exception as e:
                # Gérer les erreurs d'envoi d'e-mail
                context['errors'] = str(e)
                context['message'] = 'Une erreur est survenue lors de l\'envoi de votre e-mail. Veuillez reessayer :' + str(e)

            # Afficher le formulaire de connexion
            form = AuthenticationForm()
            context['form'] = form
            return render(request, 'registration/login.html', context=context)
        else:
            # Afficher les erreurs de formulaire
            context['errors'] = user_form.errors
    else:
        # Afficher le formulaire d'inscription
        user_form = UserRegistrationForm()
        context['form'] = user_form

    return render(request, 'connexion/signup.html', context=context)


def activate(request, uidb64, token):
    """
    Vue pour activer le compte utilisateur via le lien envoyé par e-mail.
    """
    print(f'Activation demandé avec UID: {uidb64} et Token: {token}')

    try:
        # Décoder l'ID utilisateur
        uid = urlsafe_base64_decode(uidb64).decode()
        #print(f'UID Décodé: {uid}')
        # Trouver l'utilisateur correspondant
        user = User.objects.get(pk=uid)
        #print('Utilisateur trouvé:', user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print('Erreur de décodage ou utilisateur non trouvé:', e)
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Activer l'utilisateur si le jeton est valide
        user.is_active = True
        user.save()
        print('Utilisateur activé:', user)
        return redirect('login')
    else:
        # Afficher une page d'erreur si l'activation échoue
        #print('Activation échouée ou utilisateur non valide')
        return render(request, 'connexion/activation_invalid.html')

