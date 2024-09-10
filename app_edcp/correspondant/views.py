import json
import os
import base64
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django import forms

from base_edcp.emails import MAIL_CONTENTS, send_email
from base_edcp.pdfs import generate_pdf, PDF_TEMPLATES
from base_edcp.models import User, Enregistrement
from demande.models import ActionDemande, AnalyseDemande, CategorieDemande, Commentaire, CritereEvaluation, HistoriqueDemande, ReponseDemande
from demande.forms import CommentaireForm, ProjetReponseForm, ProjetReponseModelForm, ValidateForm
from demande.views import user_has_niv_validation, can_validate, can_terminate
from demande_auto.models import EchelleNotation
from options.models import Status
from user.utils import create_new_user, check_email

from .models import Correspondant, DesignationDpoMoral, TypeDPO
from .forms import DPOCabinetFormDisabled, DPODPOUpdateFormDisabled, DPOFormPage1, DPOCabinetForm, UserIsDPOForm, generate_analyse_form, DPOUpdateForm #, AnalyseDPOForm


### Functions

def index(request):
	"""
	Vue index Correspondant du tableau de bord client.
	Affiche la liste des correspondants désignés par l'utilisateur,
	et la liste des organisations pour lesquels l'utilisateur n'a pas encore désigné de DPO.
	"""
	dpos_physique = Correspondant.objects.filter(Q(user=request.user) | Q(created_by=request.user)).filter(is_personne_morale=False) # Filtre si l'utilisateur est lui-même un DPO ou s'il a désigné des DPO
	dpos_moral = Correspondant.objects.filter(created_by=request.user).filter(is_personne_morale=True) # Liste des DPO personne morale
	orgs_without_dpo = Enregistrement.objects.filter(user=request.user).filter(has_dpo=False) # Liste des organisations créées par l'utilisateur et qui n'ont pas de DPO
	context = {
		'correspondants_physique': dpos_physique,
		'correspondants_moral': dpos_moral,
		'orgs_without_dpo': orgs_without_dpo
	}

	return render(request, 'correspondant/index.html', context=context)


