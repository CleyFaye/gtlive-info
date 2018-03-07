"""Author model"""
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    class Meta:
        ordering = ('name',)

    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        help_text=_('List of users that can use this identity to publish '
                    + 'articles'),
    )
    name = models.CharField(
        _('Author name'),
        max_length=200,
        unique=True,
        help_text=_('Visible author name'),
    )
    twitter = models.CharField(
        _('Twitter handle'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('Twitter handle for this author identity'),
    )

    def __str__(self):
        return self.name
