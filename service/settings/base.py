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

INSTALLED_APPS = [
	"unfold",
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	"phonenumber_field",
    'dal',
    'dal_select2',
	# Local apps
	"resources.core",
	"resources.users",
	"resources.cars",
]

MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
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

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'service/static')

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
