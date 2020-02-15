from django import template


register = template.Library()

@register.filter(name='iter')
def make_iterator(it):
    """
    Create iterator from iterable.
    """
    return iter(it)

@register.filter(name='yield')
def yielder(it):
    """
    Yield from generator.

    Adapted from:
    https://stackoverflow.com/a/40701031
    """
    try:
        return next(it)
    except StopIteration:
        return None
