"""
Ajustes de Django para el proyecto.

Generado al comenzar el proyecto con: 'django-admin startproject' utilizando Django 4.1.4.

https://docs.djangoproject.com/en/4.1/topics/settings/

https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()

# crea la ruta dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# variables de ambiente (clave secreta: se genera aleatoriamente con cada proyecto)
SECRET_KEY = os.environ.get('SECRET_KEY')

# no ejecutar con Debug = True en produccion / no se debe desplegar el sitio con Debug = True
DEBUG = os.environ.get('DEBUG')

# lista de hosts/dominios del sitio
ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# aplicaciones instaladas en el sitio
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'django_bleach'
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/login/'
# un middleware es un software con el que las distintas aplicaciones se comunican entre si
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# representa la ruta de importacion a la configuracion de URL
ROOT_URLCONF = 'SPP_Django.urls'
# contiene las configuraciones para las plantillas a utilizar
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # base_dir apunta a la ruta, template especifica la carpeta 
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
# ruta de la aplicacion WSGI 
WSGI_APPLICATION = 'SPP_Django.wsgi.application'

# contiene las configuraciones para las bases de datos 
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}


# validadores para checkear la seguridad de las passwords de usuario
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

# representa el codigo del lenguaje
LANGUAGE_CODE = 'en-us'
# representa la zona horaria para la aplicacion
TIME_ZONE = 'UTC'
# debe estar en True para que haga efecto el cambio de idioma
USE_I18N = True
# zona horaria por defecto de Django
USE_TZ = True

# ruta para archivos estaticos como CSS, JavaScript e Imagenes
STATIC_URL = 'static/'

# llave primaria a usar para modelos que no tienen un campo con 'primary_key = True'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'