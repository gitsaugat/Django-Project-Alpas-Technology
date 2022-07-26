import os
from AlpasProject.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

CUSTOM_APPS = [
    'users',
    'core'
]

THIRD_PARTY_APPS = [

]


INSTALLED_APPS += CUSTOM_APPS
INSTALLED_APPS += THIRD_PARTY_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
