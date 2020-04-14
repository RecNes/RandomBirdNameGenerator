# coding: utf-8
"""
Django settings for rbnbase project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import json
import os

from django.utils.translation import ugettext_lazy as _

from .logging_settings import LOGGING, BASE_DIR

with open('secrets.txt', 'r') as f:
    SECRETS = json.load(f)[0]

LOGGING = LOGGING
# ABS_PATH = os.path.abspath(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG

ADMINS = (
    ('Sencer Hamarat', 'sencerhamarat@gmail.com'),
)

MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = SECRETS['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = SECRETS['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Random Bird name Generator <info@rbgn.recnes.com>'
SERVER_EMAIL = 'server@rbgn.recnes.com'
EMAIL_SUBJECT_PREFIX = '[ RBNG ]'

ALLOWED_HOSTS = SECRETS['ALLOWED_HOSTS'].split(',')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'gunicorn',
    'rbnapi',
    'rest_framework',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rbnbase.urls'

WSGI_APPLICATION = 'rbnbase.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

default_db = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': SECRETS['DBNAME'],
}

if SECRETS['DBNAME'] in ['postgresql', 'mysql', 'mariadb', 'oracle']:
    default_db.update({
        'ENGINE': 'django.db.backends.{}'.format(SECRETS['DBNAME']),
        'USER': SECRETS['DBUSER'],
        'PASSWORD': SECRETS['DBPASSWORD'],
        'HOST': SECRETS['DBHOST'],
        'PORT': SECRETS['DBPORT'],
    })
    
    
DATABASES = {default_db}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LOCALE_PATHS = (
#     os.path.join(BASE_DIR, "l10n"),
# )
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
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
