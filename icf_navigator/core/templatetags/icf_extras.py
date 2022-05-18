from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

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
        if value != False:
            return format_html('<li>{}</li>', pd[value])
    return ''

@register.simple_tag()
def text_value(value, pd):
    if value in pd:
        return format_html('<p>{}</p>', pd[value])
    return ''

@register.simple_tag()
def list_values(value, pd):
    if value not in pd:
        return ''
    values = []
    for x in pd[value]:
        if x:
            values.append([x])
    return format_html_join('\n', '<li>{}</li>', values)

@register.simple_tag()
def list_text(value, pd):
    if value in pd:
        return (', '.join(pd[value]))

@register.simple_tag()
def percent(a, b):
    if(a and b):
        return (int(a)/int(b)) * 100
    if(b == 0):
        return 100
    else:
        return 0

@register.simple_tag()
def in_list(value, key, pd):
    if key in pd:
        return value in pd[key]
    else:
        return False

@register.simple_tag()
def explain_text(value, pd, et):
    if pd.get(value) == True:
        return mark_safe(et.get(value))
    elif pd.get(value):
        return mark_safe(pd[value])
    else:
        return ''

@register.simple_tag()
def explain_text_li(value, pd, et):
    if pd.get(value) == True:
        return format_html('<li>{}</li>', et.get(value))
    elif pd.get(value):
        return format_html('<li>{}</li>', pd.get(value))
    else:
        return ''

@register.simple_tag()
def is_true(key, pd):
    return pd.get(key) == True