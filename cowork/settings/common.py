# Python imports
from os.path import abspath, basename, dirname, join, normpath
import sys
import datetime
import os
import environ
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = environ.Path(__file__) - 2


# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

# collect static files here
STATIC_ROOT = join(PROJECT_ROOT, 'run', 'static')

# collect media files here
MEDIA_ROOT = join(PROJECT_ROOT, 'run', 'media')

# look for static assets here
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))
AUTHENTICATION_BACKENDS = \
    ['django.contrib.auth.backends.ModelBackend',
     'allauth.account.auth_backends.AuthenticationBackend']
REST_USE_JWT = True
OLD_PASSWORD_FIELD_ENABLED = True
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=300),
    'JWT_ALLOW_REFRESH': True,
}

# ##### APPLICATION CONFIGURATION #########################

# these are the apps
DEFAULT_APPS = [
    'django.contrib.contenttypes',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.google',
    'rest_auth.registration',
    'django_extensions',
    'storages',
    'apps.basic',
    'apps.user',

]
GRAPPELLI_ADMIN_TITLE = "Table Tech"
AUTH_USER_MODEL = 'user.User'
# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

# Internationalization
USE_I18N = False


# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = normpath(join(PROJECT_ROOT, 'run', 'SECRET.key'))

# these persons receive error notification
ADMINS = (
    ('your name', 'your_name@example.com'),
)
MANAGERS = ADMINS


# ##### DJANGO RUNNING CONFIGURATION ######################

# the default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# the root URL configuration
ROOT_URLCONF = '%s.urls' % SITE_NAME

# the URL for static files
STATIC_URL = '/static/'

# the URL for media files
MEDIA_URL = '/media/'


# ##### DEBUG CONFIGURATION ###############################
DEBUG = False
SITE_ID = 1


# finally grab the SECRET KEY
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Could not open %s for writing!' % SECRET_FILE)


# Auth settings
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_UNIQUE_EMAIL = False
# Make email verification mandatory to avoid junk email accounts
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/thank'

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_LOGOUT_ON_GET = True

REST_FRAMEWORK = {
    "DATE_INPUT_FORMATS": ["%d/%m/%Y"],
    'DATETIME_FORMAT': "%d/%m/%Y %H:%M",
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'TIME_FORMAT': "%I:%M %p",
}


REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'apps.user.serializers.LoginUserSerializer',
    'USER_DETAILS_SERIALIZER': 'apps.user.serializers.UserDetailsSerializer',
    'PASSWORD_RESET_SERIALIZER': 'apps.user.serializers.PasswordResetSerializer'
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'apps.user.serializers.RegistrationSerializer',
}

GRAPPELLI_ADMIN_TITLE = "Table Tech"


# AWS S3 bukket app_settings
AWS_LOCATION = 'static'
# CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME ='tt-media'
AWS_S3_CUSTOM_DOMAIN='%s.s3.ap-south-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
     'CacheControl': 'max-age=86400',
}

DEFAULT_FILE_STORAGE = 'settings.storage_backends.MediaStorage'
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder',
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder',)
AWS_DEFAULT_ACL = 'public-read'
AWS_IS_GZIPPED=True



# SMTP static
EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.ap-south-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIAZ7WAJCH3WA6EAJRT'
DEFAULT_FROM_EMAIL = "ezhilan@bondstate.com"
EMAIL_HOST_PASSWORD = 'BN1UQdJNpTM8MRRJ61szmyvNd3BjQQo7vObcnog38zf3'
