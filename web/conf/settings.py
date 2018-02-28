from settings import *
from conf.project_settings import *
from logging import getLogger
logg = getLogger(__name__)
try:
    from conf.local_settings import *
except ImportError:
    logg.warn('No local settings found; this might be an issue')

try:
    THIRDPARTY_APPS
except NameError:
    THIRDPARTY_APPS = []
try:
    PROJECT_APPS
except NameError:
    PROJECT_APPS = []

INSTALLED_APPS = (INSTALLED_APPS
                  + THIRDPARTY_APPS
                  + PROJECT_APPS)

try:
    THIRDPARTY_MIDDLEWARE
except NameError:
    THIRDPARTY_MIDDLEWARE = []
try:
    PROJECT_MIDDLEWARE
except NameError:
    PROJECT_MIDDLEWARE = []
try:
    THIRDPARTY_AFTERCACHE_MIDDLEWARE
except NameError:
    THIRDPARTY_AFTERCACHE_MIDDLEWARE = []

MIDDLEWARE = (['django.middleware.cache.UpdateCacheMiddleware']
              + MIDDLEWARE
              + THIRDPARTY_MIDDLEWARE
              + PROJECT_MIDDLEWARE
              + ['django.middleware.cache.FetchFromCacheMiddleware']
              + THIRDPARTY_AFTERCACHE_MIDDLEWARE)
