import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)

# Lee el archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, 'environments', f"{os.getenv('ENV', 'local')}.env"))

SECRET_KEY = env('SECRET_KEY', default='your-secret-key')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
DEBUG = env.bool('DEBUG', default=True)
APPS_DIR = BASE_DIR / "resources"
ENV = env.bool("ENV", default="local")

UNFOLD = {
    "SITE_TITLE": "Car Dealer Admin",
    "SITE_HEADER": "Car Dealer",
	"COLORS": {
		"primary": {
			"50": "240 248 255",
			"100": "224 240 255",
			"200": "192 220 255",
			"300": "160 200 255",
			"400": "128 180 255",
			"500": "96 160 255",
			"600": "64 140 255",
			"700": "32 120 255",
			"800": "0 100 255",
			"900": "0 80 220",
			"950": "0 60 180"
		}
	},
}

INSTALLED_APPS = [
	"unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	'whitenoise.runserver_nostatic',
	"phonenumber_field",
	# Local apps
	"resources.core",
	"resources.users",
	"resources.cars",
	"resources.sales",
	"resources.reviews",
]

MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
	"whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "service.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'resources/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = "service.wsgi.application"

DATABASES = {}

AUTH_USER_MODEL = "users.CustomUser"
AUTH_PASSWORD_VALIDATORS = [
	{
		"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
	},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = ["service/static"]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
	"version": 1,
	"disable_existing_loggers": False,
	"formatters": {
		"verbose": {
			"format": "{levelname} {asctime} {module} {message}",
			"style": "{",
		},
		"simple": {
			"format": "{levelname} {message}",
			"style": "{",
		},
		"detailed": {
			"format": "{levelname} {asctime} {filename} {funcName}():{lineno} | {message}",
			"style": "{",
		},
		"rich": {
			"datefmt": "[%X]",
			"style": "{",
		},
	},
	"handlers": {
		"console": {
			"level": "DEBUG",
			"class": "rich.logging.RichHandler",
			"formatter": "rich",
		},
	},
	"loggers": {
		"django": {
			"handlers": ["console"],
			"level": "INFO",
			"propagate": True,
		},
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.utils.autoreload': {
            'handlers': ['console'],
            'level': 'INFO',  # NOTE: Level in `Info` for reduce noise
            'propagate': False,
        }
    }
}
