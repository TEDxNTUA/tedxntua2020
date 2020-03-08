'''Sets default configuration parameters and imports from environment'''
import dj_database_url
from django.utils.translation import ugettext_lazy as _


from .env import env_bool, env_list, env_setting, abs_path, env_str


DEBUG = env_bool('DEBUG', False)
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', ['*'] if DEBUG else [])
SECRET_KEY = env_str('SECRET_KEY', 'secret' if DEBUG else '')

FILE_UPLOAD_PERMISSIONS = env_str('FILE_UPLOAD_PERMISSIONS')
if FILE_UPLOAD_PERMISSIONS is not None:
    # Convert string to octal
    # https://docs.djangoproject.com/en/2.2/ref/settings/#file-upload-permissions
    FILE_UPLOAD_PERMISSIONS = int(FILE_UPLOAD_PERMISSIONS, 8)

# Application definition

INSTALLED_APPS = [
    'project.home',
    'project.partners',
    'project.program',
    'project.team',
    'project.about',
    'project.users',
    'versatileimagefield',
    'parler',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpack_loader',
    'django_extensions',
    'active_link',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # The directories where `{% extends "base.html" %}` directives
        # will search in.
        'DIRS': [abs_path('project', 'templates'), 'project/home/templates/home/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.utils.contextprocessors.settings',
            ],
            'libraries': {
                'iter_extras': 'project.templatetags.iter_extras',
                'lang_extras': 'project.templatetags.lang_extras',
            },
        },
    },
]

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
DATABASES = {'default': dj_database_url.config()}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# Assets

STATIC_URL = env_str('STATIC_URL', '/static/')
STATIC_ROOT = env_str('STATIC_ROOT', abs_path('static'))

MEDIA_URL = env_str('MEDIA_URL', '/media/')
MEDIA_ROOT = env_str('MEDIA_ROOT', abs_path('media'))

STATICFILES_DIRS = (
    abs_path('project/static'),
)

# Webpack Loader configuration is set
# on the environment-specific settings
# dev.py and prod.py


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': env_setting('LOG_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'verbose': {
            'format': '%(levelname)-8s %(asctime)s %(name)s.%(funcName)s:%(lineno)s - %(message)s'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': env_setting('LOG_LEVEL', 'INFO'),
            'propagate': True
        }
    }
}

VERSATILEIMAGEFIELD_SETTINGS = {
    # Documentation link: https://django-versatileimagefield.readthedocs.io/en/latest/installation.html#versatileimagefield-settings
    'cache_length': 2592000,
    'cache_name': 'versatileimagefield_cache',
    'jpeg_resize_quality': 70,
    'sized_directory_name': '__sized__',
    'filtered_directory_name': '__filtered__',
    'placeholder_directory_name': '__placeholder__',
    'create_images_on_demand': False,
    'image_key_post_processor': None,
    'progressive_jpeg': False
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    # Documentation link: https://django-versatileimagefield.readthedocs.io/en/latest/installation.html#versatileimagefield-rendition-key-sets
    'Sizes': [
        ('small', 'thumbnail__320x320'),
        ('medium', 'thumbnail__720x720'),
        ('large', 'thumbnail__1024x1024')
    ]
}

LOCALE_PATHS = (
    abs_path('locale'),
)

LANGUAGES = [
    ('el', _('Greek')),
    ('en', _('English')),
]

PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'el'},
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}
PARLER_DEFAULT_LANGUAGE_CODE = 'en'

TEDXNTUA_DATE = '2020-03-28'
TEDXNTUA_SHOW_UNPUBLISHED = env_bool('TEDXNTUA_SHOW_UNPUBLISHED', False)
TEDXNTUA_TICKETS_ENABLED = env_bool('TEDXNTUA_TICKETS_ENABLED', False)
TEDXNTUA_TICKETS_URL = env_str('TEDXNTUA_TICKETS_URL', '/')
TEDXNTUA_SCHEDULE_ENABLED = env_bool('TEDXNTUA_SCHEDULE_ENABLED', False)
