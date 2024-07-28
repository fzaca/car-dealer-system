from django.apps import AppConfig


class CarsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "resources.cars"

    def ready(self):  # noqa: PLR6301
        import resources.cars.signals  # noqa: F401, PLC0415
