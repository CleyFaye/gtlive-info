"""ArticleDetailView implementation"""
from django.views.generic.detail import DetailView
from blog.models import Article


class ArticleDetailView(DetailView):
    model = Article

    def get_queryset(self):
        return Article.published_articles(super().get_queryset())
