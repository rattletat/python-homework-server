from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter()
@stringfilter
def beautify_error(error):
    lines = error.split("\n")
    error_index = [i for i, line in enumerate(lines) if "Error" in line][0]
    error_line = lines[error_index]

    try:
        if "AssertionError" in error_line:
            m = re.search("'([^']*)' != '([^']*)'", error)
            return f"Falsch: {m.group(1)}\nLösung: {m.group(2)}"
    except AttributeError:
        pass
    return error_line
