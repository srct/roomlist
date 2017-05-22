"""
Django settings for roomlist project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# standard library imports
from __future__ import absolute_import, print_function
import os
# core django imports
from django.contrib.messages import constants as messages
# imports from your apps
from . import secret

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# cryptography
SECRET_KEY = secret.SECRET_KEY

# These configurations are set by default for a local development environment. Turning
# off debug mode will display 404 and 500 error pages instead of detailed logs.
DEBUG = True
# the domains this application will be deployed on, e.g. which
# domains this app should listen to requests from.
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # where template files are located
            os.path.join(BASE_DIR, 'templates'),
            # may specify to avoid requiring paths
            os.path.join(BASE_DIR, 'housing/templates'),
            os.path.join(BASE_DIR, 'accounts/templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': DEBUG,
        }
    }
]

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
    'welcome',
    'core',
    # packages
    'analytical',
    'cas',
    'crispy_forms',
    'django_gravatar',
    'haystack',
    'multiselectfield',
    'randomslugfield',
    'rest_framework',
    # social media authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.tumblr',
    'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.spotify',
    # twitch? stackexchange? soundcloud?
)

CRISPY_TEMPLATE_PACK = 'bootstrap'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cas.middleware.CASMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'settings.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        # If you want to change the database engine you are free to do so here.
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'roomlist',
        'USER': 'roommate',
        'PASSWORD': secret.DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '',
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
# add localhost and it will be 2
SITE_ID = 2

# further settings for social auth
# custom account adapter
SOCIALACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'

# specifying what information is being requested from Facebook
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

# for bootstrap css classes
MESSAGE_TAGS = {messages.ERROR: 'danger', }

# for using Mason's Central Authentication Service
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)
# Mason's CAS endpoint-- note the lack of a trailing slash... actually matters
CAS_SERVER_URL = 'https://login.gmu.edu'
CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True
CAS_RESPONSE_CALLBACKS = (
    'accounts.cas_callbacks.create_user',
)
# Peoplefinder API endpoint for user creation in the CAS callback (above)
PF_URL = "http://api.srct.gmu.edu/pf/v1/"
# email address used in CAS callback
ORGANIZATION_EMAIL_DOMAIN = 'masonlive.gmu.edu'

# haystack is the package used for search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
# Haystack Signal Processor
# The RealtimeSignalProcessor allows for objects to indexed as soon as
# they are created -- in real time.
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# dummy cache for development-- doesn't actually cache things
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# configure piwik analytics
# point to the piwik url
PIWIK_DOMAIN_PATH = 'piwik.example.com'
# set piwik server site id (piwik can track multiple websites)
PIWIK_SITE_ID = 1

# email for the development environment
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
