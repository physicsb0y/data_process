from .base import *
from decouple import config


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-v94y0^1069o0a9filc12c&083l@5^f2rq-!6fyd5gjxj(+=_^j"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']




# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config('POSTGRES_DB'),
        "USER": config('POSTGRES_USER'),
        "PASSWORD": config('POSTGRES_PASSWORD'),
        "HOST": config('POSTGRES_HOST'),
        "PORT": config('POSTGRES_PORT'),
    }
}


