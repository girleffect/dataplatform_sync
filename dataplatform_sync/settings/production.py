from .base import *


DEBUG = False


# ISON Credentials
# =======================
ISON_HOST = os.environ.get('ISON_HOST', None)
ISON_USER = os.environ.get('ISON_USER', None)
ISON_PASSWORD = os.environ.get('ISON_PASSWORD', None)


# Amazon Credentials
# =======================
S3_BUCKET = os.environ.get('S3_BUCKET', None)
S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY', None)
S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY', None)
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'eu-west-1')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
