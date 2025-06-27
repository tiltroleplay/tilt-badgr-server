# settings_local.py for Fly.io deployment

import os
from .settings import *

# Remove or comment out import that might fail during build
# from mainsite import TOP_DIR

DEBUG = False
DEBUG_ERRORS = DEBUG
DEBUG_STATIC = DEBUG
DEBUG_MEDIA = DEBUG

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-gb'

# Database config from environment variables with defaults as fallback
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'dbyherfdojaere'),
        'USER': os.getenv('POSTGRES_USER', 'ucjwf0gypzeyl'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'arandomstringthaticanuserforpostgresqlproduction'),
        'HOST': os.getenv('POSTGRES_HOST', 'tiltroleplay.com'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'OPTIONS': {},
    }
}

# Cache settings, use Redis URL from env if possible
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': os.getenv('MEMCACHED_LOCATION', 'memcached:11211'),
        'KEY_FUNCTION': 'mainsite.utils.filter_cache_key',
    }
}

# Email config
DEFAULT_FROM_EMAIL = 'badges@tiltroleplay.com'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Celery config, use Redis URL env var or fallback
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_ALWAYS_EAGER = False

# Application options
HTTP_ORIGIN = 'https://tiltroleplay.com'
ALLOWED_HOSTS = [os.getenv('ALLOWED_HOST', 'tilt-badgr-server.fly.dev')]
STATIC_URL = HTTP_ORIGIN + '/static/'

BADGR_APPROVED_ISSUERS_ONLY = False
GDPR_COMPLIANCE_NOTIFY_ON_FIRST_AWARD = True

# Secret keys — load from env, fallback to fixed string (set strong value in production!)
SECRET_KEY = os.getenv('SECRET_KEY', 'replace-this-with-a-secure-key')
UNSUBSCRIBE_KEY = os.getenv('UNSUBSCRIBE_KEY', SECRET_KEY)
UNSUBSCRIBE_SECRET_KEY = os.getenv('UNSUBSCRIBE_SECRET_KEY', SECRET_KEY)

# Logging (adjusted, commented out import TOP_DIR)
import os

LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': [],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'badgr_events': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'badgr_events.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'Badgr.Events': {
            'handlers': ['badgr_events'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s',
        },
        'json': {
            '()': 'mainsite.formatters.JsonFormatter',
            'format': '%(asctime)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%z',
        },
    },
}
