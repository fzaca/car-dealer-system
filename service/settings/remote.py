from .base import *  # noqa: F403

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql",
		"NAME": config("POSTGRES_DB"),  # noqa: F405
		"USER": config("POSTGRES_USER"),  # noqa: F405
		"PASSWORD": config("POSTGRES_PASSWORD"),  # noqa: F405
		"HOST": "postgres",  # NOTE: If you are in the compose this field is the service name
		"PORT": "5432",
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
