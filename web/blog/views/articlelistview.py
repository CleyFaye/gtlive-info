"""ArticleListView implementation"""
from django.views.generic.list import ListView
from blog.models import Article


class ArticleListView(ListView):
    paginate_by = 5

    def get_queryset(self):
        return Article.published_articles()
