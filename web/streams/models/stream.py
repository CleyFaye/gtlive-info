"""Stream details"""
from datetime import (
    datetime,
    timezone,
    timedelta,
)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.youtube import (getSingleVideoResult,
                           getThumbnailData)
from .game import Game
from streams.fields import (YoutubeVideoReferenceField,
                            TrustLevelField)


class Stream(models.Model):
    scheduled_date = models.DateTimeField(
        _('Scheduled streaming date and time'),
        blank=True,
        null=True,
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

    def save(self, *args, **kwargs):
        if self.live_yt_ref:
            if ((not self.live_title
                 or not self.live_thumbnail
                 or not self.duration)):
                videoDetails = getSingleVideoResult(self.live_yt_ref)
                if not self.live_title:
                    self.live_title = videoDetails['title']
                if not self.live_thumbnail:
                    thumbnailImage = getThumbnailData(
                        videoDetails['thumbnail'])
                    if thumbnailImage:
                        self.live_thumbnail.save('thumbnail.jpg',
                                                 thumbnailImage)
                if not self.duration:
                    self.duration = videoDetails['duration']
        if self.archive_yt_ref:
            if ((not self.archive_title
                 or not self.archive_thumbnail)):
                videoDetails = getSingleVideoResult(self.archive_yt_ref)
                if not self.archive_title:
                    self.archive_title = videoDetails['title']
                if not self.archive_thumbnail:
                    thumbnailImage = getThumbnailData(
                        videoDetails['thumbnail'])
                    if thumbnailImage:
                        self.archive_thumbnail.save('thumbnail.jpg',
                                                    thumbnailImage)
        super().save(*args,
                     **kwargs)

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
        right_now = datetime.utcnow().replace(tzinfo=timezone.utc)
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
            return (cls.objects
                    .filter(scheduled_date__lt=next_stream.scheduled_date)
                    .order_by('-scheduled_date')[0])
        except IndexError:
            return None
