from django.apps import AppConfig


class AgendaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agenda'

    def ready(self):
        from .q import start
        start()