from django.apps import AppConfig


class ZadanieAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Zadanie_app'

    def ready(self):
        import Zadanie_app.signals