def designate(request, org):
	"""
	Vue de désignation du DPO.
	Renvoie un premier formulaire pour la création du compte utilisateur du DPO,
	puis redirige vers la vue UpdateView pour l'édition du DPO créé
	"""
	context = {}
	organisation = Enregistrement.objects.get(id=org) # récupération de l'organisation pour laquelle le DPO va être désigné

	# if request.is_ajax() :
	# vérifie si la requête reçue est une requête AJAX. Utilisé pour la vérification de la disponibilité de l'adresse email
	if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
		email = request.GET.get('email')
		print(f'Ajax request received {email}')
		
		return check_email(email) # appel de la fonction de vérification de l'email et renvoi de la valeur

	# si le formulaire de création de compte utilisateur a été soumis
	if request.method == 'POST':
		form_page1 = DPOFormPage1(request.POST) # récupération des données du formulaire
		form_user_is_dpo = UserIsDPOForm(request.POST)

		# si le formulaire de choix a été soumis et est valide,
		#    l'utilisateur courant fait donc une auto-désignation
		#    le DPO est alors créé avec pour "user" l'utilisateur courant
		if 'submit_user_is_dpo_form' in request.POST and form_user_is_dpo.is_valid(): 
			dpo = Correspondant.objects.create(
				user=request.user, 
				organisation=organisation, 
				created_by=request.user, 
				categorie=CategorieDemande.objects.get(label='designation_dpo'),
				type_dpo=TypeDPO.objects.get(label='personne_physique'),
				status=Status.objects.get(label='demande_attente_traitement'),
			) # création du DPO
			Enregistrement.objects.filter(id=org).update(has_dpo=True) # mise à jour de l'organsiation avec --> has_dpo = True
			messages.success(request, 'Le Correspondant a bien été créé.')
			dpo.save_historique(action_label='creation', user=request.user)
			return redirect('dashboard:correspondant:edit', pk=dpo.id, is_new=True) # redirection vers la vue UpdateView avec l'id du DPO créé
		
		# si le formulaire de création de compte a été soumis et est valide,
		#    l'utilisateur courant désigne quelqu'un d'autre comme DPO.
		#    le DPO est alors enregistré avec le compte nouvellement créé
		elif 'submit_designation_form' in request.POST and form_page1.is_valid(): 
			user, password = create_new_user(form_page1.cleaned_data) # appel de la fonction de création d'un nouvel utilisateur
			# si l'utilisateur a bien été créé
			if user:
				print(f'Password check : {password}')
				# envoi du mail de notification à l'utilisateur nouvellement créé
				send_email(
					request=request,
					mail_content=MAIL_CONTENTS['correspondant_new_compte'],
					recipient_list=[user.email],
					show_message=False,
					context={
						'user': user,
						'organisation': organisation,
						'password': password
					},
				)
				dpo = Correspondant.objects.create(
					user=user, 
					organisation=organisation, 
					created_by=request.user, 
					categorie=CategorieDemande.objects.get(label='designation_dpo'),
					type_dpo=TypeDPO.objects.get(label='personne_physique'),
					status=Status.objects.get(label='demande_attente_traitement'),
				) # création du DPO
				Enregistrement.objects.filter(id=org).update(has_dpo=True) # mise à jour de l'organsiation avec --> has_dpo = True

				print(f'DPO {dpo} created')
				messages.success(request, 'Le Correspondant a bien été créé.')
				dpo.save_historique(action_label='creation', user=request.user)

				mail_context = {
						'correspondant': dpo,
				}
				send_email(
					request=request, 
					mail_content=MAIL_CONTENTS['correspondant_designation_client'], 
					recipient_list=[dpo.user.email, request.user.email], 
					context=mail_context
				) 
				
				return redirect('dashboard:correspondant:edit', pk=dpo.id, is_new=True) # redirection vers la vue UpdateView avec l'id du DPO créé

			# si l'utilisateur n'a pas pu être créé
			else:
				context['errors'] = 'Une erreur est survenue lors de la creation du Correspondant.'
				context['form_page1'] = form_page1
				context['form_user_is_dpo'] = form_user_is_dpo
				return render(request, 'correspondant/designation.html', context=context)
		
		# si le formulaire de création d'utilisateur n'est pas valide
		else:
			context['errors'] = form_page1.errors # ajout des erreurs du formulaire au contexte
			context['form_page1'] = form_page1 # ajout du formulaire au contexte
			context['form_user_is_dpo'] = UserIsDPOForm(initial={'user_is_dpo': False}) # ajout du formulaire au contexte
	
	# si le formulaire de création de compte utilisateur n'a pas encore été soumis (la page vient d'être ouverte)
	else:
		form_page1 = DPOFormPage1() # initialisation du formulaire
		form_user_is_dpo = UserIsDPOForm() # initialisation du formulaire

		context['organisation'] = organisation # ajout de l'organisation au contexte
		context['form_page1'] = form_page1 # ajout du formulaire au contexte
		context['form_user_is_dpo'] = form_user_is_dpo # ajout du formulaire au contexte

	return render(request, 'correspondant/designation.html', context=context) # renvoi de la vue


def designate_cabinet(request, org):
	"""
	Vue de désignation d'un DPO personne morale.
	"""
	context = {}
	organisation = Enregistrement.objects.get(id=org) # récupération de l'organisation pour laquelle le DPO va être désigné
	form = DPOCabinetForm()

	if request.method == 'POST':
		form = DPOCabinetForm(request.POST, request.FILES)
		if form.is_valid():
			# dpo = form.save(commit=False)
			dpo = form.cleaned_data
			# print ('form_dpo : ', form.cleaned_data)
			# création du correspondant
			correspondant = Correspondant.objects.create(
				user = dpo['cabinet'].user,
				created_by = request.user,
				organisation = organisation,
				cabinet = dpo['cabinet'],
				categorie = CategorieDemande.objects.get(label='designation_dpo'),
				is_personne_morale = True,
				type_dpo=TypeDPO.objects.get(label='personne_morale'),
				status=Status.objects.get(label='demande_attente_traitement'),
			)

			messages.success(request, 'La désignation du Correspondant a bien été enregistrée.')
			correspondant.save_historique(action_label='creation', user=request.user) # enregistrement de la création dans l'historique
			
			Enregistrement.objects.filter(id=org).update(has_dpo=True) # mise à jour de l'organsiation avec --> has_dpo = True
			mail_context = {
				'correspondant': correspondant,
			}
			print ('context - view : ', mail_context)
			send_email(
				request=request, 
				mail_content=MAIL_CONTENTS['correspondant_designation_client'], 
				recipient_list=[correspondant.cabinet.email_contact, request.user.email], 
				context=mail_context
			) 
		# context
			return redirect('dashboard:correspondant:detail', pk=correspondant.id) #

		else:
			context['errors'] = form.errors

	context['form'] = form
	return render(request, 'correspondant/designation_cabinet.html', context=context)


