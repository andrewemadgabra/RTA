"""
Django settings for RTA project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import json
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jnk&d@v_*i$5&hj!m1fsdq@4$&gbi3_x870%1#ga4-5rx%a(o!'

JSON_CONFIGERATIONS_FILE = open(os.path.join(BASE_DIR, "Configuration.json"))
JSON_CONFIGRATION = json.load(JSON_CONFIGERATIONS_FILE)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = JSON_CONFIGRATION["DEBUG"]


ALLOWED_HOSTS = JSON_CONFIGRATION["ALLOWED_HOSTS"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    # 'rest_framework',
    'django_rest_passwordreset',
    'knox',
    'User',
    'Jobs',
    'EmploymentStatus',
    'Actors',
    'Periority',
    'Letter',
    'Topics',
    'Projects',
    'Financial',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'RTA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'RTA.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': JSON_CONFIGRATION['DATABASE_NAME'],
        'HOST': JSON_CONFIGRATION['DATABASE_HOST'],
        'USER': JSON_CONFIGRATION['DATABASE_USER'],
        'PASSWORD': JSON_CONFIGRATION['DATABASE_PASSWORD'],
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'unicode_results': True,
        },

    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'db.sqlite3',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'User.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('username', 'email', 'first_name', 'last_name', 'middle_name', 'number_of_identification'),
            'max_similarity': 0.5
        }
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


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}


REST_KNOX = {'TOKEN_TTL': timedelta(hours=24),
             'TOKEN_LIMIT_PER_USER':  1,
             }

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'
DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'

USE_I18N = False

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/'+JSON_CONFIGRATION['STATIC_DIR']+'/'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = JSON_CONFIGRATION['EMAIL_HOST']
EMAIL_PORT = JSON_CONFIGRATION['EMAIL_PORT']
EMAIL_HOST_USER = JSON_CONFIGRATION["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = JSON_CONFIGRATION["EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = JSON_CONFIGRATION["EMAIL_USE_TLS"]
EMAIL_USE_SSL = JSON_CONFIGRATION["EMAIL_USE_SSL"]


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
