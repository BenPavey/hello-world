import os
import logging
from google.oauth2 import service_account
import dj_database_url
from storages.backends.gcloud import GoogleCloudStorage
from urllib.parse import urljoin
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

# Security and configuration settings
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hello_app',  # This is the app we created earlier
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

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Using Google Cloud Storage for static files
STATICFILES_STORAGE = 'storage_backends.gcloud.GoogleCloudStaticFileStorage'  # Custom storage backend for GCS
GS_BUCKET_NAME = 'learntoscale-static-files'  # Replace with your static bucket name

# URL for serving static files
STATIC_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)

# Define Google Cloud Storage Credentials
GOOGLE_CREDENTIALS_PATH = "/tmp/gcp-storage-key.json"  # Path to GCP credentials
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH)

# Optional: Customize where you store static files (local vs GCS)
STATIC_ROOT = None  # GCS handles static files

# Media files - Not configured for now
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", 0))

# Custom Storage for Static Files (GCS)
from storages.backends.gcloud import GoogleCloudStorage
from urllib.parse import urljoin

class GoogleCloudStaticFileStorage(GoogleCloudStorage):
    """
    Google file storage class for handling static files (e.g., CSS, JS).
    """
    bucket_name = GS_STATIC_BUCKET_NAME

    def url(self, name):
        """
        Returns the correct static URL instead of Google's default URL.
        """
        return urljoin(STATIC_URL, name)