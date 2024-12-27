from django.apps import AppConfig


class VvpatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vvpat'

    def ready(self):
        import vvpat.signals
