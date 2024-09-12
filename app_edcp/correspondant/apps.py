from django.apps import AppConfig

class CorrespondantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'correspondant'

    def ready(self):
        """ 
            activer et enregistrer le signal défini dans correspondant et demarre avec l'application Django
        """
        import correspondant.signals  # Importez les signaux ici
