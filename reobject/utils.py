from itertools import chain
from operator import itemgetter


def flatmap(func, iterable):
    return chain(*map(func, iterable))


def cmp(*attrs):
    def g(obj):
        if isinstance(obj, dict):
            return itemgetter(*attrs)(obj)
        else:
            return attrgetter(*attrs)(obj)

    return g


def attrgetter(*items):
    if any(not isinstance(item, str) for item in items):
        raise TypeError('attribute name must be a string')
    if len(items) == 1:
        attr = items[0]

        def g(obj):
            return tuple(
                [resolve_attr(obj, attr)]
            )
    else:
        def g(obj):
            return tuple(
                resolve_attr(obj, attr) for attr in items
            )
    return g


def resolve_attr(obj, attr):
    reverse = attr.startswith('-')
    attr = attr.lstrip('-')

    for name in attr.split("__"):  # Django-style attribute access
        obj = getattr(obj, name)

    return obj if not reverse else -obj
