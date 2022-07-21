import os
from AlpasProject.settings.base import *

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ['*']

CUSTOM_APPS = [
    'user',
    'core'
]

THIRD_PARTY_APPS = [
    'crispy_forms'
]


INSTALLED_APPS += CUSTOM_APPS
INSTALLED_APPS += THIRD_PARTY_APPS


DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': os.environ.get('POSTGRES_DB'),

        'USER': os.environ.get('POSTGRES_USER'),

        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),

        'HOST': os.environ.get('DB_HOST'),

        'PORT': os.environ.get('DB_PORT'),

    }

}
