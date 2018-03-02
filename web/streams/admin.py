"""streams admin settings"""
from django.contrib import admin
from .models import (
    Stream,
    Game,
)


class StreamAdmin(admin.ModelAdmin):
    list_display = ('scheduled_date',
                    'live_title')
    date_hierarchy = 'scheduled_date'


admin.site.register(Stream, StreamAdmin)
admin.site.register(Game)
