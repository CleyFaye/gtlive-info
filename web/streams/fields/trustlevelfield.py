"""Indicate the trust level of a schedule"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TrustLevelField(models.CharField):
    """Provides a trust level for a schedule."""
    description = _('Provides a trust level for a schedule')

    (PEEPACHU,
     SKIP,
     DRAMALAMA,
     PURPLEGUY) = [str(x)
                   for x in range(4)]
    CHOICES = (
        (PEEPACHU, _('The most reliable of all gave us this information, it '
                     + 'can be trusted (probably)')),
        (SKIP, _('We\'ve got some serious hints, so it\'s probably alright')),
        (DRAMALAMA, _('Hmm. At this point, it\'s 50/50 wishful thinking and '
                      + 'unreliable source, place your bets…')),
        (PURPLEGUY, _('Let\'s be honest, this is more like a placeholder and '
                      + 'less like a reliable information at this point.')),
    )

    def __init__(self,
                 *args,
                 **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = TrustLevelField.CHOICES
        super().__init__(*args,
                         **kwargs)
