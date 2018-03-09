"""streams admin settings"""
from django.contrib import admin
from .models import (
    Stream,
    Game,
)


class GameAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'kind',
                    'completed')


class StreamAdmin(admin.ModelAdmin):
    list_display = ('scheduled_date',
                    'live_title')
    date_hierarchy = 'scheduled_date'
    fields = ('scheduled_date',
              'latepatness',
              'live_yt_ref',
              'archive_yt_ref',
              'trust_level',
              'source',
              'source_url',
              'square_art',
              'games',
              'secret_art',
              'secret_meaning',
              'live_title',
              'live_thumbnail',
              'duration',
              'archive_title',
              'archive_thumbnail')
    filter_horizontal = ('games',)
    list_filter = ('games',)


admin.site.register(Game,
                    GameAdmin)
admin.site.register(Stream,
                    StreamAdmin)
