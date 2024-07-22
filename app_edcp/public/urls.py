from django.urls import path

from . import views

app_name = 'public'

urlpatterns = [
    path('', views.index, name='index'), 
    path('a-propos/', views.a_propos, name='a_propos'),
    path('guides/', views.guides, name='guides'),
    path('faq/', views.faq, name='faq'),
    path('contacts/', views.contacts, name='contacts'),
    # autres motifs d'URL
]