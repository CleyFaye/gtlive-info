"""Youtube reference value"""
from urllib.parse import (urlparse,
                          parse_qs)
from django.core.exceptions import ValidationError
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

    @staticmethod
    def get_video_id_from_youtube_com_link(parsedURL):
        parsedQS = parse_qs(parsedURL.query)
        if 'v' not in parsedQS or len(parsedQS['v']) != 1 or not parsedQS['v']:
            raise ValidationError('No video ID in URL')
        return parsedQS['v'][0]

    @staticmethod
    def get_video_id_from_youtu_be_link(parsedURL):
        return parsedURL.path[1:]

    def pre_save(self,
                 model_instance,
                 add):
        value = getattr(model_instance,
                        self.attname)
        parsed = urlparse(value)
        if not parsed.scheme:
            return value
        if parsed.netloc == 'www.youtube.com':
            videoID = self.get_video_id_from_youtube_com_link(parsed)
        elif parsed.netloc == 'youtu.be':
            videoID = self.get_video_id_from_youtu_be_link(parsed)
        else:
            raise ValidationError('Expected a Youtube URL or Video ID')
        setattr(model_instance,
                self.attname,
                videoID)
        return videoID
