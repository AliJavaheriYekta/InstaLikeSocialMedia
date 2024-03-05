from django.apps import AppConfig


class ContentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contents'

    def ready(self):
        # Call signal registration functions
        import contents.signals
