"""Stream details"""
from datetime import timedelta
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from utils import get_now
from .game import Game
from .ytlink import YTLink
from streams.fields import TrustLevelField


class Stream(models.Model):
    class Meta:
        ordering = ['-scheduled_date']

    scheduled_date = models.DateTimeField(
        _('Scheduled streaming date and time'),
        blank=True,
        null=True,
        unique=True,
        help_text=_('The expected streaming date, or if changed afterward, '
                    + 'the actual streaming date.'),
    )
    source = models.TextField(
        _('Source of the stream schedule'),
        blank=True,
        help_text=_('Where did this information come from'),
    )
    source_url = models.URLField(
        _('URL for more details on the source'),
        blank=True,
        help_text=_('An URL to provide a more detailed explanation about the '
                    + 'stream schedule'),
    )
    square_art = models.ImageField(
        _('The image on the blackboard'),
        blank=True,
        null=True,
        help_text=_('The image drawn on the top-left blackboard'),
    )
    secret_art = models.ImageField(
        _('The secret code image'),
        blank=True,
        null=True,
        help_text=_('The image drawn on the top-right secret blackboard'),
    )
    secret_meaning = models.TextField(
        _('The meaning of the secret message'),
        blank=True,
        null=True,
        help_text=_('If discovered, the meaning behind the secret message'),
    )
    trust_level = TrustLevelField(
        _('Level of confidence for this schedule'),
        blank=True,
        null=True,
        help_text=_('How much can this information be trusted.'),
    )
    live_video = models.ForeignKey(
        YTLink,
        blank=True,
        null=True,
        help_text=_('Live video for this stream'),
    )
    archive_videos = models.ManyToManyField(
        YTLink,
        blank=True,
        related_name='archive',
        help_text=_('(list of) archive video from this stream'),
    )
    latepatness = models.IntegerField(
        _('How late was the stream'),
        blank=True,
        null=True,
        help_text=_('How late was the stream (in minutes)'),
    )
    games = models.ManyToManyField(
        Game,
        blank=True,
        help_text=_('(list of) game played on the stream.'),
    )

    def get_absolute_url(self):
        return reverse('streams:details', kwargs={'pk': self.pk})

    @property
    def display_title(self):
        if self.live_video and self.live_video.title:
            return self.live_video.title
        if self.archive_videos.all().exists():
            archive_title = self.archive_videos.all()[0].title
            if archive_title:
                return archive_title
        return '(no title)'

    @property
    def next_stream(self):
        try:
            return self._cached_next_stream
        except AttributeError:
            try:
                self._cached_next_stream = (
                    Stream.past_streams()
                    .filter(scheduled_date__gt=self.scheduled_date)
                    .order_by('scheduled_date'))[0]
            except IndexError:
                self._cached_next_stream = None
        return self.next_stream

    @property
    def previous_stream(self):
        try:
            return self._cached_previous_stream
        except AttributeError:
            try:
                self._cached_previous_stream = (
                    Stream.objects
                    .filter(scheduled_date__lt=self.scheduled_date)
                    .order_by('-scheduled_date'))[0]
            except IndexError:
                self._cached_previous_stream = None
        return self.previous_stream

    @classmethod
    def past_streams(cls):
        right_now = get_now()
        return cls.objects.filter(scheduled_date__lt=right_now)

    @classmethod
    def get_next_stream(cls, hoursMargin=3):
        """Return the next scheduled stream.

        Parameters
        ----------
        hoursMargin : int
            Number of hours after which a stream is still considered "next".


        Returns
        -------
        Stream
            A Stream instance, or None if no such stream is presnet in the DB.
        """
        right_now = get_now()
        hours_offset = timedelta(hours=-hoursMargin)
        right_before = right_now + hours_offset
        try:
            return (cls.objects
                    .filter(scheduled_date__gte=right_before)
                    .order_by('-scheduled_date')[0])
        except IndexError:
            return None

    @classmethod
    def get_previous_stream(cls, hoursMargin=3):
        """Return the last scheduled stream.

        Parameters
        ----------
        hoursMargin : int
            Number of hours after which a stream is still considered "next".


        Returns
        -------
        Stream
            A Stream instance, or None if no such stream is presnet in the DB.
        """
        next_stream = cls.get_next_stream(hoursMargin)
        try:
            if next_stream:
                return (cls.objects
                        .filter(scheduled_date__lt=next_stream.scheduled_date)
                        .order_by('-scheduled_date')[0])
            else:
                return (cls.objects
                        .order_by('-scheduled_date')[0])
        except IndexError:
            return None
