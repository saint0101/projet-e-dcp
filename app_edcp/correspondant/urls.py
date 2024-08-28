# user/urls.py
from django.urls import path
from . import views

app_name = 'correspondant'

urlpatterns = [
    path('', views.index, name='index'), # affichage de l'ensemble des organisations enregistrées par l'utilisateur en précisant celles qui ont des DPO
    path('liste/', views.DPOListView.as_view(), name='list'), # affichage de la liste des DPO (pour le gestionnaire)
    # path('designation/', views.designate, name='designation'), # page de désignation d'un DPO (page 1)
    path('designation/org=<int:org>/', views.designate, name='designation'), # page de désignation d'un DPO (page 1)
    path('designation-cabinet/org=<int:org>/', views.designate_cabinet, name='designation_cabinet'), # page de désignation d'un DPO personne morale
    path('edit/<int:pk>/', views.DPOUpdateView.as_view(), name='edit'), # page d'édition du DPO physique
    path('edit-cabinet/<int:pk>/', views.DPOUpdateCabinet.as_view(), name='edit_cabinet'), # page d'édition du DPO personne morale
    path('edit/<int:pk>/<str:is_new>/', views.DPOUpdateView.as_view(), name='edit'), # page d'édition du DPO après la désignation (page 2)
    path('analyse/<int:pk>/', views.analyse, name='analyse'), # page d'analyse du DPO
    path('analyse/<int:pk>/<str:action>/', views.analyse, name='analyse'), # page de validation du DPO
    path('analyse/reponse/<int:pk>/', views.generate_response, name='reponse'), # vue de génération du projet de réponse --> à supprimer (géré dans Demande)
    path('analyse/submit/<int:pk>/', views.submit_analyse, name='submit'), # vue de soumission de l'analyse
    path('appr/<int:pk>/<int:approve>/', views.approve, name='approve'), # approbation ou refus du DPO --> à supprimer
    path('cabinet/<int:pk>/', views.designation_detail, name='designation_detail'), # affichage des détails du DPO personne morale --> à supprimer
    path('<int:pk>/', views.correspondant_detail, name='detail'), # affichage des détails du DPO
    path('<int:pk>/<str:action>/', views.correspondant_detail, name='detail'), # affichage des détails du DPO avec un paramètre d'action
    # path('<int:pk>/', views.DPODetailView.as_view(), name='detail'),
    # path('nouveau/', views.EnregCreateView.as_view(), name='create'),
    # path('nouveau/', views.DPOCreateView.as_view(), name='nouveau'),
    # path('nouveau/', views.createDPO, name='nouveau'), # création d'un nouveau DPO
    #path('designation/', views.CreateDPOWizardView.as_view(), name='create'),
    # path('liste/', views.EnregListView.as_view(), name='list'),
    # path('edit/<int:pk>/', views.EnregUpdateView.as_view(), name='edit'),
    # path('<int:pk>/', views.EnregDetailView.as_view(), name='detail'),
    # autres motifs d'URL
]