def designation_detail(request, pk):
	pass


""" TO DELETE """
def approve(request, pk, approve):
	""" Vue d'approbation de correspondant """
	context = {}
	correspondant = Correspondant.objects.get(id=pk)
	# vérifie si l'utilisateur est un gestionnaire
	if request.user.is_staff: 
		# si l'action est une approbation (approve == 1)
		if approve == 1 :
			correspondant.is_approved = True
			messages.success(request, 'Correspondant approuvé.')

		# si l'action est un retrait de l'approbation (approve == 0)
		if approve == 0 :
			correspondant.is_approved = False
			messages.success(request, 'Approbation retirée.')

		# si l'action est un refus (approve == 2)
		if approve == 2 :
			correspondant.is_approved = False
			correspondant.is_rejected = True
			messages.success(request, 'Désignation refusée.')

		correspondant.save()
		# préparation du contexte pour l'envoi de l'email
		mail_context = {
			'correspondant': correspondant,
			'approved': approve
		}
		# envoi de l'email
		send_email(
			request=request, 
			mail_content=MAIL_CONTENTS['correspondant_approbation_client'], 
			recipient_list=[correspondant.created_by.email, correspondant.user.email], 
			context=mail_context,
			show_message=False
		)
	
	# si l'utilisateur n'est pas un gestionnaire
	else :
		messages.error(request, 'Vous n\'avez pas les droits pour effectuer cette action.')

	context['correspondant'] = correspondant
	return redirect('dashboard:correspondant:detail', pk=correspondant.id)



def analyse(request, pk, action=None):
	""" Vue d'analyse de la demande """
	correspondant = get_object_or_404(Correspondant, pk=pk)
	analyse = correspondant.analyse
	AnalyseDPOForm = generate_analyse_form(CategorieDemande.objects.get(label='designation_dpo'), analyse)
	
	# si aucune analyse n'a encore été créée pour cette demande
	if not analyse :
		status_brouillon, created = Status.objects.get_or_create(label='brouillon', defaults={'description': 'Brouillon'})
		status_encours, created = Status.objects.get_or_create(label='analyse_en_cours', defaults={'description': 'Analyse en cours'})
		# action_changement, created = ActionDemande.objects.get_or_create(label='changement_statut', defaults={'description': 'Changement de statut'})
		
		# création de l'analyse
		analyse = AnalyseDemande.objects.create(created_by=request.user, status=status_brouillon)
		correspondant.analyse = analyse
		correspondant.status = status_encours
		correspondant.save()
		correspondant.save_historique(action_label='changement_statut', user=request.user)

	# si le formulaire d'analyse a été envoyé
	if request.method == 'POST':
		form = AnalyseDPOForm(request.POST)
		if form.is_valid():
			form_data = form.cleaned_data

			# enregistrement de l'analyse
			analyse.observations = form.cleaned_data['observations']
			analyse.prescriptions = form.cleaned_data['prescriptions']
			analyse.avis_juridique = form.cleaned_data['avis_juridique']
			analyse.updated_at = datetime.now()
			analyse.updated_by = request.user

			# enregistrement de l'évaluation. Ce champ est stocké sous forme de texte sérialisé (JSON)
			evaluation = {}
			# pour chaque critère d'évaluation défini pour cette catégorie de demande, si le champ est renseigné, il est enregistré
			for field in CritereEvaluation.objects.filter(categorie_demande=CategorieDemande.objects.get(label='designation_dpo')):
					if field.label in form_data.keys() :
						evaluation[field.label] = form_data[field.label]
			serialized_data = json.dumps(evaluation) # conversion en JSON
			# print('serialized_data : ', serialized_data)
			analyse.evaluation = serialized_data # enregstrement du champ

			analyse.save()
			return redirect('dashboard:correspondant:analyse', pk=pk)

	form = AnalyseDPOForm(initial=analyse.__dict__) # initialisation du formulaire d'analyse
	
	# initialisation du formulaire d'affichage du DPO en fonction de son type
	if correspondant.is_personne_morale:
		form_dpo = DPOCabinetFormDisabled(instance=correspondant)
	else:
		form_dpo = DPODPOUpdateFormDisabled(instance=correspondant)

	form_projet_reponse = ProjetReponseModelForm(demande=correspondant) # initialisation du formulaire de projet de reponse
	
	form_comment = CommentaireForm() # initialisation du formulaire de commentaires
	# préparation du contexte
	context = {
		'form': form,
		'form_dpo': form_dpo,
		'form_comment': form_comment,
		'form_projet_reponse': form_projet_reponse,
		'correspondant': correspondant,
		'analyse': analyse,
		'can_validate': can_validate(request.user, correspondant),
		'can_terminate': can_terminate(request.user, correspondant),
		'commentaires': Commentaire.objects.filter(demande=correspondant).order_by('created_at'),
		'validations': analyse.validations.all(),
		'action': action,
		'historique': HistoriqueDemande.objects.filter(demande=correspondant)
	}  

	# si l'action est une validation de demande
	if action == 'validate': 
		form_validation = ValidateForm()
		context['form_validation'] = form_validation

	# si le paramètre show_comments est true (après un ajout de commentaire, pour afficher directement le formulaire)
	if action == 'show_comments':
		context['show_comments'] = True

	# Si un projet de réponse existe pour cette demande
	if correspondant.analyse.projet_reponse:
		pdf_path = correspondant.analyse.projet_reponse.fichier_reponse.path # récupération de l'adresse du fichier
		with open(pdf_path, 'rb') as pdf_file: # ouverture du fichier PDF
			# Convert pdf to a string
			pdf_content = base64.b64encode(pdf_file.read()).decode()
			context['projet_reponse_pdf'] = pdf_content

	return render(request, 'correspondant/correspondant_analyse.html', context=context)


