from .base import *  # noqa

DEBUG = True
SECRET_KEY = '1234'

# Sites
URL = env('URL')

# Email
DEFAULT_FROM_EMAIL = 'john@test.com'
DJMAIL_REAL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Must be absolute URLs for use in emails.
MEDIA_ROOT = str(BASE_DIR.parent / 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = str(BASE_DIR.parent / 'static')
STATIC_URL = '/static/'
