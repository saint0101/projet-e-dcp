## Regroupe les méthodes utilisées pour la validation des champs des formulaires

import re
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from base_edcp.models import User


def validate_unique_email(value):
  """
  Validation de l'adresse email :
  - ne doit pas être déjà utilisée
  - doit avoir une longueur max
  """
  # si l'email existe
  if User.objects.filter(email=value).exists():
    raise ValidationError("Cet adresse e-mail est déjà utilisée.")
  
  if len(value) > 254:
    raise ValidationError("L'adresse e-mail doit avoir une longueur max de 254 caractères.")
  
  if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
    raise ValidationError("L'adresse e-mail doit être valide.")
    

def validate_charfield(value):
  """
  Validation des champs textuels (nom, prénoms, adresse, descriptions etc.) :
  - ne doit pas contenir de caractères spéciaux ni de chiffres
  - doit avoir une longueur min et une longueur max
  """
  if len(value) > 100:
    raise ValidationError("Le texte doit avoir une longueur maximum de 100 caractères.")

  if len(value)  < 2:
    raise ValidationError("Le texte est trop court.")
    

def validate_phone_number(value):
  """
  Validation du numéro de téléphone :
  - doit être au format (+)XXXXXXXXXXX
  """
  phone_regex = re.compile(r'^\+?1?\d{9,16}$')
  if not phone_regex.match(value):
    raise ValidationError("Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 16 chiffres autorisés.")
  

def validate_image_size(value):
    """
    Validation des champs image :
    - doit avoir une taille max
    - doit être une image
    """
    max_size_kb = 1024  # Example: 1 MB limit
    if value.size > max_size_kb * 1024:
        raise ValidationError(f"Le fichier dépasse la taille maximale de {max_size_kb} KB.")
    
    # Check if the uploaded file is an image
    try:
        w, h = get_image_dimensions(value)
    except AttributeError:
        raise ValidationError("Le fichier téléchargé n'est pas une image.")
