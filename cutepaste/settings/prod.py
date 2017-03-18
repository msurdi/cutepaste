import os

from .default import *  # noqa

DEBUG = False
COMPRESS_OFFLINE = os.environ.get("COMPRESS_OFFLINE", "true") == "true"
COMPRESS_ENABLED = True
COMPRESS_CSS_HASHING_METHOD = "content"
DATABASES["default"]["NAME"] = "/data/cutepaste.db"  # noqa
STATIC_ROOT = "build/statics"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'root': {
            'handlers': ['console'],
            'level': os.getenv('CP_LOG_LEVEL', 'INFO'),
        },
    },
}
