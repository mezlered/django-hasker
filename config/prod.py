from config.base import *


SECRET_KEY = 'r)&z7b=ym3!uu^s9i-v)c)pasery#o6&wvsi_d-*0ruu)vrcor'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['pyt']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}