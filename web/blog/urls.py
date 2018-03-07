"""blog URLs"""
from django.conf.urls import url
from django.views.generic.detail import DetailView
from .models import Article
from .views import ArticleListView

urlpatterns = [
    url(r'^$',
        ArticleListView.as_view(),
        name='list'),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(model=Article),
        name='article'),
]
