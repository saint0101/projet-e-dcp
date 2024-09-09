import psycopg2  # Bibliothèque pour se connecter à une base de données PostgreSQL

# Détails de la connexion à la base de données PostgreSQL
db_config = {
    'dbname': 'edcp_db',  # Nom de la base de données
    'user': 'Uroot_edcp',  # Nom d'utilisateur pour accéder à la base de données
    'password': 'e_dcp@2023#',  # Mot de passe de l'utilisateur
    'host': 'localhost',  # Adresse du serveur PostgreSQL (ici, sur la machine locale)
    'port': '5436'  # Port d'écoute du serveur PostgreSQL
}

try:
    # Connexion à la base de données PostgreSQL avec les détails spécifiés dans db_config
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()  # Création d'un curseur pour exécuter les commandes SQL

    # Lire le fichier SQL qui contient les commandes à exécuter
    with open('integ/edcp_db_server_no_structure.sql', 'r', encoding='utf-8') as sql_file:
        sql_commands = sql_file.read()  # Lire tout le contenu du fichier SQL

    # Séparer les différentes commandes SQL en utilisant le point-virgule comme séparateur
    commands = sql_commands.split(';')

    # Boucle sur chaque commande SQL
    for command in commands:
        try:
            # Vérifier si la commande n'est pas vide avant de l'exécuter
            if command.strip():
                # Vérification spécifique avant d'exécuter une commande INSERT INTO
                if "INSERT INTO" in command:
                    # Vérification si un enregistrement avec l'ID 1 existe déjà dans la table auth_permission
                    check_command = "SELECT EXISTS(SELECT 1 FROM auth_permission WHERE id = 1);"
                    cursor.execute(check_command)  # Exécuter la commande de vérification
                    exists = cursor.fetchone()[0]  # Récupérer le résultat

                    if exists:
                        # Si l'enregistrement existe déjà, afficher un message et ne pas réinsérer
                        print(f"L'enregistrement existe déjà : {command}")
                    else:
                        # Sinon, exécuter la commande INSERT et valider la transaction
                        cursor.execute(command)
                        connection.commit()
                else:
                    # Exécution des autres types de commandes SQL (non INSERT)
                    cursor.execute(command)
                    connection.commit()
        except psycopg2.IntegrityError as e:
            # Si une erreur d'intégrité (doublons, etc.) survient, on annule la transaction et affiche l'erreur
            print(f"Erreur d'intégrité pour la commande : {command}")
            connection.rollback()  # Annuler la transaction pour cette commande
        except Exception as e:
            # Si une autre exception survient, on l'affiche et on annule également la transaction
            print(f"Erreur lors de l'exécution : {e}")
            connection.rollback()  # Annuler la transaction

    print("Données intégrées avec succès.")  # Message de succès si toutes les commandes sont exécutées correctement

except (Exception, psycopg2.DatabaseError) as error:
    # Gestion des erreurs de connexion ou d'exécution de base de données
    print(f"Erreur lors de l'intégration des données: {error}")
    connection.rollback()  # Annuler la transaction en cas d'erreur globale

finally:
    # Fermeture de la connexion à la base de données
    if connection:
        cursor.close()  # Fermer le curseur
        connection.close()  # Fermer la connexion à la base de données