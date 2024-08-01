from .base import *  # noqa: F403

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])  # noqa: F405
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])  # noqa: F405
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[])  # noqa: F405

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

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{env("REDIS_USER", default="default")}:'  # noqa: F405
                    f'{env("REDIS_PASSWORD", default="")}@'  # noqa: F405
                    f'{env("REDIS_HOST", default="localhost")}:'  # noqa: F405
                    f'{env("REDIS_PORT", default="6379")}/1',  # noqa: F405
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
