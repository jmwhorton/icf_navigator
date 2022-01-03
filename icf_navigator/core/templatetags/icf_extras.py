from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import format_html

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

@register.simple_tag()
def list_value(value, pd):
    if value in pd:
        return format_html('<li>{}</li>', pd[value])
    return ''

@register.simple_tag()
def percent(a, b):
    if(a and b):
        return (int(a)/int(b)) * 100
    else:
        return 0