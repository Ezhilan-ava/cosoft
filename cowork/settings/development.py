# Python imports
from os.path import join

# project imports
from .common import *
import environ
import os
# uncomment the following line to include i18n
# from .i18n import *


# ##### DEBUG CONFIGURATION ###############################
DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = environ.Path(__file__) - 2
env = environ.Env()
env_file = ROOT_DIR('.env')
env.read_env(env_file=env_file)

# allow all hosts during development
ALLOWED_HOSTS = ['*']

# adjust the minimal login
LOGIN_URL = 'core_login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'core_login'


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default':env.db('DATABASE_URL', default= "postgres://kdmqaayufwbhcx:32b08cf5582c848a00d270e895127950b5ec1ee0610f1f90dfe87c818ae2329a@ec2-54-216-185-51.eu-west-1.compute.amazonaws.com:5432/d2fffudlk6u19g")
}

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS
