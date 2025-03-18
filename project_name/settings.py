import os
import sys
from datetime import timedelta
from pathlib import Path

from decouple import Config, RepositoryEnv, Csv

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, "apps"))

DOTENV_FILE = "env/.env"
config = Config(RepositoryEnv(DOTENV_FILE))

ENVIRONMENT = config("ENVIRONMENT", default="staging")

DEBUG = config("DEBUG", cast=bool, default=False)

if ENVIRONMENT == "dev":
    _db_config = {
        "dbName": config("POSTGRES_DB", default="tempdb3"),
        "username": config("POSTGRES_USER", default="s"),
        "password": config("POSTGRES_PASSWORD", default=""),
        "dbHost": config("POSTGRES_HOST", default=""),
        "dbPort": config("POSTGRES_PORT", default="5432"),
    }

    _other_config = {
        "secretKey": config("SECRET_KEY", default="sdfdfdfdfer4dfgdfw4"),
        "domain_name": config("DOMAIN_NAME", default="https://api.gotur.uz"),
    }

    _redis_config = {
        "host": config("REDIS_HOST", default="localhost"),
        "port": config("REDIS_PORT", cast=int, default=6379),
    }

    _jwt_config = {
        "access_token_lifetime": config("ACCESS_TOKEN_LIFETIME", default=300, cast=int),
        "refresh_token_lifetime": config("REFRESH_TOKEN_LIFETIME", default=5000, cast=int),
    }

    _swagger = {
        "swagger_base_url": config("SWAGGER_BASE_URL", default=None),
        "title": config("SWAGGER_TITLE", default=None),
    }

else:
    raise NotImplementedError(f"Unknown environment: {ENVIRONMENT}")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=Csv())
SECRET_KEY = _other_config["secretKey"]
AUTH_USER_MODEL = "users.User"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "drf_yasg",
    "rest_framework",
    "django_filters",
    "debug_toolbar",

    "users",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'project_name.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'project_name.wsgi.application'

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": _db_config["dbHost"],
        "PORT": _db_config["dbPort"],
        "USER": _db_config["username"],
        "PASSWORD": _db_config["password"],
        "NAME": _db_config["dbName"],
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get("MEDIA_PATH", "media/"))
STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get("STATIC_PATH", "static/"))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'common.paging.PageNumberPagination',
    'PAGE_SIZE': 10,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=_jwt_config['access_token_lifetime']),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=_jwt_config['refresh_token_lifetime']),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = [
    # "https://example.com"
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Type in the *\'Value\'* input box below: **\'Bearer &lt;JWT&gt;\'**, where JWT is the JSON web token you get back when logging in.',
        },
    },
    'DOC_EXPANSION': False,
}

SWAGGER_CONFIG = _swagger
