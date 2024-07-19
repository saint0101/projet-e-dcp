from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('client/', views.index_client, name='index_client'),
    path('manager/', views.index_mgr, name='index_mgr'),
]