"""
Django settings for demoservice project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

SECRET_KEY = os.environ.get('SECRET_KEY', 'no_secret')

DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'

ALLOWED_HOSTS = ['*']

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_openid_auth',
    'demoservice',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demoservice.urls'

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

WSGI_APPLICATION = 'demoservice.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', None)
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'demoservice')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'demoservice')
POSTGRES_PASS = os.environ.get('POSTGRES_PASS', 'demoservice')
if POSTGRES_HOST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': POSTGRES_DB,
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASS,
            'HOST': POSTGRES_HOST,
            'PORT': POSTGRES_PORT,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # noqa
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = (
    'django_openid_auth.auth.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/openid/login/'
LOGIN_REDIRECT_URL = '/'

OPENID_CREATE_USERS = True
OPENID_SSO_SERVER_URL = 'https://login.launchpad.net/'
OPENID_LAUNCHPAD_TEAMS_REQUIRED = ['canonical-content-people']
OPENID_USE_AS_ADMIN_LOGIN = True
OPENID_LAUNCHPAD_TEAMS_MAPPING_AUTO = True

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# RabbitMQ
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', 5672)

# Celery options
CELERY_BROKER_URL = 'amqp://guest:guest@{host}:{port}//'.format(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
)

CELERY_TASK_ALWAYS_EAGER = os.environ.get("CELERY_TASK_ALWAYS_EAGER", False)

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

DEMO_DIR = '/srv/run.demo.haus-demos/'
if DEBUG:
    DEMO_DIR = os.path.join(BASE_DIR, 'demos')

GITHUB_WEBHOOK_SECRET = os.environ.get('GITHUB_WEBHOOK_SECRET')

LAUNCHPAD_ALLOWED_TEAMS = ["canonical-webmonkeys"]
LAUNCHPAD_WEBHOOK_SECRET = os.environ.get('LAUNCHPAD_WEBHOOK_SECRET')

DOCKERFILE_REPO_TEMPLATE = (
    "https://raw.githubusercontent.com/canonical-webteam/dockerfiles/master/"
    "{}/{}/{}"
)

default_log_level = 'DEBUG' if DEBUG else 'WARNING'
log_level = os.environ.get('LOG_LEVEL', default_log_level)
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': log_level,
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'demoservice': {
            'handlers': ['console'],
            'level': log_level,
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': log_level,
            'propagate': True,
        },
    },
}

if os.environ.get('LOGSTASH_HOST'):
    LOGGING['handlers']['logstash'] = {
        'level': log_level,
        'class': 'logstash.LogstashHandler',
        'host': os.environ.get('LOGSTASH_HOST'),
        'port': int(os.environ.get('LOGSTASH_PORT', 5959)),
        'version': 1,
        'message_type': 'logstash',
        'tags': ['demoservice', 'run.demo', 'run.demo.haus'],
    }
    LOGGING['loggers']['demoservice']['handlers'] += ['logstash']
