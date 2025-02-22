from django import template

register = template.Library()

@register.filter
def batch(iterable, batch_size):
    """Yields batches of given size from iterable."""
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]
