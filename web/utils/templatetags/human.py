"""Template to "humanize" some output"""
from math import floor
from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter
def humanDuration(duration):
    """Convert a duration (in minutes) to a text description with hours.

    Example : 10 minutes outputs "10 minutes", while 65 minutes outputs
    "1 hour 5 minutes".
    """
    minutes = int(duration)
    if minutes >= 60:
        hours = floor(minutes / 60)
        minutes -= hours * 60
    else:
        hours = 0
    resultComponents = []
    if hours == 1:
        resultComponents.append(_('1 hour'))
    elif hours > 1:
        resultComponents.append(_('%i hours') % hours)
    if minutes == 1:
        resultComponents.append(_('1 minute'))
    elif minutes > 1:
        resultComponents.append(_('%i minutes') % minutes)
    return ' '.join(resultComponents)
