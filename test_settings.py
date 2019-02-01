from dataplatform_sync.settings.common import *


DEBUG = True
SECRET_KEY = 'tests'
CELERY_ALWAYS_EAGER = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}

# ISON Credentials
# =======================
ISON_HOST = 'ISON_HOST'
ISON_USER = 'ISON_USER'
ISON_PASSWORD = 'ISON_PASSWORD'


# Amazon S3 Credentials
# =======================
S3_BUCKET = 'S3_BUCKET'
S3_SECRET_KEY = 'S3_SECRET_KEY'
S3_ACCESS_KEY = 'S3_ACCESS_KEY'
