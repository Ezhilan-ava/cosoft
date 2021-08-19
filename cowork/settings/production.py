# for now fetch the development settings only
from .development import *

# turn off all debugging
DEBUG = True

# You will have to determine, which hostnames should be served by Django
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://kdmqaayufwbhcx:32b08cf5582c848a00d270e895127950b5ec1ee0610f1f90dfe87c818ae2329a@ec2-54-216-185-51.eu-west-1.compute.amazonaws.com'),
}

# ##### SECURITY CONFIGURATION ############################

# TODO: Make sure, that sensitive information uses https
# TODO: Evaluate the following settings, before uncommenting them
# redirects all requests to https
# SECURE_SSL_REDIRECT = True
# session cookies will only be set, if https is used
# SESSION_COOKIE_SECURE = True
# how long is a session cookie valid?
# SESSION_COOKIE_AGE = 1209600

# validates passwords (very low security, but hey...)
# AUTH_PASSWORD_VALIDATORS = [
#    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
#    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
#    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
#    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
# ]

# the email address, these error notifications to admins come from
# SERVER_EMAIL = 'root@localhost'

# how many days a password reset should work. I'd say even one day is too long
# PASSWORD_RESET_TIMEOUT_DAYS = 1
