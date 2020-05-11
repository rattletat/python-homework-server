from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()
EXTENSIONS = ["fenced_code", "codehilite", "tables", "smarty", "markdown_katex"]


@register.filter()
def mdfile2html(mdfile):
    with open(mdfile, "r") as f:
        description = f.read()

    return md.markdown(description, extensions=EXTENSIONS)


@register.filter()
@stringfilter
def mdtext2html(mdtext):
    return md.markdown(mdtext, extensions=EXTENSIONS)
