# user/urls.py
from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('liste/', views.UserListView.as_view(), name='list'),
    path('edit/<int:pk>/', views.UserUpdateView.as_view(), name='edit'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='detail'),
    # autres motifs d'URL
]