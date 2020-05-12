from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

QUESTION_REGEX = '.*self\.assert.+\(submission\.([^(]+\(.+\)), \"?[^"]+\"?\).*'
ERROR_REGEX = "AssertionError: '?([^']+)'? != '?([^']+)'?"


@register.filter()
@stringfilter
def beautify_error(error):
    lines = error.split("\n")
    error_index = [i for i, line in enumerate(lines) if "Error" in line][0]
    error_line = lines[error_index]
    question_line = lines[error_index - 1]

    try:
        if "AssertionError" in error_line:
            mq = re.search(QUESTION_REGEX, question_line)
            me = re.search(ERROR_REGEX, error_line)
            return (
                f"Aufruf: {mq.group(1)}\n"
                f"Falsch: {me.group(1)}\n"
                f"Lösung: {me.group(2)}"
            )
    except AttributeError:
        pass
    lines = "\n".join(lines[error_index - 3:])
    return f"{lines}"
