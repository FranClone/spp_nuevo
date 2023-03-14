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

#AUTH_USER_MODEL = 'core.UserProfile'

AUTHENTICATION_BACKENDS = [
    # axes tiene que ser el primer backend
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# Settings para Django Axes
AXES_ENABLED = False  # Activa el uso de Django Axes
AXES_FAILURE_LIMIT = 3  # Número máximo de intentos fallidos permitidos
AXES_COOLOFF_TIME = 1/120  # Tiempo de espera en HORAS para permitir nuevos intentos después de un bloqueo
AXES_USE_USER_AGENT = True  # Activar el uso de user-agent para identificar solicitudes maliciosas
AXES_LOCKOUT_TEMPLATE = 'lockout.html' # Opcional, path al template que se muestra cuando se bloquea una IP

# BORRAR CUANDO ESTÉ TERMINADO
# Configuración para pruebas unitarias
AXES_BEHIND_REVERSE_PROXY = False  # Desactiva el uso de proxy inverso
AXES_DISABLE_ACCESS_LOG = True  # Desactiva el registro de accesos a "django-axes"
AXES_META_PRECEDENCE_ORDER = ['HTTP_X_FORWARDED_FOR']  # Cambia el orden de verificación de IPs para pruebas detrás de un proxy

# aplicaciones instaladas en el sitio
INSTALLED_APPS = [
    'colorfield',
    'admin_interface',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_password_validators',
    'core',
    'django_bleach',
    'axes'
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/login/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'core\media')
MEDIA_URL = '/core/media/'

# un middleware es un software con el que las distintas aplicaciones se comunican entre si
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # axes tiene que ser el último middleware agregado
    'axes.middleware.AxesMiddleware',
]
# representa la ruta de importacion a la configuracion de URL
ROOT_URLCONF = 'SPP_Django.urls'
"""Configuración de seguridad, al terminar el development
poner estos comandos en true"""
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
#segundos para avisarte de que tienes que usar HTTPS
SECURE_HSTS_SECONDS = 0

"""Este comando sirve para cuando esto sea subido a una URL, 
para que Chrome y otros navegadores lo detecten, antes de activar
esto, subir el sitio aquí https://hstspreload.org/"""
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

SECURE_HSTS_PRELOAD = False     
#Redigir a SSL
SECURE_SSL_REDIRECT = False
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
    {
        'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator',
        'OPTIONS': {
             'min_length_digit': 1,
             'min_length_alpha': 1,
             'min_length_special': 1,
             'min_length_lower': 0,
             'min_length_upper': 0,
             'special_characters': "~!@#$%^&*()_+{}\":;'[]"
         }
    },
]

# representa el codigo del lenguaje
LANGUAGE_CODE = 'es-cl'
# representa la zona horaria para la aplicacion
TIME_ZONE = 'UTC'
# debe estar en True para que haga efecto el cambio de idioma
USE_I18N = True
# zona horaria por defecto de Django
USE_TZ = True

# ruta para archivos estaticos como CSS, JavaScript e Imagenes
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core\static')]

# llave primaria a usar para modelos que no tienen un campo con 'primary_key = True'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'