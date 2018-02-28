"""URL settings"""
from django.conf.urls import (url,
                              include)
from django.contrib import admin
from django.http import HttpResponseRedirect

urlpatterns = ([
    url(r'^admin/',
        admin.site.urls),
    url(r'^maintenance/',
        include('maintenance_mode.urls')),
    url(r'^$',
        lambda r: HttpResponseRedirect('streams/'),
        name='homepage'),
    url(r'^streams/',
        include('streams.urls')),
])
