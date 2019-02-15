from .common import *


DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&q(#l4#*%5eikotl0(%@25lh09gm#b5&(ik7oya@-o_sn!1=%@'


# ISON Credentials
# =======================
ISON_HOST = os.environ('ISON_HOST', None)
ISON_USER = os.environ('ISON_USER', None)
ISON_PASSWORD = os.environ('ISON_PASSWORD', None)


# Amazon S3 Credentials
# =======================
S3_BUCKET = os.environ('S3_BUCKET', None)
S3_SECRET_KEY = os.environ('S3_SECRET_KEY', None)
S3_ACCESS_KEY = os.environ('S3_ACCESS_KEY', None)
