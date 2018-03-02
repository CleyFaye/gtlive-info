"""Kind of activity"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ActivityTypeField(models.CharField):
    """Selection of activity kind."""
    description = _('Selection of activity kind')

    (OTHER,
     VIDEOGAME,
     NONVIDEOGAME,
     INTERACTIVESTORY,
     REACTIONVIDEO,
     TESTINGTASTING) = [str(x)
                        for x in range(6)]
    CHOICES = (
        (OTHER, _('Other')),
        (VIDEOGAME, _('Video game')),
        (NONVIDEOGAME, _('Non-video, still game')),
        (INTERACTIVESTORY, _('Interactive story')),
        (REACTIONVIDEO, _('Reaction to various things')),
        (TESTINGTASTING, _('Testing or tasting stuff')),
    )

    def __init__(self,
                 *args,
                 **kwargs):
        kwargs['max_length'] = 2
        kwargs['default'] = ActivityTypeField.OTHER
        kwargs['choices'] = ActivityTypeField.CHOICES
        super().__init__(*args,
                         **kwargs)
