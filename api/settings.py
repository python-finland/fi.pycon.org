import json
import os
datadir = os.path.join(os.path.dirname(__file__), '..', '..')

# -------------- NOTE: change this every year --------------
YEAR = '2016'
# ----------------------------------------------------------

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['fi.pycon.org']

ADMINS = (
    ('Hieu Nguyen', 'webmaster@python.fi'),
    ('Tuure Laurinolli', 'rahastonhoitaja@python.fi'),
    ('Jyry Suvilehto', 'puheenjohtaja@python.fi'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(datadir, 'db%s.sqlite3' % YEAR),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Helsinki'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Local settings
local_stuff = json.load(open(os.path.join(datadir, 'secrets.json')))
SECRET_KEY = local_stuff['SECRET_KEY']
EMAIL_HOST_USER = local_stuff['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = local_stuff['EMAIL_HOST_PASSWORD']

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = EMAIL_HOST_PASSWORD = local_stuff['STATIC_ROOT']


ROOT_URLCONF = 'api.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api.pyconfi2016',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.expanduser("~/fi.pycon.org.log"),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

ROOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", YEAR)
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ROOT_PATH],
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

DATE_FORMAT = 'Y-m-d'

EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
EMAIL_USE_TLS = True
SERVER_EMAIL = 'webmaster@python.fi'
DEFAULT_FROM_EMAIL = 'webmaster@python.fi'

SEATS_AVAILABLE = 164  # From optimistic budget


TICKET_PRICES = {
    'individual_eb': 55,
    'individual': 65,
    'corporate_eb': 110,
    'corporate': 135,
    'student': 20,
    'organizer': 0,
    'speaker': 0,
    'sponsor': 0
}
