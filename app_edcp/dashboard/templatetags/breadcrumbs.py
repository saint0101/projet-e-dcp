"""
Custom tag pour la gestion du fil d'ariane (breadcrumbs).
Permet de récupérer le texte et l'url de l'élément à afficher.
Utilise la fonction split() avec comme séparateur ' / '.
"""

from django import template
from django.template.defaultfilters import stringfilter

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