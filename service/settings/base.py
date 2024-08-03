import os
import environ
from pathlib import Path

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

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
    "django.contrib.humanize",
	"whitenoise.runserver_nostatic",
	"phonenumber_field",
	"nanoid_field",
    "memoize",
    "django_select2",
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

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "silk",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "silk.middleware.SilkyMiddleware",
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
        'INTERCEPT_REDIRECTS': False,
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

ROOT_URLCONF = "service.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'resources/core/templates'],
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

# https://fonts.google.com/icons
UNFOLD = {
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("images/logo.svg"),
        "dark": lambda request: static("images/logo.svg"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("images/logo.svg"),
        "dark": lambda request: static("images/logo.svg"),
    },
    "SITE_TITLE": _("Car Dealer Admin"),
    "SITE_HEADER": _("Car Dealer"),
    "SITE_SYMBOL": "directions_car",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("images/favicon.ico"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "resources.core.utils.environment_callback",
    "DASHBOARD_CALLBACK": "resources.core.pages.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("images/car-dealer-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
    },
    "STYLES": [
        lambda request: static("css/styles.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/scripts.js"),
    ],
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
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "badge": "resources.core.utils.badge_callback",  # FIXME: Example for use in others apps
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Cars"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Body types"),
                        "icon": "Garage",  # https://fonts.google.com/icons
                        "link": reverse_lazy("admin:cars_bodytype_changelist"),
                    },
                    {
                        "title": _("Brands"),
                        "icon": "local_offer",
                        "link": reverse_lazy("admin:cars_brand_changelist"),
                    },
                    {
                        "title": _("Car models"),
                        "icon": "auto_awesome_motion",
                        "link": reverse_lazy("admin:cars_carmodel_changelist"),
                    },
                    {
                        "title": _("Cars"),
                        "icon": "directions_car",
                        "link": reverse_lazy("admin:cars_car_changelist"),
                    },
                    {
                        "title": _("Featured cars"),
                        "icon": "star",
                        "link": reverse_lazy("admin:cars_featuredcar_changelist"),
                    },
                ],
            },
            {
                "title": _("Reviews"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Comments"),
                        "icon": "comment",
                        "link": reverse_lazy("admin:reviews_comment_changelist"),
                    },
                    {
                        "title": _("Reviews"),
                        "icon": "rate_review",
                        "link": reverse_lazy("admin:reviews_review_changelist"),
                    },
                ],
            },
            {
                "title": _("Sales"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Invoices"),
                        "icon": "receipt",
                        "link": reverse_lazy("admin:sales_invoice_changelist"),
                    },
                    {
                        "title": _("Payment methods"),
                        "icon": "payment",
                        "link": reverse_lazy("admin:sales_paymentmethod_changelist"),
                    },
                    {
                        "title": _("Payments"),
                        "icon": "attach_money",
                        "link": reverse_lazy("admin:sales_payment_changelist"),
                    },
                    {
                        "title": _("Sales"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:sales_sale_changelist"),
                    },
                ],
            },
            {
                "title": _("Users & Groups"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Customers"),
                        "icon": "recent_actors",
                        "link": reverse_lazy("admin:users_customer_changelist"),
                    },
                    {
                        "title": _("Employees"),
                        "icon": "support_agent",
                        "link": reverse_lazy("admin:users_employee_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "groups_3",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:users_customuser_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [],
}
