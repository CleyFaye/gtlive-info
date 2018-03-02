"""Youtube reference value"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class YoutubeVideoReferenceField(models.CharField):
    """Reference to a Youtube video."""
    description = _('Reference to a Youtube video using it\'s code')

    def __init__(self,
                 *args,
                 **kwargs):
        kwargs.setdefault('max_length',
                          50)
        kwargs.setdefault('null',
                          True)
        kwargs.setdefault('blank',
                          True)
        super().__init__(*args,
                         **kwargs)
