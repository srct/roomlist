# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
# override all the things for the production environment
from __future__ import absolute_import
import os
from .settings import *
from . import secret

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['roomlist.gmu.edu']

PIWIK_DOMAIN_PATH = 'https://piwik.srct.gmu.edu/'
PIWIK_SITE_ID = 4

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secret.DB_NAME,
        'USER': secret.DB_USER,
        'PASSWORD': secret.DB_PASSWORD,
        'HOST': secret.DB_HOST,
        'PORT': secret.DB_PORT,
    }
}

# example.com is 1
# roomlist.srct.gmu.edu is 2
# roomlist.gmu.edu is 3
SITE_ID = 3

# where the static files are being hosted from
STATIC_ROOT = '/srv/roomlist/static'
# can haz ssl certs
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# use redis cache when not in local development
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        # configure to redis port
        'LOCATION': 'localhost:6379',
     },
}

# need to configure ADMINS email so that ERROR level logs (500 level exceptions)
# can be sent out

# https://docs.djangoproject.com/en/1.7/topics/logging/
# https://docs.djangoproject.com/en/1.7/howto/error-reporting/
# https://docs.python.org/2/library/logging.config.html#configuration-dictionary-schema

# use the *real*, non development email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# the email address that error messages come from; sent to admins
SERVER_EMAIL = ''
ADMINS = (('Roomlist Devs', 'roomlist@lists.srct.gmu.edu'),
          ('SRCT Execs', 'srct@gmu.edu'),)

# logging into the mail server
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = secret.EMAIL_HOST_PASSWORD
# includes implicit TLS
EMAIL_USE_SSL = False

LOGGING = {
    'version': 1,
    # the ones the print everything out to the terminal
    # and the ones that email on SuspiciousOperation occurrences
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            # make sure to change this to the proper path, and one that
            # can be written to
            'filename': '/srv/roomlist/debug.log',
        },
        # 'mail_admins' by default does not include a traceback attachment
        # setting 'include_html' to True will attach an html traceback file to the email
        # you can also set an additional 'email_backend' arg to a custom email handler (e.g. SES)
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        # logs request errors
        # 5XX responses are raised as ERROR messages
        # 4XX responses are raised as WARNING messages
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file',],
            'propagate': True,
        },
    # django's default loggers send request and security messages at the ERROR
    # or CRITICAL level to the AdminEmailHandler via mail_admins
    },
}
