"""
Django settings for app_edcp project.

Generated by 'django-admin startproject' using Django 3.2.25.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6y#+$9x4^((t)&smclcdro&3fz55#(tb6mq+!nzfojq)ca9%cm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload', # rechargement automatique de la page web en cas de changement sur les fichiers
    'django.contrib.staticfiles',
    'compressor', # compression des fichiers statiques CSS et JS
    # 'bootstrap5',
    # 'django_feather',
    'crispy_forms',
    'crispy_bootstrap5',
    'formtools',
    'base_edcp',
    'options',
    'public',
    'dashboard',
    'connexion',
    'demande',
    'correspondant',
    'user',
    'enregistrement',
    'demande_auto',
    # 'admindocs', # génération automatique de la documentation dans l'admin Django.
    # 'django_extensions', # génération de diagrammes de classe UML
    # ,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
]

ROOT_URLCONF = 'app_edcp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Assurez-vous que 'BASE_DIR / "templates"' est inclus
        # 'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dashboard.context_processors.get_menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'app_edcp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }

# configure Database postgresql avecs d'environnement
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        # 'PORT': os.environ.get('DB_PORT', '5436'), # A retirer si exécution via Docker
        'NAME': os.environ.get('DB_NAME', 'edcp_db'),
        'USER': os.environ.get('DB_USER', 'Uroot_edcp'),
        'PASSWORD': os.environ.get('DB_PASS', 'e_dcp@2023#')
    }
}

# version alternative en cad de développement local sans docker
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'PORT': '5435',
        'NAME': 'edcp_db',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / "static",
 ]

# COMPRESS_ROOT = BASE_DIR / 'static'

# STATICFILES_FINDERS.append(compressor.finders.CompressorFinder)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder', 
)

"""
Utilisé pour la compilation des fichiers Sass en CSS
"""
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
Indique à Django d'utiliser le modèle User défini dans edcp_apirest comme modèle d'utilisateur personnalisé pour le projet.
Cela signifie que vous avez un modèle d'utilisateur personnalisé nommé User situé dans le fichier edcp_apirest.models.py
"""
AUTH_USER_MODEL = 'base_edcp.User'

"""
Modifiez les informations de la page d'administration
"""
# Personnalisation de l'administration
ADMIN_SITE_TITLE = "Plateforme e-DCP"
ADMIN_SITE_HEADER = "Plateforme e-DCP"
ADMIN_INDEX_TITLE = "Bienvenue sur le portail d'administration de l'application e-DCP"

"""Utilisé pour l'affichage des formulaires avec boostratp"""
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'

LOGIN_REDIRECT_URL = 'dashboard:index'
LOGOUT_REDIRECT_URL = 'public:index'

# Gestion des pages 403
HANDLER403 = 'dashboard.views.custom_permission_denied_view'

# configurez les paramètres du serveur SMTP
# Qwerty@12345#TAZ
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.office365.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'edcp@artci.ci')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'edcp@artci.ci')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'ZM7rfPxdS87&bWq$')


MEDIA_URL = '/uploads/' # URL utilisée pour l'accès aux fichiers. Doit être ajoutée à la liste des URLs
MEDIA_ROOT = BASE_DIR / 'uploads' # Répertoire de stockage des fichiers

""" Outils de génération de diagrammes de classe UML sous forme d'image """
GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}
