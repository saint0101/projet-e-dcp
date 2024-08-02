# Fonctionnalités et actions

## Formulaires

- Ajouter/configurer les validateurs (backend)
- Ajouter les validateurs côté client (JavaScript)

## Inscription

- Ajouter le recueil du consentement
- Insérer l'email de l'utilisateur dans le message de confirmation après l'inscription (connexion -> views.py). Penser à masquer les caractères par des **

## Enregistrement

- Ajouter la prise en charge des fichiers à joindre
- Mettre à jour l'affichage dynamique des champs avec les nouveaux champs (copie RCCM, type de pièce)

## Désignation du Correspondant

- Ajouter la possibilité pour l'utilisateur de liéer son propre compte s'il est déjà le Correspondant
- Ajouter la fonction de génération du mot de passe aléatoire
- Ajouter l'envoi du lien de réinitialisation du mot de passe à l'adresse du DPO

## Paramètres

- Prévoir une Table `Paramètres` pour permettre à l'administrateur de modifier les paramètres tels que la taille max des fichiers à uploader, la longueur des champs etc.

## Sécurité

- Réactiver les règles de validation des mots de passe dans settings.py avant la mise en production
