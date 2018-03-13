"""streams admin settings"""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from .models import (
    Stream,
    Game,
    YTLink,
)


class StreamAdmin(admin.TabularInline):
    model = Stream.games.through
    fields = ['date',
              'title',
              'link']
    readonly_fields = ['date',
                       'title',
                       'link']
    can_delete = False
    max_num = 0

    def date(self, instance):
        return instance.stream.scheduled_date
    date.short_description = _('Date')

    def title(self, instance):
        return instance.stream.live_title
    title.short_description = _('Live title')

    def link(self, instance):
        return format_html(('<a href="%s">Admin</a>&nbsp;-'
                            + '&nbsp;<a href="%s">Site</a>')
                           % (reverse('admin:streams_stream_change',
                                      args=(instance.stream.pk,)),
                              instance.stream.get_absolute_url()))
    link.short_description = _('Stream page')


class GameAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'kind',
                    'completed')
    inlines = [StreamAdmin]


class StreamAdmin(admin.ModelAdmin):
    list_display = ('scheduled_date',
                    'title')
    date_hierarchy = 'scheduled_date'
    fields = ('scheduled_date',
              'latepatness',
              'live_video',
              'archive_videos',
              'trust_level',
              'source',
              'source_url',
              'square_art',
              'games')
    filter_horizontal = ('games',
                         'archive_videos')
    list_filter = ('games',)
    radio_fields = {'trust_level': admin.VERTICAL}
    save_on_top = True
    search_fields = ('source',
                     'live_video__title',
                     'archive_videos__title')

    def title(self, instance):
        if instance.live_video:
            return instance.live_video.title
        if instance.archive_videos.exists():
            return instance.archive_videos.all()[0].title
        return '?'


class YTLinkAdmin(admin.ModelAdmin):
    list_display = ('video_id',
                    'title')


admin.site.register(Game,
                    GameAdmin)
admin.site.register(Stream,
                    StreamAdmin)
admin.site.register(YTLink,
                    YTLinkAdmin)
