from django.urls import path
from . import views

app_name = 'facturation'

urlpatterns = [
    #path('', views.index, name='index'),
    path('nouveau/<int:demande_pk>/', views.create, name='create'),
    path('<int:pk>/', views.detail_htmx, name='detail_htmx'),
    path('paiement/<int:pk>/', views.create_paiement_caisse, name='paiement_caisse'),
    # autres motifs d'URL
]
