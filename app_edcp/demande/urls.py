from django.urls import path
from . import views

app_name = 'demande'

urlpatterns = [
  path('', views.demandes_all, name='list_all'),
  # autres motifs d'URL
]