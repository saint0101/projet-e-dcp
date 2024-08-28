"""
Fonctions de filtres personnalisés utilisables dans les templates.
"""

from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import FileField

register = template.Library()

@register.filter
@stringfilter
def get_bread_text(value, arg):
    """Split la chaîne en paramètre et renvoie la première occurence (correspondant au texte à afficher)"""
    return value.split(arg)[0]


@register.filter
@stringfilter
def get_bread_url(value, arg):
    """Split la chaîne en paramètre et renvoie la seconde occurence (correspondant à l'url)"""
    return value.split(arg)[1]


@register.filter
@stringfilter
def get_filename(value):
    """
    Utilisé pour l'affichage des noms de fichiers à partir du chemin fournit en entrée
    Split la chaîne en paramètre et renvoie la dernière occurence (correspondant au nom du fichier)
    """
    if value:
        return value.split('/')[-1]
    
    return ''


@register.filter
def get_fileinfos(value):
    """
    Affiche l'URL et le nom du fichier sous forme de lien.
    Le nom du fichier est le dernier élément du path.
    Renvoie du code HTML.
    """
    if value :
        fileurl = value.url
        filename = value.name.split('/')[-1]
        return f'<a href="{fileurl}">{filename}</a>'
    
    return '<a href="#">Vide</a>'


@register.filter
def get_file_fields(instance, excluded_fields=None):
    """
    Retourne la liste des champs FileField de l'instance passée en paramètre (ex: Enregistrement, Correspondant etc.).
    Utilisé pour l'affichage des fichiers justificatifs.
    - Paramètres:
    -- excluded_fields: champs FileField à exclure (séparés par des virgules)
    """
    excluded = []
    if excluded_fields:
        excluded = excluded_fields.split(',')
    return [field for field in instance._meta.get_fields() if isinstance(field, FileField) and field.name not in excluded]


@register.filter
def get_file_fields_include(instance, included_fields=None):
    """
    Retourne la liste des champs FileField de l'instance passée en paramètre (ex: Enregistrement, Correspondant etc.).
    Utilisé pour l'affichage des fichiers justificatifs.
    - Paramètres:
    -- include_fields: champs à inclure
    """
    included = []
    if included_fields:
        included = included_fields.split(',')
    return [field for field in instance._meta.get_fields() if isinstance(field, FileField) and field.name in included]


@register.filter
def attr(obj, attr_name):
    """
    Renvoie la valeur du champ attr_name de l'objet.
    Utilisé pour l'affichage dynamique des fichiers justificatifs
    """
    return getattr(obj, attr_name, None)


@register.filter
def get_form_field(form, field_name):
    """
    Renvoie la valeur du champ field_name de l'objet.
    Utilisé pour l'affichage dynamique des formulaires.
    """
    return form[field_name]


@register.filter
def leading_zeros(value, num_digits):
    """
    Permet d'ajouter des zero devant une valeur.
    Utilisé pour l'affichage des ID des demandes.
    """
    return str(value).zfill(num_digits)

@register.filter
def get_demande_url(demande):
    """ Renvoie l'url de la page de la demande, en fonction de sa catégorie. """
    print('demandes', demande.categorie.label)
    if demande.categorie.label == 'designation_dpo':
        return 'dashboard:correspondant:'
    
    if demande.categorie.label == 'demande_autorisation':
        return 'dashboard:demande_auto:'