""" TO DELETE (géré dans Demande)"""
def generate_response(request, pk):
	""" Vue de génération du projet de réponse """
	correspondant = get_object_or_404(Correspondant, pk=pk)
	# préparation du contexte. pk et url_path sont utilisés pour généré le QR code 
	context = {
			'pk': pk,
			'correspondant': correspondant,
			'url_path': 'dashboard:correspondant:detail',
	}
	pdf_file = generate_pdf(request, PDF_TEMPLATES['correspondant_approbation'], context) # génération du projet de réponse en PDF
	# création et enregistrement du projet de réponse
	## METTRE EN PLACE UNE SUPPRESSION DES ANCIENS PROJETS DE REPONSE
	projet_reponse = ReponseDemande.objects.create()
	projet_reponse.fichier_reponse.save('projet_reponse.pdf', pdf_file)
	projet_reponse.intitule = 'Lettre d\'approbation'
	# projet_reponse.fichier_reponse = pdf_file
	projet_reponse.save()
	correspondant.analyse.projet_reponse = projet_reponse
	correspondant.analyse.save()
	messages.success(request, 'Projet de réponse généré.')

	return redirect('dashboard:correspondant:analyse', pk=pk)


def submit_analyse(request, pk):
	""" Soumission de l'analyse pour validation par le supérieur """
	correspondant = get_object_or_404(Correspondant, pk=pk)
	analyse = correspondant.analyse
	
	# si l'analyse a bien été créée, changement du statut
	if analyse :
		analyse.is_locked = True # verrouillage de l'analyse pendant la validation pour éviter une modification
		
		# si l'utilisateur qui traite la demande est un superviseur (niv_validation 1)
		# la demande passe directement au niveau 2
		if user_has_niv_validation(request.user, 1):
			analyse.niv_validation = 2
			status, created = Status.objects.get_or_create(
				label='attente_validation_2',
				defaults={'description': 'En attente de validation niv. 2'}    
			)
		else:
			analyse.niv_validation = 1
			status, created = Status.objects.get_or_create(
				label='attente_validation_1',
				defaults={'description': 'En attente de validation niv. 1'}    
			)

		analyse.status = status
		analyse.save()
		correspondant.save_historique(action_label='changement_statut', user=request.user, status=analyse.status, is_private=True)
 
	return redirect('dashboard:correspondant:analyse', pk=pk)


class DPOUpdateCabinet(UpdateView):
	""" Vue de modification du DPO personne morale """
	model = Correspondant
	form_class = DPOCabinetForm
	template_name = 'correspondant/correspondant_edit.html'
	context_object_name = 'correspondant'

	def get_success_url(self):
		# Redirect to the detail view of the created object
		self.object.save_historique(action_label='mise_a_jour', user=self.request.user)
		messages.success(self.request, 'Désignation du correspondant mise à jour.')
		return reverse('dashboard:correspondant:detail', kwargs={'pk': self.object.pk})
		


