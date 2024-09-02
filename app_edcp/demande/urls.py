from django.urls import path
from . import views

app_name = 'demande'

urlpatterns = [
  path('test-pdf', views.test_pdf, name='test_pdf'), # à supprimer. Utilisé pour les tests d'affichage du fichier de réponse
  path('liste/', views.demandes_all, name='liste_all'), # liste de toutes les demandes
  path('liste/a_traiter/', views.demandes_a_traiter, name='liste_a_traiter'), # liste des demandes à traiter
  path('liste/mes_demandes/', views.mes_demandes, name='mes_demandes'), # liste des demandes de l'utilisateur
  # path('liste/<str:filter>/', views.demandes_all, name='list_all'), # 'all', 'a_traiter', 'terminees'
  path('analyse/<int:pk>/', views.analyse_demande, name='analyse'), # page d'analyse du DPO
  path('analyse/<int:pk>/<str:action>/', views.analyse_demande, name='analyse'), # page de validation du DPO
  path('analyse/reponse/<int:pk>/', views.generate_response, name='reponse'), # vue de génération du projet de réponse --> à supprimer (géré dans Demande)
  path('analyse/submit/<int:pk>/', views.submit_analyse, name='submit'), # vue de soumission de l'analyse
  path('validation/<int:pk>/', views.handle_validation, name='validation'), # validation d'une demande
  path('commentaire/<int:pk>/', views.add_commentaire, name='add_commentaire'), # ajout de commentaires
  path('reponse/<int:pk>/', views.generate_response, name='response_create'), # vue de génération du projet de reponse
  path('reponse/<int:pk>/<str:template>/', views.generate_response, name='response_create'), # vue de génération du projet de reponse
  path('delete/<int:pk>/', views.delete_demande, name='delete'),
  # autres motifs d'URL
]