"""Google Analytics key injector for context"""
from django.conf import settings


def googleanalytics(request):
    return {'ANALYTICS_KEY': settings.ANALYTICS_KEY}
