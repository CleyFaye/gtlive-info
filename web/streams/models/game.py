"""Game details"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from streams.fields import ActivityTypeField


class Game(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(
        _('Name of the game/activity'),
        unique=True,
        max_length=200,
        help_text=_('The name of the game or activity performed on the stream'),
    )
    reference = models.URLField(
        _('Online reference to get more informations'),
        blank=True,
        help_text=_('Online resource to get more info (game page, etc.)'),
    )
    description = models.TextField(
        _('Brief description'),
        blank=True,
        help_text=_('A brief description of the game/activity for quick '
                    + 'reference'),
    )
    kind = ActivityTypeField(
        _('Kind of activity'),
        help_text=_('The kind of activity'),
    )
    completed = models.NullBooleanField(
        _('Game completed'),
        null=True,
        blank=True,
        help_text=_('True if the game was completed live, False if it wasn\'t. '
                    + 'None if the game isn\'t "completable"'),
    )

    def __str__(self):
        return self.name
