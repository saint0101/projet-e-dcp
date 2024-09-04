# user/urls.py
from django.urls import path
from . import views

app_name = 'demande_auto'

urlpatterns = [
    path('', views.index, name='index'),
    # path('nouveau/', views.demandeCreateView.as_view(), name='create'),
    path('nouveau/', views.create, name='create'),
    path('liste/', views.DemandeListView.as_view(), name='list'),
    path('edit/<str:pk>/', views.update, name='edit'),
    # path('edit/<str:pk>/', views.demandeUpdateView.as_view(), name='edit'),
    # path('analyse/<str:pk>/', views.analyse, name='analyse'),
    # path('edit/<str:pk>/', views.demandeUpdateView.as_view(), name='edit'),
    path('edit/<str:pk>/sous-finalites/', views.get_sous_finalites, name='sous_finalites'),
    path('edit/<str:pk>/add-transfert/', views.add_transfert, name='add_transfert'),
    path('edit/<str:pk>/add-interco/', views.add_interco, name='add_interco'),
    path('edit/<str:pk>/delete-transfert/<str:transfert_id>', views.delete_transfert, name='delete_transfert'),
    path('edit/<str:pk>/delete-interco/<str:interco_id>', views.delete_interco, name='delete_interco'),
    path('<int:pk>', views.detail, name='detail'),
    
    # autres motifs d'URL
]
