import os
from decouple import config

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings.local")
os.environ.setdefault("ENV", config("ENV", default="local"))


application = get_wsgi_application()
