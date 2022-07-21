import os
from django.core.exceptions import ImproperlyConfigured

APP_MODE = os.environ.get('MODE')

if not APP_MODE:
    raise ImproperlyConfigured("No mode specified for project")
if APP_MODE == 'DEV':
    from AlpasProject.settings.dev import *
elif APP_MODE == 'PROD':
    from AlpasProject.settings.prod import *
else:
    raise ImproperlyConfigured(
        "Please specify correct mode in your env file MODE=DEV or MODE=PROD")
