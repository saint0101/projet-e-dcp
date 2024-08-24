from django.urls import path
from . import views

app_name = 'demande'

urlpatterns = [
  path('', views.demandes_all, name='list_all'),
  path('validation/<int:pk>/', views.handle_validation, name='validation'),
  # autres motifs d'URL
]