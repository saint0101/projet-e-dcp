from django.urls import path

from . import views

app_name = 'connexion'

urlpatterns = [
    path('', views.index, name='index'), # url d'accueil, redirige vers l'url de login
    path('signup/', views.signup, name='signup'), # URL de l'inscription

    # autres motifs d'URL
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), # URL d'activation du compte

]
