from django import template

register = template.Library()

@register.filter
def split(value, key=","):
    """Split string by given key (default: comma)."""
    if value:
        return value.split(key)
    return []
