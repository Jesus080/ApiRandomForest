"""
Apps configuration para la aplicación predictor.
"""
from django.apps import AppConfig


class PredictorConfig(AppConfig):
    """Configuración de la app predictor."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictor'
    verbose_name = 'Malware Detector'
    
    def ready(self):
        """
        Se ejecuta cuando la aplicación está lista.
        Aquí podríamos pre-cargar el modelo si fuera necesario.
        """
        pass
