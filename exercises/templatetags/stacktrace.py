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
    question_line = lines[error_index - 1]

    try:
        if "AssertionError" in error_line:
            mq = re.search(
                r'self\.assert.+\(submission\.([^(]+\(.+\)), ".*"\)$', question_line
            )
            me = re.search("'([^']*)' != '([^']*)'", error_line)
            return (
                f"Aufruf: {mq.group(1)}\nFalsch: {me.group(1)}\nLösung: {me.group(2)}"
            )
    except AttributeError:
        pass
    lines = "\n".join(lines[error_index - 2:])
    return f"{lines.strip()}"
