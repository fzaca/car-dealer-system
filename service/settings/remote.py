from .base import *  # noqa: F403


ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "localhost:8100"]
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']
CORS_ORIGIN_WHITELIST = ['http://localhost:8000']


DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql",
		"NAME": env("DB_NAME"),  # noqa: F405
		"USER": env("DB_USER"),  # noqa: F405
		"PASSWORD": env("DB_PASSWORD"),  # noqa: F405
		"HOST": env("DB_HOST"),  # noqa: F405
		"PORT": env("DB_PORT"),  # noqa: F405
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
