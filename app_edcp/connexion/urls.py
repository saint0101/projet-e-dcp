from django.urls import path

from . import views

app_name = 'connexion'

urlpatterns = [
    path('', views.index, name='index'), # url d'accueil, redirige vers l'url de login
    path('signup/', views.signup, name='signup'), # URL d'inscription
    path('login/', views.Login.as_view(), name='login'), # URL de login
    # path('login/<str:reset_param>', views.Login.as_view(), name='login'), # URL de l'inscription
    path('logout/', views.Logout.as_view(), name='logout'),
    path('password-change/', views.PasswordChange.as_view(), name='password_change'),

    # autres motifs d'URL
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), # URL d'activation du compte
]
