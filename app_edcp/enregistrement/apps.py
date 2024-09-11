from django.apps import AppConfig

class EnregistrementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'enregistrement'

    def ready(self):
        """ 
            activer et enregistrer le signal défini dans enregistrement et demarre avec l'application Django
        """
        import enregistrement.signals  # Importez les signaux ici

