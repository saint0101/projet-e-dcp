"""
Custom tag pour la gestion du fil d'ariane (breadcrumbs).
Permet de récupérer le texte et l'url de l'élément à afficher.
Utilise la fonction split() avec comme séparateur ' / '.
"""

from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import FileField

register = template.Library()

@register.filter
@stringfilter
def get_bread_text(value, arg):
    """Split la chaîne en paramètre et renvoie la prmeière occurence (correspondant au texte à afficher)"""
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
    Affiche l'URL et le nom du fichier sous forme de lien
    Le nom du fichier est le dernier élément du path
    """
    if value :
        fileurl = value.url
        filename = value.name.split('/')[-1]
        return f'<a href="{fileurl}">{filename}</a>'
    
    return '<a href="#">Vide</a>'


@register.filter
def get_file_fields(instance):
    """
    Retourne la liste des champs FileField de l'instance.
    Utilisé pour l'affichage des fichiers justificatifs
    """
    return [field for field in instance._meta.get_fields() if isinstance(field, FileField)]


@register.filter
def attr(obj, attr_name):
    """
    Renvoie la valeur du champ attr_name de l'objet.
    Utilisé pour l'affichage dynamique des fichiers justificatifs
    """
    return getattr(obj, attr_name, None)