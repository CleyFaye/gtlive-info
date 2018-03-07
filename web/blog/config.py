"""blog AppConfig"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    """Configuration for blog application"""
    name = 'blog'
    verbose_name = _('Site blogging')
