from .base import *  # noqa: F403

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "localhost:8100"]

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
	}
}

LOGGING = {
    **LOGGING,  # noqa: F405
    'loggers': {
        **LOGGING['loggers'],  # noqa: F405
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django.template': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
