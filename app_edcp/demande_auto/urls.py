# user/urls.py
from django.urls import path
from . import views

app_name = 'demande_auto'

urlpatterns = [
    path('', views.index, name='index'),
    # path('nouveau/', views.demandeCreateView.as_view(), name='create'),
    path('nouveau/', views.create, name='create'),
    path('liste/', views.DemandeListView.as_view(), name='list'),
    path('detail/<str:pk>', views.detail, name='detail'),
    path('edit/<str:pk>/', views.update, name='edit'),
    # path('edit/<str:pk>/', views.demandeUpdateView.as_view(), name='edit'),
    path('edit/<str:pk>/sous-finalites/', views.get_sous_finalites, name='sous_finalites'),
    
    # autres motifs d'URL
]
