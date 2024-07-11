# user/urls.py
from django.urls import path

from . import views



urlpatterns = [
    path('', views.index, name='index'),
    # autres motifs d'URL
]