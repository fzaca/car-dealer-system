import random

from django.conf import settings
from django.utils.translation import gettext_lazy as _


def environment_callback(request):
    if settings.ENV == "production":
        return [_("Production"), "warning"]

    return [_(f"Development:{settings.ENV}"), "info"]


def badge_callback(request):
    return f"+{random.randint(1, 99)}"


def permission_callback(request):
    return True
