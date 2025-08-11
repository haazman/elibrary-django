from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split a string by the given separator"""
    if value:
        return value.split(arg)
    return []

@register.filter
def trim(value):
    """Remove whitespace from both ends of the string"""
    if value:
        return value.strip()
    return value
