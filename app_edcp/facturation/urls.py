from django.urls import path
from . import views

app_name = 'facturation'

urlpatterns = [
    #path('', views.index, name='index'),
    path('nouveau/<int:demande_pk>/', views.create, name='create'),
    path('<int:pk>/', views.detail_htmx, name='detail_htmx'),
    path('paiement/add/<int:pk>/', views.create_paiement_caisse, name='paiement_caisse'),
    path('paiement/detail/<int:pk>/', views.detail_paiement, name='paiement_detail'),
    path('paiement/valider/<int:pk>/', views.validate_paiement, name='paiement_valider'),
    path('paiement/all/', views.list_paiements, name='list_paiements'),
    # autres motifs d'URL
]
