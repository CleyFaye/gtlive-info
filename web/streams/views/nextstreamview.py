"""Display informations about next stream"""
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from streams.models import Stream


@method_decorator(cache_page(60), name='dispatch')
class NextStreamView(DetailView):
    """Display information about the next stream, if available"""
    template_name = 'streams/nextstream.html'

    def __init__(self):
        self.next_stream = None

    def get_next_stream(self):
        if not self.next_stream:
            self.next_stream = Stream.get_next_stream(3)
            if not self.next_stream:
                raise Http404('No stream scheduled')
        return self.next_stream

    def get_object(self):
        return self.get_next_stream()

    def get(self,
            request,
            *args,
            **kwargs):
        try:
            self.get_next_stream()
        except Http404:
            return redirect('streams:noschedule')
        return super().get(request,
                           *args,
                           **kwargs)

    def get_context_data(self,
                         *args,
                         **kwargs):
        context = super().get_context_data(*args,
                                           **kwargs)
        context['previous_stream'] = Stream.get_previous_stream(3)
        return context
