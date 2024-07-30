import os
from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENVIRONMENT = os.environ.get("ENVIRONMENT")

if ENVIRONMENT == "production":
    environ.Env.read_env(os.path.join(BASE_DIR, "envs", ".env.production"))
else:
    environ.Env.read_env(os.path.join(BASE_DIR, "envs", ".env.local"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = []

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne",
    "django.contrib.staticfiles",
    "apps.users.apps.UsersConfig",
    "apps.banners.apps.BannersConfig",
    "apps.films.apps.FilmsConfig",
    "apps.cinemas.apps.CinemasConfig",
    "apps.halls.apps.HallsConfig",
    "apps.news.apps.NewsConfig",
    "apps.promotions.apps.PromotionsConfig",
    "apps.pages.apps.PagesConfig",
    "apps.mailing.apps.MailingConfig",
    "apps.schedule.apps.ScheduleConfig",
    "apps.booking.apps.BookingConfig",
    "ajax_datatable",
    "channels",
    "mathfilters",
    "django_cleanup.apps.CleanupConfig"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.utilities.middlewares.LanguageMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.app_directories.Loader",
                "django.template.loaders.filesystem.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.utilities.context_processors.main_page_context"
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

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

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True

USE_TZ = True

LANGUAGE_CODE = 'uk'

LANGUAGES = [
    ('en', 'English'),
    ('uk', 'Українська'),
]

LOCALE_PATHS = [str(BASE_DIR / "locale")]

STATIC_ROOT = str(BASE_DIR / "staticfiles")

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = str(BASE_DIR / "media")

MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "apps.users.authentication.EmailBackend",
]

AJAX_DATATABLE_STRIP_HTML_TAGS = False

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
