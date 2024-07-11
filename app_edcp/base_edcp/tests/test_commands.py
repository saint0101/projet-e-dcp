# -*- encoding: utf-8 -*-

"""
Test custom Django management commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Substitution de la méthode 'check'
# dans la classe 'Command' du module 'wait_for_db'
@patch('base_edcp.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Tests de la commande"""

    # Test de vérification si la base de données est prête
    def test_wait_for_db_ready(self, patched_check):
        """Test d'attente de la base de données si elle est disponible"""
        # Définition de la valeur de retour de la méthode 'check' simulée à True
        patched_check.return_value = True

        # Appel de la commande 'wait_for_db'
        call_command('wait_for_db')

        # Vérification que la méthode 'check' a été appelée une fois avec databases=['default']
        patched_check.assert_called_once_with(databases=['default'])

    # Test d'attente de la base de données avec des erreurs opérationnelles
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test d'attente de la base de données en cas d'erreur opérationnelle."""
        # Configuration de l'effet secondaire de la méthode 'check'
        # simulée pour lever Psycopg2Error deux fois,
        # OperationalError trois fois, puis retourner True
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

        # Appel de la commande 'wait_for_db'
        call_command('wait_for_db')

        # Vérification que la méthode 'check' a été appelée six fois
        self.assertEqual(patched_check.call_count, 6)
        # Vérification que la méthode 'check' a été appelée avec databases=['default']
        patched_check.assert_called_with(databases=['default'])
