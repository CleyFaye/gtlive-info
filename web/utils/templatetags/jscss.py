from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


def _get_url(relativepath):
    filepath = static(relativepath)
    return '%s?ver=%s' % (filepath,
                          settings.STATIC_VERSION)


@register.simple_tag
@stringfilter
def js(jspath):
    return mark_safe('<script type="text/javascript" src="%s" ></script>'
                     % _get_url(jspath))


@register.simple_tag
@stringfilter
def css(csspath):
    return mark_safe('<link rel="stylesheet" href="%s" type="text/css" />'
                     % _get_url(csspath))


@register.simple_tag
@stringfilter
def img(imgpath):
    return mark_safe('%s' % _get_url(imgpath))
