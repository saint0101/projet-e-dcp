from django.urls import path
from . import views

app_name = 'demande'

urlpatterns = [
  path('liste/', views.demandes_all, name='liste_all'),
  path('liste/a_traiter', views.demandes_a_traiter, name='liste_a_traiter'),
  # path('liste/<str:filter>/', views.demandes_all, name='list_all'), # 'all', 'a_traiter', 'terminees'
  path('validation/<int:pk>/', views.handle_validation, name='validation'),
  # autres motifs d'URL
]