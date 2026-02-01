"""
Django settings for finory_ia project.
"""

from pathlib import Path
from datetime import timedelta
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'corsheaders',
    'django_extensions',
    
    # Local apps
    'core',
    'ai_engine',
    'accounting',
    'sales',
    'purchases',
    'inventory',
    'payments',
    'banking',
    'crm',
    'hr',
    'documents',
    'tasks',
    'identity',
    'legal',
    'analytics',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.TenantMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'finory_ia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'finory_ia.wsgi.application'

# Database
# Store SQLite in LOCALAPPDATA to avoid disk I/O errors from cloud sync (OneDrive etc.)
# and paths with spaces. On non-Windows, uses project dir.
_sqlite_dir = os.environ.get('LOCALAPPDATA', str(BASE_DIR))
_db_path = os.path.join(_sqlite_dir, 'FinoryAI', 'db.sqlite3')
if _sqlite_dir != str(BASE_DIR):
    os.makedirs(os.path.dirname(_db_path), exist_ok=True)
else:
    _db_path = str(BASE_DIR / 'db.sqlite3')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _db_path,
        'OPTIONS': {
            'timeout': 20,
        }
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
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
_static_dir = BASE_DIR / 'static'
STATICFILES_DIRS = [str(_static_dir)] if _static_dir.exists() else []

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'core.User'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# drf-spectacular settings for OpenAPI schema and Swagger UI
SPECTACULAR_SETTINGS = {
    'TITLE': 'Finory IA API',
    'DESCRIPTION': 'OpenAPI schema for Finory IA',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://localhost:8000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)
CORS_ALLOW_CREDENTIALS = True

# Cache Configuration with Redis
# Redis connection URL format: redis://[:password]@host:port/db
# Example: redis://:password@localhost:6379/1
# For Redis with password: redis://:mypassword@127.0.0.1:6379/1
# For Redis without password: redis://127.0.0.1:6379/1

REDIS_URL = config('REDIS_URL', default='redis://127.0.0.1:6379/1')
REDIS_CACHE_URL = config('CACHE_URL', default=REDIS_URL)

# Try to configure Redis cache, fallback to database cache if Redis unavailable
try:
    import redis
    
    # Test Redis connection
    _redis_test = redis.from_url(REDIS_CACHE_URL, socket_connect_timeout=2)
    _redis_test.ping()
    _redis_test.close()
    
    # Configure Redis cache with Django's built-in backend
    # Django 4.0+ has built-in Redis support
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_CACHE_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django.core.cache.backends.redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'finory_cache',
            'TIMEOUT': 300,  # Default timeout in seconds (5 minutes)
        },
        'session': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': config('SESSION_CACHE_URL', default=REDIS_URL.replace('/1', '/2')),
            'OPTIONS': {
                'CLIENT_CLASS': 'django.core.cache.backends.redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'finory_session',
        },
        'dummy': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
    }
except Exception as e:
    # Fallback to database cache if Redis is not available
    # This handles both ImportError (redis not installed) and ConnectionError (Redis not running)
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f'Redis not available, using database cache: {e}')
    
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache_table',
        },
        'session': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'session_cache_table',
        },
        'dummy': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
    }

# Session Configuration
# Options:
# - 'django.contrib.sessions.backends.cache' - Use Redis cache (recommended for production)
# - 'django.contrib.sessions.backends.cached_db' - Use cache with DB fallback (best of both)
# - 'django.contrib.sessions.backends.db' - Use database only (fallback if Redis unavailable)

# Determine session engine based on Redis availability
# If Redis is not available, use database sessions to avoid cache table dependency issues
_use_redis_sessions = False
try:
    import redis
    _redis_test = redis.from_url(REDIS_CACHE_URL, socket_connect_timeout=1)
    _redis_test.ping()
    _redis_test.close()
    _use_redis_sessions = True
except Exception:
    pass

if _use_redis_sessions:
    SESSION_ENGINE = config(
        'SESSION_ENGINE',
        default='django.contrib.sessions.backends.cached_db'  # Cache with DB fallback
    )
    if 'cache' in SESSION_ENGINE:
        SESSION_CACHE_ALIAS = config('SESSION_CACHE_ALIAS', default='session')
    else:
        SESSION_CACHE_ALIAS = None
else:
    # Fallback to database sessions when Redis is not available
    SESSION_ENGINE = config(
        'SESSION_ENGINE',
        default='django.contrib.sessions.backends.db'
    )
    SESSION_CACHE_ALIAS = None

# Session security settings
SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE', default=86400, cast=int)  # 24 hours
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)  # True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = config('SESSION_COOKIE_SAMESITE', default='Lax')  # Lax, Strict, or None
SESSION_SAVE_EVERY_REQUEST = config('SESSION_SAVE_EVERY_REQUEST', default=False, cast=bool)  # Save on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = config('SESSION_EXPIRE_AT_BROWSER_CLOSE', default=False, cast=bool)

# Celery Configuration (for async AI tasks)
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

# Encryption Settings
ENCRYPTION_KEY = config('ENCRYPTION_KEY', default='dev-encryption-key-change-in-production')

# AI Settings
AI_ENABLED = config('AI_ENABLED', default=True, cast=bool)
AI_AUTONOMOUS_MODE_DEFAULT = config('AI_AUTONOMOUS_MODE_DEFAULT', default=False, cast=bool)

# Logging (ensure logs dir exists so file handler works)
_logs_dir = BASE_DIR / 'logs'
os.makedirs(_logs_dir, exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'json': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': str(_logs_dir / 'finory_ia.log'),
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'finory_ia': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}