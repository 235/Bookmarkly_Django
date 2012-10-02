"""Base settings shared by all environments"""
# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *   # pylint: disable=W0614,W0401

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k2s1xfejf)b5+vb=^3@uu6@kxodzst+8z+v!$^+c705+8ft)p_'

INSTALLED_APPS = (
    'app.apps.auth',
    'app.apps.collection',

    #'south',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

#==============================================================================
# Calculation of directories relative to the project module location
#==============================================================================

import os
import sys
import app as project_module

PROJECT_DIR = os.path.dirname(os.path.realpath(project_module.__file__))

PYTHON_BIN = os.path.dirname(sys.executable)
ve_path = os.path.dirname(os.path.dirname(os.path.dirname(PROJECT_DIR)))
# Assume that the presence of 'activate_this.py' in the python bin/
# directory means that we're running in a virtual environment.
#if os.path.exists(os.path.join(PYTHON_BIN, 'activate_this.py')):
#    # We're running with a virtualenv python executable.
#    VAR_ROOT = os.path.join(os.path.dirname(PYTHON_BIN), 'var')
#elif ve_path and os.path.exists(os.path.join(ve_path, 'bin',
#        'activate_this.py')):
#    # We're running in [virtualenv_root]/src/[project_name].
#    VAR_ROOT = os.path.join(ve_path, 'var')
#else:
#    # Set the variable root to a path in the project which is
#    # ignored by the repository.
#    VAR_ROOT = os.path.join(PROJECT_DIR, 'var')
VAR_ROOT = os.path.join(PROJECT_DIR, '..')

if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)

#==============================================================================
# Project URLS and media settings
#==============================================================================

ROOT_URLCONF = 'app.urls'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/public/'
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(VAR_ROOT, 'public')
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'public'),
)

#==============================================================================
# Templates
#==============================================================================

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
)

#==============================================================================
# Middleware
#==============================================================================
MIDDLEWARE_CLASSES += (
    'app.apps.disable_csrf.DisableCSRF',
)

#==============================================================================
# Auth / security
#==============================================================================

AUTHENTICATION_BACKENDS += (
)

#==============================================================================
# Miscellaneous project settings
#==============================================================================

#==============================================================================
# Third party app settings
#==============================================================================