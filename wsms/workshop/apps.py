from django.apps import AppConfig


class WorkshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workshop'
    def ready(self):
    # Import the signals module
        import workshop.signals
