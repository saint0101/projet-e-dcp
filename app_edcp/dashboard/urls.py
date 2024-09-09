from django.urls import path, include

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('construction', views.page_en_construction, name='construction'),
    path('enregistrement/', include('enregistrement.urls')),
    path('demande/', include('demande.urls')), 
    path('correspondant/', include('correspondant.urls')),
    path('user/', include('user.urls')),
    path('demande-autorisation/', include('demande_auto.urls')),
    path('facturation/', include('facturation.urls')),
]