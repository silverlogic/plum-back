'''
https://docs.djangoproject.com/en/1.9/ref/settings/
'''
import pathlib

from django.utils.translation import ugettext_lazy as _

import dj_database_url

from .env import env

BASE_DIR = pathlib.Path(__file__).parent.parent
SETTINGS_DIR = BASE_DIR / 'settings'
APPS_DIR = BASE_DIR / 'apps'

ALLOWED_HOSTS = ['*']  # Host checking done by web server.
ROOT_URLCONF = 'apps.urls'
WSGI_APPLICATION = 'apps.wsgi.application'

AUTH_USER_MODEL = 'users.User'
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_USER_FIELDS = ['email']
SOCIAL_AUTH_PROFILE_EXTRA_PARAMS = {'fields': 'email'}
SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile', 'email']
SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, email, first_name, last_name'
}
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'apps.users.pipeline.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

# Mail
EMAIL_BACKEND = 'djmail.backends.default.EmailBackend'
DJMAIL_MAX_RETRY_NUMBER = 3

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework.authtoken',
    'djmail',
    'corsheaders',
    'avatar',
    'easy_thumbnails',
    'django_jinja',
    'crispy_forms',
    'social.apps.django_app.default',

    # Apps
    'apps.api',
    'apps.base',
    'apps.users',
    'apps.family',
    'apps.cards',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        'DIRS': [str(APPS_DIR / 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".j2",
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR / 'templates')],
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


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# https://github.com/kennethreitz/dj-database-url#url-schema
DATABASES = {}
DATABASES['default'] = dj_database_url.parse(env('DATABASE_URL'))


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ('en', _('English')),
]

# For reverse proxying
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'formatters': {
        'simple': {
            'format': '[%(name)s] [%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
    }
}

# Allow requests from any domain.
CORS_ORIGIN_ALLOW_ALL = True

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'ORDERING_PARAM': 'order_by',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# Avatars
AVATAR_GRAVATAR_DEFAULT = 'retro'
AVATAR_STORAGE_DIR = 'user-avatars'
AVATAR_MAX_AVATARS_PER_USER = 1
