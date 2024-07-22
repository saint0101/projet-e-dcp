from django.urls import path, include

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'), # url du tableau de bord
    # path('client/', views.index_client, name='index_client'),
    # path('manager/', views.index_mgr, name='index_mgr'),
]