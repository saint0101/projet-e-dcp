# user/urls.py
from django.urls import path
from . import views

app_name = 'correspondant'

urlpatterns = [
    path('', views.index, name='index'),
    path('liste/', views.DPOListView.as_view(), name='list'),
    path('<int:pk>/', views.DPODetailView.as_view(), name='detail'),
    # path('nouveau/', views.EnregCreateView.as_view(), name='create'),
    # path('liste/', views.EnregListView.as_view(), name='list'),
    # path('edit/<int:pk>/', views.EnregUpdateView.as_view(), name='edit'),
    # path('<int:pk>/', views.EnregDetailView.as_view(), name='detail'),
    # autres motifs d'URL
]