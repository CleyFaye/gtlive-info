"""streams AppConfig"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    """Configuration for streams application"""
    name = 'streams'
    verbose_name = _('Manage streams schedule')
