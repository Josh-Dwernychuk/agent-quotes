################### This code is duplicated in settings/base.py ######## # noqa
import environ

BASE_DIR = environ.Path(__file__) - 3
env = environ.Env()
########################################################################

# .env file, should load only in development environment
# To enable this locally, run `export DJANGO_READ_DOT_ENV_FILE=True`
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined
    # in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(BASE_DIR.path('.env'))
    print('Loading .env File: {}'.format(env_file))
    env.read_env(env_file)

from .base import *  # noqa

LOCAL = True

INSTALLED_APPS += [ # noqa
    'debug_toolbar',
    'django_extensions',
]
MIDDLEWARE += [ # noqa
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ALLOWED_HOSTS += ['localhost'] # noqa

INTERNAL_IPS = ['127.0.0.1']

DJANGO_ADMIN_URL = r'^admin/'
