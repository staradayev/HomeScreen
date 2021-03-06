"""
Django settings for atosite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c__fkjoycw6c7kv-1adunwm^46ql##&*jy+uu9pul*il&l^sko'

LIQPAY_PUBLIC = 'i85334638545'
LIQPAY_PRIVAT = 'UPqxQVi4Shax8DQF32TgXzuX61TGkH7s6QgWzG2o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['pics.care']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'care',
    'ato',
    'api',
    'registration',
    'corsheaders',
    'jfu',
    'password_reset',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    "django.core.context_processors.media",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.contrib.messages.context_processors.messages",
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.tz",
)

ROOT_URLCONF = 'atosite.urls'

WSGI_APPLICATION = 'atosite.wsgi.application'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
        'GET',
        'POST',
    )

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ato',
        'USER': 'ato',
        'PASSWORD': 'atocarepass',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

AUTHENTICATION_BACKENDS = (
    'care.userBackend.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

LOGIN_URL = '/care/login'


#Template dirs
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

#static dirs
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_files'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ua'
#
LANGUAGES = (
    ('ua', 'Ukrainian'),
    ('en', 'English'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

MULTILINGUAL_FAIL_SILENTLY = True

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DONATED_LEFT = 0.95

CURRENCIES_COURSE = 22


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/care/detail/'

#Registration fields

ACCOUNT_ACTIVATION_DAYS = 3 # days count while activation active
REGISTRATION_OPEN = True
REGISTRATION_AUTO_LOGIN = True

# for send activation
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'smtp.postmarkapp.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '0838a5fe-387b-4f07-a656-50ca5b792333'
EMAIL_HOST_PASSWORD = '0838a5fe-387b-4f07-a656-50ca5b792333'
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'pics@ato.care'

# API settings
CATEGORIES_PER_PAGE = 20
PICTURES_PER_PAGE = 20
TAGS_PER_PAGE = 20
PHOTOGRAPHERS_PER_PAGE = 7
PHOTOS_PER_PHOTOGRAPHER = 5
