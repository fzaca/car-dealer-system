from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "resources.users"

    def ready(self):  # noqa: PLR6301
        import resources.users.signals  # noqa: F401, PLC0415
