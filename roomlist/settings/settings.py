"""
Django settings for roomlist project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from __future__ import absolute_import, print_function

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ORGANIZATION_EMAIL_DOMAIN = 'masonlive.gmu.edu'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'housing/templates'),
    os.path.join(BASE_DIR, 'accounts/templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_LOADERS = (

    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

from . import config
DEBUG = config.DEBUG
TEMPLATE_DEBUG = config.TEMPLATE_DEBUG
ALLOWED_HOSTS = config.ALLOWED_HOSTS

PIWIK_DOMAIN_PATH = config.PIWIK_DOMAIN_PATH
PIWIK_SITE_ID = config.PIWIK_SITE_ID

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    # apps
    'api',
    'housing',
    'accounts',
    # packages
    'crispy_forms',
    'django_gravatar',
    'analytical',
    'randomslugfield',
    'haystack',
    'multiselectfield',
    # social media authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.instagram',
    # 'allauth.socialaccount.providers.tumblr',
    # 'allauth.socialaccount.providers.spotify',
    # 'allauth.socialaccount.providers.github',
    # twitch? stackexchange? soundcloud?
)

CRISPY_TEMPLATE_PACK = 'bootstrap'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cas.middleware.CASMiddleware',
    'django.middleware.doc.XViewMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# for bootstrap css classes
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {messages.ERROR: 'danger',}

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'settings.wsgi.application'

from . import secret

SECRET_KEY = secret.SECRET_KEY

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config.DB_ENGINE,
        'NAME': secret.DB_NAME,
        'USER': secret.DB_USER,
        'PASSWORD': secret.DB_PASSWORD,
        'HOST': secret.DB_HOST,
        'PORT': secret.DB_PORT,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# set for social auth
# example.com is by default set to 1

SITE_ID = 2

# further settings for social auth

SOCIALACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['public_profile', ],
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'link',
            ]
        }
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)

# Peoplefinder API for user creation
PF_URL = "http://api.srct.gmu.edu/pf/v1/"

CAS_SERVER_URL = 'https://login.gmu.edu'
CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True

CAS_RESPONSE_CALLBACKS = (
    'accounts.cas_callbacks.create_user',
)

HAYSTACK_CONNECTIONS = {
    'default' : {
        'ENGINE' : 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH' : os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# Haystack Signal Processor
# The RealtimeSignalProcessor allows for objects to indexed as soon as
# they are created -- in real time.
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Use redis cache when not in local development
if DEBUG:
    pass
else:
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '/var/run/redis/redis.sock',
        },
    }

# need to configure ADMINS email so that ERROR level logs (500 level exceptions)
# can be sent out

# https://docs.djangoproject.com/en/1.7/topics/logging/
# https://docs.djangoproject.com/en/1.7/howto/error-reporting/
# https://docs.python.org/2/library/logging.config.html#configuration-dictionary-schema

if not DEBUG:

    ADMINS = config.ADMINS
    SERVER_EMAIL = config.SERVER_EMAIL
    EMAIL_HOST = config.EMAIL_HOST
    EMAIL_PORT = config.EMAIL_PORT
    EMAIL_HOST_USER = config.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
    EMAIL_USE_SSL = config.EMAIL_USE_SSL

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                # make sure to change this to the proper path, and one that
                # can be written to
                'filename': '/path/to/django/debug.log',
            },
        },
        # logs request errors
        'loggers': {
            'django.request': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
