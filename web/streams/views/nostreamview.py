"""Display previous stream info"""
from django.views.generic import TemplateView
from blog.models import Article
from streams.models import Stream


class NoStreamView(TemplateView):
    """Display the previous stream info"""
    template_name = 'streams/noschedule.html'

    def get_context_data(self,
                         *args,
                         **kwargs):
        context = super().get_context_data(*args,
                                           **kwargs)
        context['previous_stream'] = Stream.get_previous_stream(3)
        context['last_article'] = Article.last_article()
        return context
