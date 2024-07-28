from django.apps import AppConfig


class EstacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estaciones'
    def ready(self):
        import estaciones.signals  # Import the signals module