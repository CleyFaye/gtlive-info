"""Stream details"""
from datetime import timedelta
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from utils import get_now
from utils.youtube import (getSingleVideoResult,
                           getThumbnailData)
from .game import Game
from streams.fields import (YoutubeVideoReferenceField,
                            TrustLevelField)


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
    live_title = models.TextField(
        _('Title of the stream when it ran live'),
        blank=True,
        null=True,
        help_text=_('Title of the video when it was live on the Game Theorist '
                    + 'channel.'),
    )
    live_yt_ref = YoutubeVideoReferenceField(
        _('Video reference of the live stream'),
        help_text=_('The Youtube reference code for the live stream.'),
    )
    live_thumbnail = models.ImageField(
        _('Thumbnail of the full video'),
        blank=True,
        null=True,
        help_text=_('The thumbnail used on the full stream, on the main '
                    + 'channel'),
    )
    archive_title = models.TextField(
        _('Title of the video when uploaded to the archive channel'),
        blank=True,
        null=True,
        help_text=_('Title of the video when uploaded to the GTLive channel.'),
    )
    archive_yt_ref = YoutubeVideoReferenceField(
        _('Video reference of the archive version'),
        help_text=_('The Youtube reference code for the archive video.'),
    )
    archive_thumbnail = models.ImageField(
        _('Thumbnail of the archive video'),
        blank=True,
        null=True,
        help_text=_('The thumbnail used on the archive video'),
    )
    latepatness = models.IntegerField(
        _('How late was the stream'),
        blank=True,
        null=True,
        help_text=_('How late was the stream (in minutes)'),
    )
    duration = models.IntegerField(
        _('Stream duration'),
        blank=True,
        null=True,
        help_text=_('Stream duration (in minutes)'),
    )
    games = models.ManyToManyField(
        Game,
        blank=True,
        help_text=_('(list of) game played on the stream.'),
    )

    def update_youtube_archiveref(self):
        """Update metadata from youtube.

        Returns
        -------
        bool
            True if anything was changed, False otherwise


        Notes
        -----
        See update_youtube() for details.
        This function update the "archive" part of the stream.
        """
        any_change = False
        if self.archive_yt_ref:
            if ((not self.archive_title
                 or not self.archive_thumbnail)):
                videoDetails = getSingleVideoResult(self.archive_yt_ref)
                if not self.archive_title and videoDetails['title']:
                    self.archive_title = videoDetails['title']
                    any_change = True
                if not self.archive_thumbnail and videoDetails['thumbnail']:
                    thumbnailImage = getThumbnailData(
                        videoDetails['thumbnail'])
                    if thumbnailImage:
                        self.archive_thumbnail.save('thumbnail.jpg',
                                                    thumbnailImage)
                        any_change = True
        return any_change

    def update_youtube_liveref(self):
        """Update metadata from youtube.

        Returns
        -------
        bool
            True if anything was changed, False otherwise


        Notes
        -----
        See update_youtube() for details.
        This function update the "live" part of the stream.
        """
        any_change = False
        if self.live_yt_ref:
            if ((not self.live_title
                 or not self.live_thumbnail
                 or not self.duration)):
                videoDetails = getSingleVideoResult(self.live_yt_ref)
                if not self.live_title and videoDetails['title']:
                    self.live_title = videoDetails['title']
                    any_change = True
                if not self.live_thumbnail and videoDetails['thumbnail']:
                    thumbnailImage = getThumbnailData(
                        videoDetails['thumbnail'])
                    if thumbnailImage:
                        self.live_thumbnail.save('thumbnail.jpg',
                                                 thumbnailImage)
                        any_change = True
                if not self.duration and videoDetails['duration']:
                    self.duration = videoDetails['duration']
                    any_change = True
        return any_change

    def update_youtube(self,
                       no_save=False):
        """Update metadata from youtube.

        This will populate title, thumbnails and duration is possible, and if
        they are initially empty.
        If any change happens, the object is automatically saved unless no_save
        is True.

        When an object is created, this is called on first save.
        """
        if ((self.update_youtube_liveref()
             or self.update_youtube_archiveref())):
            if not no_save:
                self.save()

    def save(self, *args, **kwargs):
        self.update_youtube(no_save=True)
        super().save(*args,
                     **kwargs)

    def get_absolute_url(self):
        return reverse('streams:details', kwargs={'pk': self.pk})

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
