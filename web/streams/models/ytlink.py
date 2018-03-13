"""Youtube video link"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.youtube import (getSingleVideoResult,
                           getThumbnailData)
from streams.fields import YoutubeVideoReferenceField


class YTLink(models.Model):
    class Meta:
        ordering = ['video_id']

    video_id = YoutubeVideoReferenceField(
        _('Video ID'),
        blank=False,
        null=False,
        help_text=_('The Youtube video ID'),
    )
    title = models.TextField(
        _('Title of the video'),
        blank=True,
        null=True,
        help_text=_('Title of the video'),
    )
    thumbnail = models.ImageField(
        _('Thumbnail of the video'),
        blank=True,
        null=True,
        help_text=_('The thumbnail of the video'),
    )
    duration = models.IntegerField(
        _('Stream duration'),
        blank=True,
        null=True,
        help_text=_('Video duration (in minutes)'),
    )

    def __str__(self):
        if self.title:
            return self.title
        return self.video_id

    def update_youtube_metadata(self):
        """Update metadata from youtube.

        Returns
        -------
        bool
            True if anything was changed, False otherwise


        Notes
        -----
        Only update missing fields.
        """
        any_change = False
        if ((not self.title
                or not self.thumbnail
                or not self.duration)):
            videoDetails = getSingleVideoResult(self.video_id)
            if not self.title and videoDetails['title']:
                self.title = videoDetails['title']
                any_change = True
            if not self.thumbnail and videoDetails['thumbnail']:
                thumbnailImage = getThumbnailData(
                    videoDetails['thumbnail'])
                if thumbnailImage:
                    self.thumbnail.save('thumbnail.jpg',
                                        thumbnailImage)
                    any_change = True
            if not self.duration and videoDetails['duration']:
                self.duration = videoDetails['duration']
                any_change = True
        return any_change

    def save(self,
             *args,
             **kwargs):
        super().save(*args,
                     **kwargs)
        if self.update_youtube_metadata():
            super().save(*args,
                         **kwargs)
