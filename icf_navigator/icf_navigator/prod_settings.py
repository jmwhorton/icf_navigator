from icf_navigator.settings import *

ALLOWED_HOSTS = ['navigator-icf.apps.dbmi.cloud']

SECRET_KEY = os.getenv('ICF_DJANGO_SECRET_KEY', '^%(#2k$5n08-i2=t8f%w3iy3^)g(=nfjy#%)!!rqx_0q3e#*ym')

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'icf_navigator',
        'USER': os.getenv('ICF_DATABASE_USER', 'mydatabaseuser'),
        'PASSWORD': os.getenv('ICF_DATABASE_PASSWORD', 'mypassword'),
        'HOST': os.getenv('ICF_DATABASE_HOST', 'localhost'),
        'PORT': '5432',
    }
}
