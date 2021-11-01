from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def phone(value):
    if len(value) == 10:
        area = value[0:3]
        pre = value[3:6]
        rest = value[6:]
        return "({}) {}-{}".format(area, pre, rest)
    return value