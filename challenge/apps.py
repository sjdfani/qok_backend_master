from django.apps import AppConfig


class ChallengeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'challenge'

    def ready(self) -> None:
        from .auto_job import main
        main()
