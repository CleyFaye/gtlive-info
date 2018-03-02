"""Display stream details"""
from django.views.generic.detail import DetailView
from streams.models import Stream


class StreamDetailView(DetailView):
    """Display a stream info"""
    model = Stream
