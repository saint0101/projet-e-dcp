# user/urls.py
from django.urls import path
from . import views

app_name = 'enregistrement'

urlpatterns = [
    path('', views.index, name='index'),
    path('nouveau/', views.EnregCreateView.as_view(), name='create'),
    path('liste/', views.EnregListView.as_view(), name='list'),
    path('<int:pk>/', views.EnregDetailView.as_view(), name='detail'),
    # autres motifs d'URL
]
