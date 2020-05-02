from django.template import Library

register = Library()


@register.filter
def add_classes(widget, classes):
    widget.field.widget.attrs['class'] = classes
    return widget

@register.filter
def add_placeholder(widget, placeholder):
    widget.field.widget.attrs['placeholder'] = placeholder
    return widget
