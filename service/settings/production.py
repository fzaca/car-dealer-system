from .base import *  # noqa: F403

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=[]).split(",")  # noqa: F405
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default=[]).split(",")  # noqa: F405

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql",
		"NAME": config("DB_NAME"),  # noqa: F405
		"USER": config("DB_USER"),  # noqa: F405
		"PASSWORD": config("DB_PASSWORD"),  # noqa: F405
		"HOST": config("DB_HOST"),  # noqa: F405
		"PORT": config("DB_PORT"),  # noqa: F405
	}
}


LOGGING = {
    **LOGGING,  # noqa: F405
    'loggers': {
        **LOGGING['loggers'],  # noqa: F405
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.utils.autoreload': {
            'handlers': ['console'],
            'level': 'INFO',  # NOTE: Level in `Info` for reduce noise
            'propagate': False,
        }
    },
}
