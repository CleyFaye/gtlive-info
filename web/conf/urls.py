"""URL settings"""
from django.conf.urls import (url,
                              include)
from django.contrib import admin
from streams.views import NextStreamView

urlpatterns = ([
    url(r'^admin/',
        admin.site.urls),
    url(r'^maintenance/',
        include('maintenance_mode.urls')),
    url(r'^$',
        NextStreamView.as_view(),
        name='homepage'),
    url(r'^streams/',
        include('streams.urls',
                namespace='streams'),
        )
])
