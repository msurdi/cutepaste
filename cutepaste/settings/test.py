import tempfile

from os import path

from .default import *  # noqa: F403, F401

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CP_ROOT_DIR = path.join(tempfile.gettempdir(), "cutepaste-tests")
