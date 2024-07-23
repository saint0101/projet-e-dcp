from django.urls import path, include

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('enregistrement/', include('enregistrement.urls')),
    path('correspondant/', include('correspondant.urls')),
]