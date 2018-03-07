"""Article model"""
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from utils import get_now
from .author import Author


class Article(models.Model):
    class Meta:
        ordering = ('publication_date',)

    publication_date = models.DateTimeField(
        _('Publication date'),
        blank=True,
        null=True,
        help_text=_('Date at which the article will become visible')
    )
    expiration_date = models.DateTimeField(
        _('Expiration date'),
        blank=True,
        null=True,
        help_text=_('Date at which the article will become invisible. '
                    + 'Can be left blank if the article should not expire.')
    )
    author = models.ForeignKey(
        Author,
        help_text=_('The identity under which the article is published'),
    )
    title = models.CharField(
        _('Title'),
        max_length=500,
        blank=False,
        null=False,
        help_text=_('The full title, displayed in lists and before content'),
    )
    content = models.TextField(
        _('Content'),
        blank=False,
        null=False,
        help_text=_('The article\'s content. Support markdown.'),
    )

    @classmethod
    def published_articles(cls, queryset=None):
        """Return a queryset will all published articles.

        Parameters
        ----------
        queryset : QuerySet | None
            If provided, this queryset will be filtered to include only
            published articles.
            If None, all Article will be filtered.
        """
        now = get_now()
        filter_future = Q(publication_date__lte=now)
        filter_expired = (Q(expiration_date__isnull=True)
                          | Q(expiration_date__gt=now))
        if queryset is None:
            queryset = cls.objects
        return queryset.filter(filter_future,
                               filter_expired)

    @classmethod
    def last_article(clz):
        try:
            return clz.published_articles()[0]
        except IndexError:
            return None
