# user/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),
]