"""Global project configuration.

Configuration that applies to any deployment environment (project-specific).
"""
from django.utils.translation import ugettext_lazy as _
from settings import BASE_DIR
from os.path import join
from utils import generate_random_tag

WSGI_APPLICATION = 'wsgi.application'
ROOT_URLCONF = 'conf.urls'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'US/Pacific'
USE_TZ = True

PROJECT_APPS = [
    'utils',
    'streams.StreamsConfig',
]

THIRDPARTY_APPS = [
    'markdownify',
    'tastypie',
    'maintenance_mode',
    'socialmeta.SocialMetaConfig',
]

THIRDPARTY_MIDDLEWARE = [
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
]

THIRDPARTY_AFTERCACHE_MIDDLEWARE = [
    'htmlmin.middleware.MarkRequestMiddleware',
]

HTML_MINIFY = True

MARKDOWNIFY_WHITELIST_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'strong',
    'ul',
    'p',
]

MAINTENANCE_MODE_STATE_FILE_PATH = join(BASE_DIR,
                                        'maintenance_mode_state.txt')
MAINTENANCE_MODE_IGNORE_STAFF = True
MAINTENANCE_MODE_IGNORE_URLS = [r'^/admin/']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'maintenance_mode.context_processors.maintenance_mode',
                'socialmeta.context_processors.socialmeta',
                'utils.context_processors.googleanalytics',
            ],
            },
    },
]

MEDIA_ROOT = join(BASE_DIR,
                  'uploads')
MEDIA_URL = '/u/'
STATIC_ROOT = join(BASE_DIR,
                   'collected_statics')
STATIC_URL = '/s/'
STATICFILES_DIRS = [join(BASE_DIR,
                         'webres')]

STATIC_VERSION = generate_random_tag(6)

SOCIALMETA = {
    'enabled': True,
    'title': _('GTLive Unofficial Schedule'),
    'description': _('Want to catch the next livestream from #GTLive? We\'ve '
                     + 'got some of that!'),
}
