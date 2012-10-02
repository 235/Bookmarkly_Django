"""
Example settings for local development

Use this file as a base for your local development settings and copy
it to app/settings/local.py. It should not be checked into
your code repository.

"""
from app.settings.base import *   # pylint: disable=W0614,W0401

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('You', 'your@email'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VAR_ROOT, 'dev.db'),
    }
}

# ROOT_URLCONF = 'app.urls.local'
# WSGI_APPLICATION = 'app.wsgi.local.application'
