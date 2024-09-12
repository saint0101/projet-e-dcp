# from email import message
# from multiprocessing import context
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.urls import reverse_lazy
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Obtention du modèle utilisateur configuré
User = get_user_model()


def index(request):
    """ Vue d'index du module de connexion. Redirige l'utilisateur vers l'URL de login."""
    return redirect('connexion:login')
# views.py


def signup_landing(request, messages=None):
    """
    Page de landing après l'inscription d'un nouvel utilisateur.
    Les utilisateurs doivent confirmer leur e-mail pour activer leur compte.
    """

    return render(request, 'connexion/signup_landing.html', context={'messages': messages})


def signup(request):
    """
    Vue pour l'inscription d'un nouvel utilisateur.
    Les utilisateurs doivent confirmer leur e-mail pour activer leur compte.
    """
    context = {}
    # si le formulaire a été soumis
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, request.FILES) # Créer une instance de formulaire avec les données POST et en incluant les fichiers joints
        
        # si le formulaire est valid
        if user_form.is_valid():
            user = user_form.save(commit=False) # Créer l'utilisateur mais ne pas l'activer encore
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

            email_from = settings.EMAIL_HOST_USER  # Adresse e-mail configurée dans settings
            recipient_list = [user.email]
            try:
                # Envoyer l'e-mail de confirmation
                send_mail(mail_subject, message, email_from, recipient_list, fail_silently=False)
                logger.info("Email de vérification envoyé avec succès.")
                context['message'] = {
                    'success': True,
                    'message': 'Merci pour votre inscription ! \n Un email vous a été envoyé. Veuillez cliquer sur le lien de vérification afin d\'activer votre compte. Pensez également à vérifier le dossier SPAM si vous ne le retrouvez pas.'
                }
            
            except Exception as e:
                context['errors'] = str(e)

                logger.error(f"Erreur lors de l'envoi de l'email: {e}")
                message = 'Une erreur est survenue lors de l\'envoi de l\'e-mail. Veuillez reessayer : \n' + str(e)
                context['message'] = {
                    'success': False,
                    'message': message
                }

            return render(request, 'connexion/signup_landing.html', context=context) # Affichage de la page de landing avec les messages de succès ou d'erreur
        
        # si le formulaire est invalide
        else:
            # Afficher les erreurs de formulaire
            context['form'] = user_form
            context['errors'] = user_form.errors

    # si le formulaire n'a pas encore été soumis (première ouverture de la page)
    else:
        # Afficher le formulaire d'inscription
        user_form = UserRegistrationForm()
        context['form'] = user_form

    return render(request, 'connexion/signup.html', context=context)


def activate(request, uidb64, token):
    """
    Vue pour activer le compte utilisateur via le lien envoyé par e-mail.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # Décoder l'ID utilisateur
        user = User.objects.get(pk=uid) # Trouver l'utilisateur correspondant
        print('Utilisateur trouvé:', user)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        logger.error('Erreur de décodage ou utilisateur non trouvé:', e)
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Activer l'utilisateur si le jeton est valide
        user.is_active = True
        user.email_verified = True
        user.save()
        
        messages.success(request, 'Votre compte a été activé. Vous pouvez à présent vous connecter au tableau de bord')
        return redirect('connexion:login')

    else:
        logger.error('Activation échouée ou utilisateur non valide') # Afficher une page d'erreur si l'activation échoue
        return render(request, 'connexion/activation_invalid.html')
    

class Login(LoginView):
    template_name = 'registration/login_form.html'
    success_url = reverse_lazy('dashboard:index') # Page affichée après la connexion
    
    """ def get(self, request, *args, **kwargs):
        must_reset = self.kwargs.get('must_reset')
        if must_reset == 1:
            self.success_url = reverse_lazy('connexion:password_change')
        return super().get(request, *args, **kwargs) """
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Bienvenue {self.request.user} !') 
        return response


class Logout(LogoutView):
    pass

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Déconnexion effectuée')
        return response

class PasswordChange(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('dashboard:user:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = User.objects.get(pk=self.request.user.id)
        # Met le champs must_reset à False. utilisé pour les compte utilisateurs créés dynmaiquement 
        # et pour lesquels l'utilisateur doit réinitialiser le mot de passe à la première connexion
        user.must_reset = False 
        user.email_verified = True
        user.save()
        messages.success(self.request, 'Votre mot de passe a été mis à jour.')
        return response
