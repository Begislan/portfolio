import os
from pathlib import Path

import os
import logging

# GLib эскертүүлөрүн системалык деңгээлде өчүрүү
os.environ['G_MESSAGES_DEBUG'] = 'none'
# WeasyPrint'тин логиндерин чектөө
logging.getLogger('weasyprint').setLevel(logging.ERROR)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y$bl)nl%(z@$f%en!mjx_l#r)=6xp5p51cufy=dy^gt1a(cw12'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['begiportfolio.pythonanywhere.com', "*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'ckeditor',
    'ckeditor_uploader',  # Для поддержки загрузки файлов

    'phonenumber_field',
    'core',
    'adminka',
    'django.contrib.sitemaps',
    
    # Optional: re-enable if installed, otherwise manual form styling
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Путь для статических файлов
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
AUTH_USER_MODEL = 'core.CustomUser'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

CKEDITOR_UPLOAD_PATH = "uploads/"
# CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = False

# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'full',
#         'height': 300,
#         'width': 700,
#         'simpleUpload': {
#             'uploadUrl': '/upload/',  # URL для загрузки изображений и файлов
#             'headers': {
#                 'X-CSRF-TOKEN': 'your-csrf-token',  # добавьте если требуется CSRF токен
#                 # другие заголовки если нужны
#             }
#         },
#         'extraPlugins': ','.join(['image', 'uploadimage']),  # Подключаем загрузку изображений
#         'filebrowserUploadUrl': '/ckeditor/upload/',  # URL для загрузки файлов
#         'filebrowserUploadMethod': 'form',
#     },

# }
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'extraPlugins': 'uploadimage,uploadwidget',
        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserBrowseUrl': '/ckeditor/browse/',
    }
}



LOGIN_REDIRECT_URL = 'core'


import logging

# Бардык керексиз эскертүүлөрдү өчүрүү
logging.getLogger('weasyprint').setLevel(logging.ERROR)
logging.getLogger('fontTools').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)

# Жалпы Python деңгээлинде фильтрлөө
import warnings
warnings.filterwarnings("ignore", category=UserWarning)