"""
Django settings for roomlist project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

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

print TEMPLATE_DIRS

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
    #'allauth.account.context_processors.account',
    #'allauth.socialaccount.context_processors.socialaccount',
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fGTL0pyk8MRq9YLXIOzFKZlneTdg3etdRxXs1FN2FqlVk595Ix'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'api',
    'housing',
    'accounts',
    'crispy_forms',
    'django_gravatar',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.instagram',
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

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'roomlist',
        'USER': 'django',
        'PASSWORD': 'H0jrp0llTJ',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)

CAS_SERVER_URL = 'https://login.gmu.edu'
CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True

CAS_RESPONSE_CALLBACKS = (
    'accounts.cas_callbacks.create_user',
)
