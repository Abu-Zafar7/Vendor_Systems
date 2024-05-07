from django.apps import AppConfig


class VendorsConfig(AppConfig):
    name = 'app'

    def ready(self):
        import app.signals