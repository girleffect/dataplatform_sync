from .base import *


DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')


# ISON Credentials
# =======================
ISON_HOST = os.environ.get('ISON_HOST', None)
ISON_USER = os.environ.get('ISON_USER', None)
ISON_PASSWORD = os.environ.get('ISON_PASSWORD', None)


# Amazon S3 Credentials
# =======================
S3_BUCKET = os.environ.get('S3_BUCKET', None)
S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY', None)
S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY', None)
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'eu-west-1')
