import os

from .default import *  # noqa

DEBUG = False
COMPRESS_OFFLINE = os.environ.get("COMPRESS_OFFLINE", "true") == "true"
DATABASES["default"]["NAME"] = "/data/cutepaste.db"  # noqa
STATIC_ROOT = "build/statics"
