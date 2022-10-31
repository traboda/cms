import os
from environs import Env
from pathlib import Path

env = Env()
env.read_env()

try:
    from psycopg2cffi import compat
    compat.register()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('SECRET_KEY', default='yki%oe0)_!jua45_n^v=kzc9)6q*)^gz!3zz#7lh4j8pkj9jbo')

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://localhost', 'http://192.168.50.79', 'http://127.0.0.1', 'https://cms.traboda.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'attendance',
    'membership'
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

ROOT_URLCONF = 'cms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'cms.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': env.str('POSTGRES_PORT', default='5432')
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", default="")

AWS_STORAGE_BUCKET_NAME = env.str("S3_STORAGE_BUCKET_NAME", default="")
AWS_S3_REGION_NAME = env.str("S3_REGION_NAME", default="ap-south-1")
AWS_S3_CUSTOM_DOMAIN_ENV = env.str("AWS_S3_CUSTOM_DOMAIN", default=None)
AWS_S3_CUSTOM_DOMAIN = (
    AWS_S3_CUSTOM_DOMAIN_ENV
    if AWS_S3_CUSTOM_DOMAIN_ENV
    else f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
)
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = True

if DEBUG:
    STATIC_URL = "static/"
    STATIC_LOCATION = 'static'
    STATIC_ROOT = 'static'
else:
    STATIC_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
    STATICFILES_STORAGE = "cms.utils.storage.StaticStorage"
    STATICFILES_DIRS = (os.path.join("static"),)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROUTER_USERNAME = env.str('ROUTER_USERNAME', default='')
ROUTER_PASSWORD = env.str('ROUTER_PASSWORD', default='')
ROUTER_IP = env.str('ROUTER_IP', default='192.168.50.1:8443')

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN', default='')
ADMIN_ID = env.str('ADMIN_ID', default='')
