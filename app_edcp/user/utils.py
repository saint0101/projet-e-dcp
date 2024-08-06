import random
import string
from django.http import JsonResponse
from base_edcp.models import User

def generate_random_password(length=10):
    if length < 10:
        raise ValueError("Password length must be at least 10 characters.")
    
    # Define character sets
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    
    # Ensure the password has at least one character from each character set
    password = [
        random.choice(lowercase_letters),
        random.choice(uppercase_letters),
        random.choice(digits),
        random.choice(symbols),
    ]
    
    # Fill the remaining characters randomly
    all_characters = lowercase_letters + uppercase_letters + digits + symbols
    password += random.choices(all_characters, k=length - len(password))
    
    # Shuffle the password list to ensure randomness
    random.shuffle(password)
    
    # Convert the list to a string and return
    return ''.join(password)


def check_email(email):
    """
    Fonction de vérification de l'existence d'un email dans la base de données
    Returns : objet JSON
    """
    # si l'utilisateur avec l'email fourni en paramètre existe dans la BD
    if User.objects.filter(email=email).exists():
        print(f'email found : {email}')
        # récupération de l'utilisateur
        user=User.objects.get(email=email)
        print(f'user : {user}')
        print(f'is_dpo : {user.is_dpo}')

        # renvoi de l'objet JSON
        return JsonResponse({
            'email_exists': True, 
            'is_dpo': user.is_dpo
            })
    # renvoi de l'objet JSON si l'email n'existe pas
    print(f'email not found : {email}')
    return JsonResponse({'email_exists': False})


def create_new_user(data):
    """
    Fonction de création d'un nouvel utilisateur.
    Crée un mot de passe aléatoire par défaut.
    """
    # à remplacer par l'ajout d'une méthode random pour le mot de passe.
    # random_password = 'pbkdf2_sha256$600000$aM8OOxx8RVXcAA8ISDbNC5$CgJsb4SLOpQgiw8SEGEsO27PR07iW8YSL2kwA6ZVV8o='
    # Création d'un nouvel utilisateur
    new_user = User.objects.create_user(
        nom=data['nom'], 
        prenoms=data['prenoms'], 
        telephone=data['telephone'], 
        email=data['email'], 
        password='', 
        is_dpo=True, is_active=True, 
        must_reset = True,
        email_verified=False)
    
    password = generate_random_password(12)
    print(f'Password created : {password}')
    new_user.set_password(password)
    new_user.save()

    return new_user, password