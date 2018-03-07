"""StreamListView implementation"""
from django.views.generic.list import ListView
from utils import get_now
from streams.models import Stream


class StreamListView(ListView):
    paginate_by = 15

    def get_queryset(self):
        now = get_now()
        return Stream.objects.filter(scheduled_date__lt=now)