class DPOUpdateView(UpdateView):
	""" Vue de modification du DPO personne physique """

	model = Correspondant
	""" fields = [
			'is_active',
			'qualifications', 
			'exercice_activite', 
			'moyens_dpo', 
			'experiences',
			'file_lettre_designation',
			'file_lettre_acceptation',
			'file_attestation_travail',
			'file_casier_judiciaire',
			'file_certificat_nationalite',
			'file_cv',
	] """
	form_class = DPOUpdateForm
	template_name = 'correspondant/correspondant_edit.html'
	context_object_name = 'correspondant'
	
	def form_valid(self, form):
		"""Méthode appelée lorsque le formulaire est valide"""
		obj = form.save(commit=False) # Sauvegarde l'objet avec les données du formulaire, sans le valider encore
		obj.profile_completed = True # Marque le profil comme complet
		response = super().form_valid(form) # Sauvegarde l'objet en appelant la méthode de la classe parente
		self.object = obj # Définit l'objet sauvegardé pour les actions post-sauvegarde
		
		messages.success(self.request, 'Informations enregistrées avec succès.')

		# s'il s'agit d'une nouvelle désignation de correspondant
		if self.kwargs.get('is_new'):
			# notification du correspondant et de l'utilisateur qui l'a désigné
			send_email(
				request=self.request, 
				mail_content=MAIL_CONTENTS['correspondant_designation_client'], 
				recipient_list=[obj.user.email, self.request.user.email], 
				context={'correspondant': obj}
			)
			# notification de l'Autorité de Protection
			send_email(
				request=self.request, 
				mail_content=MAIL_CONTENTS['correspondant_designation_mgr'], 
				recipient_list=[settings.EMAIL_HOST_USER ], 
				context={'correspondant': obj},
				show_message=False
			)

		self.object.save_historique(action_label='mise_a_jour', user=self.request.user)
		return response
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['is_new'] = self.kwargs.get('is_new') # permet de vérifier si le formulaire est affiché suite à la création d'un DPO
		return context

	def get_success_url(self):
		# Redirect to the detail view of the created object
		return reverse('dashboard:correspondant:detail', kwargs={'pk': self.object.pk})


class DPOListView(ListView):
		model = Correspondant
		template_name = 'correspondant/correspondant_list.html'
		context_object_name = 'correspondants'

		def get_queryset(self):
				queryset = super().get_queryset()
				if not self.request.user.is_staff:
						return queryset.filter(user=self.request.user)

				return queryset



def correspondant_detail(request, pk, action=None):
	""" Vue de détail du DPO"""
	template_name = 'correspondant/correspondant_detail.html'
	context = {}
	correspondant = get_object_or_404(Correspondant, pk=pk)

	# si l'utilisateur n'est pas le DPO ou n'a pas créé le DPO et s'il n'est pas un gestionnaire, permission refusée
	if not (correspondant.created_by == request.user or correspondant.user == request.user) and not request.user.is_staff:
			raise PermissionDenied
	
	historique = HistoriqueDemande.objects.filter(demande=correspondant) # chargement de l'historique
	commentaires = Commentaire.objects.filter(demande=correspondant).order_by('created_at') # chargement des commentaires
	form_comment = CommentaireForm() # initialisation du formulaire de commentaires

	context['correspondant'] = correspondant
	context['historique'] = historique
	context['commentaires'] = commentaires
	context['form_comment'] = form_comment

	# paramètre pour l'affichage automatique des commentaires 
	if action == 'show_comments':
		context['show_comments'] = True

	return render(request, template_name, context=context)


""" TO DELETE """
class DPODetailView(DetailView):
		""" Vue d'affichage du DPO. Remplacée par 'correspondant_detail' au-dessus. """
		model = Correspondant
		template_name = 'correspondant/correspondant_detail.html'
		context_object_name = 'correspondant'

		def get_queryset(self):
				queryset = super().get_queryset()
				if not self.request.user.is_staff:
						return queryset.filter(created_by=self.request.user)

				return queryset
		
		def get_context_data(self, **kwargs):
				context = super().get_context_data(**kwargs)
				
				historique = HistoriqueDemande.objects.filter(demande=self.object)
				commentaires = Commentaire.objects.filter(demande=self.object).order_by('created_at')
				print('commentaires : ', commentaires)
				form_comment = CommentaireForm()
				
				context['historique'] = historique
				context['commentaires'] = commentaires
				context['form_comment'] = form_comment

				return context


