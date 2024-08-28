"""app_edcp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from public import views as public


urlpatterns = [
    path('', public.index, name='index'),
    # path('admin/doc/', include('django.contrib.admindocs.urls')), # page de documentation admin.
    path('admin/', admin.site.urls), # page d'administration
    path('public/', include('public.urls')), # partie publque du site (accueil, à propos, contacts etc.)
    path('dashboard/', include('dashboard.urls')), # tableaux de bord client et gestionnaire
    path('connexion/', include('connexion.urls')), # page d'inscription, login, changement de mot de passe etc.
    # path('connexion/', include('django.contrib.auth.urls')), # autres pages de connexion (login, mot de passe oublié etc.) 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # ajout de l'url des fichiers statiques uploadés



