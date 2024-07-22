# user/urls.py
from django.urls import path
from . import views

app_name = 'enregistrement'

urlpatterns = [
    path('', views.index, name='index'),
    path('nouveau/', views.EnregCreateView.as_view(), name='create'),
    # autres motifs d'URL
]
