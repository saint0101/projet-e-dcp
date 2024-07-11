"""
Commande Django pour attendre que la base de données soit disponible.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Commande Django pour attendre que la base de données soit disponible."""

    def handle(self, *args, **options):
        """
        Point d'entrée de la commande.
        """
        # Afficher un message pour indiquer que nous
        # attendons que la base de données soit disponible
        self.stdout.write('En attente de la base de données...')
        # Variable pour suivre l'état de la base de données
        db_up = False
        # Boucle pour attendre que la base de données soit disponible
        while db_up is False:
            try:
                # Vérifier l'état de la base de données
                self.check(databases=['default'])
                # Marquer la base de données comme disponible si la vérification réussit
                db_up = True
            except (Psycopg2OpError, OperationalError):
                # La base de données n'est pas disponible, attendre 1 seconde avant de réessayer
                self.stdout.write('Base de données non disponible, attente de 1 seconde...')
                time.sleep(1)

        # Afficher un message pour indiquer que la base de données est disponible
        self.stdout.write(self.style.SUCCESS('Base de données disponible !'))
