from .dev import *  # noqa

# Sites
URL = 'http://localhost:8000'

# Emails
DJMAIL_REAL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Speeds up tests.
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
