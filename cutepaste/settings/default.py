import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "^8xp_q0jhh8uhg_yn824n(n&nbwqwnl-w))#n)62#*qdmyn9$!"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django_extensions",
    "compressor",
    "cutepaste.files",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "cutepaste.middleware.ExceptionMapperMiddleware",
]

ROOT_URLCONF = "cutepaste.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cutepaste.wsgi.application"

# noinspection PyUnresolvedReferences
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "../static"),
    ("jquery", os.path.join(BASE_DIR, "../node_modules/jquery/dist")),
    ("intercooler", os.path.join(BASE_DIR, "../node_modules/intercooler/src")),
    ("font-awesome/css", os.path.join(BASE_DIR, "../node_modules/font-awesome/css")),
    ("font-awesome/fonts", os.path.join(BASE_DIR, "../node_modules/font-awesome/fonts")),
    ("bootstrap", os.path.join(BASE_DIR, "../node_modules/bootstrap/dist")),
    ("theter", os.path.join(BASE_DIR, "../node_modules/tether/dist")),
    ("turbolinks", os.path.join(BASE_DIR, "../node_modules/turbolinks/dist")),
]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

STATIC_ROOT = "/tmp"

COMPRESS_PRECOMPILERS = (
    ("text/less",
     "./node_modules/.bin/lessc --source-map-map-inline {infile} {outfile}"),
    ("text/es6", "./node_modules/.bin/babel --source-maps inline {infile}"),
)

COMPRESS_ENABLED = True
COMPRESS_CSS_HASHING_METHOD = "content"
SILENCED_SYSTEM_CHECKS = ["urls.W001"]

EXCEPTION_MAPPER_ENABLED = True

CP_ROOT_DIR="/data"