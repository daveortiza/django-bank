"""
        Django settings for local development
"""

from project.base import *


SECRET_KEY = '**************************************************'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 1

ALLOWED_HOSTS = ['0.0.0.0', 'app.local', ]

WSGI_APPLICATION = 'project.wsgi_local.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


if 'DB_SERVICE' in os.environ and os.environ['DB_SERVICE'] == 'postgres':

    # Running the Docker image

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': os.environ['DB_SERVICE'],
            'PORT': os.environ['DB_PORT']
        }
    }

    # Redis

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'django',
            'USER': 'django',
            'PASSWORD': 'django',
            'HOST': 'postgres',
            'PORT': 5432
        }
    }

    #  from django.db import DatabaseError
    #  raise DatabaseError()
