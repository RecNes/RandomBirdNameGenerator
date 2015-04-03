# -*- codign: utf-8 -*-
"""
Django settings for RandomBirdNameAPI project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# ABS_PATH = os.path.abspath(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's%a3+ow-)an7ezkr3qk+uojr@k9mm&wsq3%hhzv1+tyc5*+29j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sencer Hamarat', 'sencerhamarat@gmail.com'),
)

MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sencerhamarat@gmail.com'
EMAIL_HOST_PASSWORD = 'selpak_35-k1ng.0fpa1n-'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Random Bird name Generator <info@randombirdnamegenerator.com>'
SERVER_EMAIL = 'server@randombirdnamegenerator.com'
EMAIL_SUBJECT_PREFIX = '[ RBNG ]'

ALLOWED_HOSTS = ['randombirdnamegenerator.herokuapp.com',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rbnapi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'RandomBirdNameAPI.urls'

WSGI_APPLICATION = 'RandomBirdNameAPI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "l10n"),
)
USE_TZ = True
TIME_ZONE = 'UTC'
DATE_FORMAT = '%d/%m/%Y, %D'
TIME_FORMAT = '%H:%i'
DATETIME_FORMAT = '%d/%m/%Y, %D %H:%i'
SHORT_DATE_FORMAT = '%d/%m/%Y'
SHORT_DATETIME_FORMAT = '%d/%m/%Y %H:%i'
DATE_INPUT_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%d-%m-%Y")
FIRST_DAY_OF_WEEK = 1  # Default = 0 (Sunday)

USE_I18N = True
USE_L10N = True

LANGUAGES = (
    ('en', _('English')),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'PAGE_SIZE': 1,
}