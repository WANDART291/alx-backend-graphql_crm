from celery.schedules import crontab
from pathlib import Path

# -------------------------
# BASE SETTINGS
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-with-any-random-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

# -------------------------
# INSTALLED APPS (Unified and Cleaned)
# -------------------------
INSTALLED_APPS = [
    # Django Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Project Apps
    'crm',
    'graphene_django',
    
    # Task Scheduler Apps
    'django_crontab', 
    'django_celery_beat', 
]

# -------------------------
# MIDDLEWARE & URLS
# -------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crm.urls'

# -------------------------
# TEMPLATES, DATABASE, PASSWORDS (Standard Configuration)
# -------------------------
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

WSGI_APPLICATION = 'crm.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

# -------------------------
# INTERNATIONALIZATION & STATICS
# -------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------
# GRAPHQL
# -------------------------
GRAPHENE = {
    "SCHEMA": "crm.schema.schema",
}

# ---------------------------------------------
# 📅 CONSOLIDATED TASK SCHEDULING CONFIGURATION
# ---------------------------------------------

# 1. django-crontab Configuration (from Task 3)
# Note: Duplicate CRONJOBS blocks are consolidated here.
CRONJOBS = [
    ('0 */12 * * *', 'crm.cron.update_low_stock'), 
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]

# 2. ✅ CELERY CONFIGURATION (Final Working Filesystem Broker)
# Note: CELERY_RESULT_BACKEND is omitted to prevent the RuntimeError.
CELERY_BROKER_URL = 'filesystem://' 
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'data_folder_in': 'celery_queue/in',  
    'data_folder_out': 'celery_queue/out', 
    'processed_folder': 'celery_queue/processed',
}

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC' 

# 3. CELERY BEAT SCHEDULE (Required for Task 4)
CELERY_BEAT_SCHEDULE = {
    'generate-crm-report-weekly': {
        'task': 'crm.tasks.generate_crm_report',
        # Schedule: Every Monday at 6:00 AM
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}

# 4. django-cron Configuration (Deprecated/Removed, but define the classes if needed elsewhere)
# CRON_CLASSES is kept simple and should align with your codebase.
CRON_CLASSES = [
    "crm.cron.HeartbeatCronJob", 
    "crm.cron.LowStockCronJob", 
]