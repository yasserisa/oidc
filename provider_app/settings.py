# -*- coding: utf-8 -*-
import os
import environ
import rollbar

# environ
env = environ.Env() # set default values and casting
SANDBOX = env.bool("SANDBOX")

# app
SITE_URL = env.str("SITE_URL")
LOGIN_URL = env.str("LOGIN_URL")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = env.str("SECRET_KEY")

# Debug
DEBUG = env.bool("DEBUG")
TEMPLATE_DEBUG = env.bool("DEBUG")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "provider_app/templates")],
        "APP_DIRS": True,
    },
]

# Cors
CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS")
CORS_ORIGIN_WHITELIST = env.tuple("CORS_ORIGIN_WHITELIST")
CSRF_TRUSTED_ORIGINS = env.list("CORS_ORIGIN_WHITELIST")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Custom libs
AUTHENTICATION_BACKENDS = ("provider_app.views.CustomBackend",)
OIDC_EXTRA_SCOPE_CLAIMS = "provider_app.utils.scopes.scope_claims.CustomScopeClaims"
ROOT_URLCONF = "provider_app.urls"
WSGI_APPLICATION = "provider_app.wsgi.application"

# django
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "corsheaders",
    "provider_app",
    "oidc_provider",
)

MIDDLEWARE = (
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware"
)

# SSL
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

# Database
DATABASES = {
    "default": {
        "NAME": env.str("NAME_DB"),
        "ENGINE": "django.db.backends.mysql",
        "USER": env.str("USER_DB"),
        "HOST": env.str("HOST_DB"),
        "PORT": env.str("PORT_DB"),
        "PASSWORD": env.str("PASSWORD_DB"),
        "OPTIONS": {
            "autocommit": True,
        },
    }
}

# Internationalization
LANGUAGE_CODE = "es-es"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("CACHE_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Cookies
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_AGE = env.int("SESSION_COOKIE_AGE")
CSRF_COOKIE_SECURE = True
CSRF_FAILURE_VIEW = "provider_app.utils.error.handle.missing_csrf"
SESSION_COOKIE_DOMAIN = env.str("SESSION_COOKIE_DOMAIN")
CSRF_COOKIE_DOMAIN = env.str("SESSION_COOKIE_DOMAIN")

# Authetincation API
URL_AUTH = env.str("URL_AUTH")
# LOGS APIS
PORT_UDP_LOGS = env.int("PORT_UDP_LOGS")
URL_GET_INFO_USER = env.str("URL_GET_INFO_USER")
TOKEN_AUTH = env.str("TOKEN_AUTH")

# Debug Rollbar
ROLLBAR = {
    "access_token": env.str("ROLLBAR_ACCESS_TOKEN"),
    "environment": "development" if DEBUG else "production",
    "root": BASE_DIR,
}
rollbar.init(**ROLLBAR)
#GeoIP2
GEOIP_PATH = os.path.join(BASE_DIR, "provider_app/geoip")

# Responses AUTH API
RESPONSES_LOGIN = \
    {
        "GENERIC": "RUN o Contraseña invalidas",
        "UNAUTHORIZED": "No esta autorizada esta aplicación"
    }
BODY_SCHEMA = \
    {
        "type" : "object", 
        "properties" : {
            "username" : {
                "type" : "string"
            }, 
            "password" : {
                "type" : "string"
            },
            "next" : {
                "type" : "string"
            },
            "nombre_app" : {
                "type" : "string"
            },
            "HTTP_USER_AGENT" : {
                "type" : "string"
            },
            "HTTP_X_FORWARDED_FOR" : {
                "type" : "string"
            }
        }, 
        "required" : [
            "username", 
            "password",
            "next",
            "nombre_app",
            "HTTP_USER_AGENT",
            "HTTP_X_FORWARDED_FOR"
        ], 
        "additionalProperties" : False
    }