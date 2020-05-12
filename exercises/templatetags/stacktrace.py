from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter()
@stringfilter
def beautify_error(error):
    if "AssertionError" in error:
        m = re.search("'([^']*)' != '([^']*)'", error)
        return f"Falsch: {m.group(1)}\nLösung: {m.group(2)}"
    return error
