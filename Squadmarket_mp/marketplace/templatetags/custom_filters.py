from django import template

register = template.Library()

@register.filter
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    return None

@register.filter
def get_item(dictionary, key):
    """Gets an item from a dictionary"""
    return dictionary.get(key)

@register.filter
def replace_underscore(value):
    """Replaces underscores with spaces"""
    return value.replace('_', ' ')