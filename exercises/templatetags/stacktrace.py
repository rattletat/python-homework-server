from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

ASSERTION_QUESTION_REGEX = (
    '^self\.assert[a-zA-Z]+\(submission\.([^(]+\(.*\)), "?[^"]+"?\)$'
)
ASSERTION_ERROR_REGEX = "AssertionError: '?([^']+)'? != '?([^']+)'?"
ATTRIBUTE_ERROR_REGEX = "AttributeError: .+ '(.+)' has no attribute '(.+)'"


@register.filter()
@stringfilter
def beautify_error(error):
    lines = error.split("\n")
    unwanted_terms = [
        "Traceback",
        "runner.py",
        "import tests",
        "/app/tests.py",
        "import submission",
    ]
    unknown_error_output = "\n".join(
        line
        for line in lines
        if all(term not in line for term in unwanted_terms)
    )

    # Beautify unknown case
    try:
        error_index = [i for i, line in enumerate(lines) if "Error" in line][0]
        error_line = lines[error_index]
        question_line = lines[error_index - 1]
    except IndexError:
        return unknown_error_output

    if "AssertionError" in error_line:
        try:
            mq = re.search(ASSERTION_QUESTION_REGEX, question_line.strip())
            me = re.search(ASSERTION_ERROR_REGEX, error_line.strip())
            return (
                f"Aufruf: {mq.group(1)}\n"
                f"Falsch: {me.group(1)}\n"
                f"Lösung: {me.group(2)}"
            )
        except AttributeError:
            pass
    if "AttributeError" in error_line:
        try:
            me = re.search(ATTRIBUTE_ERROR_REGEX, error_line.strip())
            if me.group(1) == "submission":
                return f"Du hast die Funktion {me.group(2)} nicht definert!"
        except AttributeError:
            pass
    return unknown_error_output
