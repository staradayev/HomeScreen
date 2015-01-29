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
SECRET_KEY = 'r__fkkaycw6c7kv-1adunwm^46ql##&*jy+uu9pul*il&l^azn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

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
CORS_PREFLIGHT_MAX_AGE = 1000
CORS_ALLOW_METHODS = (
        'GET',
        'POST',
    )

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'atobase',
        'USER': 'atouser',
        'PASSWORD': 'care2014',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

LOGIN_URL = '/care/login'


#Template dirs
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

STATIC_ROOT = '/Users/staradayev/Documents/Projects/django-learn/atosite/static_root/'

#static dirs
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = '/Users/staradayev/Documents/Projects/django-learn/atosite/media/'

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

DONATED_LEFT = 0.6


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
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'info@ato.care'

# API settings
CATEGORIES_PER_PAGE = 20
PICTURES_PER_PAGE = 20
TAGS_PER_PAGE = 20
