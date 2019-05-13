import os
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(",")


# Application definition
INSTALLED_APPS = [
    'dataplatform_sync',

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

CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = False
BROKER_URL = os.environ.get('BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

MATILLION_INSTANCE_ID = os.environ.get('MATILLION_INSTANCE_ID')

CELERYBEAT_SCHEDULE = {
    # Executes Monday at 8 a.m.
    'pull-call-detail-to-s3': {
        'task': 'dataplatform_sync.tasks.gc_data_sync',
        'schedule': crontab(hour=8, day_of_week='1'),
        'kwargs': {
            'files': 'GC_RAW_DATA/*.csv',
            'directory': 'girlsconnect/GC_RAW_DATA'
        },
    },

    # Executes Monday at 8 a.m.
    'pull-play-story-detail-to-s3': {
        'task': 'dataplatform_sync.tasks.gc_data_sync',
        'schedule': crontab(hour=8, day_of_week='1'),
        'kwargs': {
            'files': 'GC_CallDtl/playStoryDetails{}.csv',
            'timestamped_files': True,
            'timestamped_format': '%Y%m%d',
            'directory': 'girlsconnect/GC_CallDtl'
        },
    },
    # Executes every Monday at 9 a.m.
    'start_matillion_instance': {
        'task': 'dataplatform_sync.tasks.start_matillion_instance',
        'schedule': crontab(hour=9, day_of_week='1'),
        'kwargs': {
            'instance_id': MATILLION_INSTANCE_ID,
        },
    },
    # Executes every Monday at 10 a.m.
    'stop_matillion_instance': {
        'task': 'dataplatform_sync.tasks.stop_matillion_instance',
        'schedule': crontab(hour=10, day_of_week='1'),
        'kwargs': {
            'instance_id': MATILLION_INSTANCE_ID,
        },
    },
}
