"""
Django settings for hello_world_project project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import logging
import dj_database_url
import base64
from dotenv import load_dotenv
from google.oauth2 import service_account

# Load environment variables from .env file
load_dotenv()

# Decode base64-encoded service account key (Render doesn't allow uploading JSON secrets directly)
GCP_KEY_BASE64 = os.getenv("GCP_KEY_BASE64")

if GCP_KEY_BASE64:
    # Ensure the base64 string is properly padded
    missing_padding = len(GCP_KEY_BASE64) % 4
    if missing_padding:
        GCP_KEY_BASE64 += '=' * (4 - missing_padding)

    # Decode the base64 string back to JSON
    key_json = base64.b64decode(GCP_KEY_BASE64).decode("utf-8")

    # Save the key to a temporary file
    GOOGLE_CREDENTIALS_PATH = "/tmp/gcp-storage-key.json"

    with open(GOOGLE_CREDENTIALS_PATH, "w") as f:
        f.write(key_json)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH
else:
    raise ValueError("GCP_KEY_BASE64 environment variable not set")

GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')  # The name of your GCS bucket
GS_PROJECT_ID = os.getenv('GS_PROJECT_ID')
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # Path to the JSON key file for the service account
)

#undo

# Google Cloud Storage for Static Files
#STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

#STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"
STATIC_URL = '/static/'


# Set up logging
logger = logging.getLogger(__name__)

# Configure Django to log to the console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# Default to DEBUG=False if not explicitly set in .env
DEBUG = os.getenv("DEBUG", "False") == "True"

# Read ALLOWED_HOSTS from environment variables (.env for local, Render's env for production)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Get Render’s hostname dynamically
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hello_app', # This is the app we created earlier
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hello_world_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hello_world_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Read DATABASE_URL from environment variables (set by Render)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    # Fallback to SQLite only if DATABASE_URL is not set
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


if not DEBUG:
    # Path where `collectstatic` will gather static files in production
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # Use Google Cloud Storage for static files in production
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

    # Ensure the static URL points to GCP storage
    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"
    STORAGES = {
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": GS_BUCKET_NAME,
            "project_id": GS_PROJECT_ID,
            "credentials": GS_CREDENTIALS,
        },
    },
}

# Serve static files locally when DEBUG=True
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'hello_app/static'),
        os.path.join(BASE_DIR, 'static'),
    ]


# MEDIA FILES (User uploads) - Not used yet but pre-configured
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  
# LATER: This will be replaced by Google Cloud Storage for production:
# DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Strengthen security against common web attacks when running Django in production

if not DEBUG:  # Only enforce these in production
    SECURE_BROWSER_XSS_FILTER = True  # Protect against XSS attacks
    SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-type sniffing
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"  # Redirect HTTP to HTTPS
    SESSION_COOKIE_SECURE = True  # Send session cookies only over HTTPS
    CSRF_COOKIE_SECURE = True  # Send CSRF cookies only over HTTPS
    X_FRAME_OPTIONS = "DENY"  # Prevent clickjacking attacks
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", 0))  # Enforce HSTS when set

# Log a warning if DEBUG is enabled

if DEBUG:
    logger.warning("WARNING: Debug mode is enabled! Don't use this in production.")