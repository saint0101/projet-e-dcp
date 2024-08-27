from django.urls import path
from . import views

app_name = 'demande'

urlpatterns = [
  path('test-pdf', views.test_pdf, name='test_pdf'),
  path('liste/', views.demandes_all, name='liste_all'),
  path('liste/a_traiter', views.demandes_a_traiter, name='liste_a_traiter'),
  # path('liste/<str:filter>/', views.demandes_all, name='list_all'), # 'all', 'a_traiter', 'terminees'
  path('validation/<int:pk>/', views.handle_validation, name='validation'),
  path('commentaire/<int:pk>/', views.add_commentaire, name='add_commentaire'),
  path('reponse/<int:pk>/<str:template>/', views.generate_response, name='response_create'),
  # autres motifs d'URL
]