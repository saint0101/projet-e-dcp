# Tests des Modèles de la Base de Données

Ce répertoire contient les tests unitaires pour vérifier le bon fonctionnement des modèles de la base de données utilisés dans le projet. Les tests sont réalisés avec le framework de test intégré de Django.

## Modèles Testés

Les modèles suivants sont testés dans ce projet :

1. **UserModel** : Vérifie la création d'utilisateurs, la normalisation des emails, et la création de superutilisateurs.
2. **TypeClientModel** : Vérifie la création et la gestion des types de clients, ainsi que leur représentation en chaîne de caractères.
3. **TypePieceModel** : Vérifie la création et la gestion des types de pièces, ainsi que leur représentation en chaîne de caractères.
4. **EnregistrementModel** : Vérifie la création d'enregistrements, l'association des relations entre les différents modèles, et l'utilisation des valeurs par défaut.
5. **PaysModel** : Vérifie la création de pays, leur représentation en chaîne de caractères, et la validation des champs obligatoires.
6. **SecteurModel** : Vérifie la création de secteurs, leur représentation en chaîne de caractères, et la validation des champs obligatoires.

## Structure des Tests

Chaque modèle possède sa propre classe de tests, définie comme suit :

### `UserModelTest`

- **`test_create_user_with_infos_successful`** : Teste la création d'un utilisateur avec des informations valides.
- **`test_new_user_email_normalized`** : Teste la normalisation des adresses email lors de la création d'un nouvel utilisateur.
- **`test_new_without_email_raises_error`** : Vérifie qu'une erreur est levée lors de la tentative de création d'un utilisateur sans email.
- **`test_create_superuser`** : Vérifie la création d'un superutilisateur avec les droits appropriés.

### `TypeClientModelTest`

- **`test_create_type_client_successful`** : Teste la création d'un type de client avec des données valides.
- **`test_str_representation`** : Vérifie la représentation en chaîne de caractères d'un type de client.
- **`test_create_type_client_default_values`** : Vérifie la création d'un type de client avec les valeurs par défaut pour les champs non spécifiés.

### `TypePieceModelTest`

- **`test_create_type_piece_successful`** : Teste la création d'un type de pièce avec des données valides.
- **`test_str_representation`** : Vérifie la représentation en chaîne de caractères d'un type de pièce.
- **`test_create_type_piece_default_values`** : Vérifie la création d'un type de pièce avec les valeurs par défaut pour les champs non spécifiés.

### `EnregistrementModelTest`

- **`test_create_enregistrement_successful`** : Teste la création d'un enregistrement avec des données valides et vérifie l'intégrité des relations entre les modèles.
- **`test_str_representation`** : Vérifie la représentation en chaîne de caractères d'un enregistrement.
- **`test_create_enregistrement_default_values`** : Vérifie la création d'un enregistrement avec les valeurs par défaut pour les champs non spécifiés.

### `PaysModelTest`

- **`test_create_pays_successful`** : Teste la création d'un pays avec des données valides.
- **`test_str_representation`** : Vérifie la représentation en chaîne de caractères d'un pays.
- **`test_pays_validation_without_required_fields`** : Vérifie que la validation échoue si les champs obligatoires ne sont pas fournis.

### `SecteurModelTest`

- **`test_create_secteur_successful`** : Teste la création d'un secteur avec des données valides.
- **`test_str_representation`** : Vérifie la représentation en chaîne de caractères d'un secteur.
- **`test_create_secteur_default_description`** : Vérifie la création d'un secteur avec une description par défaut (null).
- **`test_validation_without_required_fields`** : Vérifie que la validation échoue si les champs obligatoires ne sont pas fournis.

## Exécution des Tests

Pour exécuter les tests, utilisez la commande suivante dans votre terminal :

```bash
docker-compose exec app_edcp python manage.py test