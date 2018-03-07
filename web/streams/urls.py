"""streams URLs"""
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import (NextStreamView,
                    NoStreamView,
                    StreamDetailView,
                    StreamListView)

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='streams/homepage.html'),
        name='homepage'),
    url(r'^next$',
        NextStreamView.as_view(),
        name='next'),
    url(r'^nope$',
        NoStreamView.as_view(),
        name='noschedule'),
    url(r'^list$',
        StreamListView.as_view(),
        name='list'),
    url(r'^(?P<pk>\d+)/$',
        StreamDetailView.as_view(),
        name='details'),
]
