"""Configuration settings specific to Astrid"""
from settings import BASE_DIR
from os.path import join
from .keys import *

DEBUG = True

ALLOWED_HOSTS = ['gtlive.info']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gtlive',
        'USER': 'gtlive',
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_ft_cache.FaultTolerantPyLibMCCache',
        'LOCATION': ['/var/run/memcached/sock'],
        'TIMEOUT': 10,
    }
}
PYLIBMC_MIN_COMPRESS_LEN = 128

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_django': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': join(BASE_DIR,
                             'logs',
                             'django.log'),
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(BASE_DIR,
                             'logs',
                             'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_django'],
            'level': 'WARNING',
            'propagate': True,
        },
        '': {
            'level': 'DEBUG',
            'handlers': ['file_debug'],
        },
    }
}
