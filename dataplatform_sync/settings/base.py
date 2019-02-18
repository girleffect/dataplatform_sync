import os
import datetime
from celery.schedules import crontab, schedule

import djcelery


djcelery.setup_loader()



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(",")


# Application definition
INSTALLED_APPS = [
    'dataplatform_sync',
    'djcelery',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'dataplatform_sync.urls'

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

WSGI_APPLICATION = 'dataplatform_sync.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databas

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.'
            'password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = False
BROKER_URL = os.environ.get('BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

CELERYBEAT_SCHEDULE = {
    # Executes every Week at 5:30 a.m.
    'pull-call-detail-to-s3': {
        'task': 'dataplatform_sync.tasks.gc_data_sync',
        'schedule': crontab(hour=14, minute=00, day_of_week='*'),
        'kwargs': {
            'files': 'GC_RAW_DATA/*.csv', 'dir': 'girlsconnect/GC_RAW_DATA'
        },
    },

    # Executes every Week at 5:00 a.m.
    'pull-play-story-detail-to-s3': {
        'task': 'dataplatform_sync.tasks.gc_data_sync',
        'schedule': crontab(hour=14, minute=00, day_of_week='*'),
        'kwargs': {
            'files': 'GC_CallDtl/playStoryDetails*.csv',
            'dir': 'girlsconnect/GC_CallDtl'
        },
    },
}
