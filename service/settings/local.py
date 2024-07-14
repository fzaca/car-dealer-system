from .base import *  # noqa: F403


ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "localhost:8100"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}
