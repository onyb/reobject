from itertools import chain


def flatmap(func, iterable):
    return chain(*map(func, iterable))


def cmp(*items):
    if any(not isinstance(item, str) for item in items):
        raise TypeError('attribute name must be a string')

    def g(obj):
        return tuple(
            resolve_attr(obj, attr) for attr in items
        )

    return g


def resolve_attr(obj, attr):
    reverse = attr.startswith('-')
    attr = attr.lstrip('-')

    for name in attr.split("__"):  # Django-style attribute access
        if isinstance(obj, dict):
            obj = obj.get(name)
        else:
            obj = getattr(obj, name)

    return obj if not reverse else -obj
