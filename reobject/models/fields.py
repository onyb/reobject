from attr import ib, Factory


def Field(*args, **kwargs):
    default = kwargs.get('default')
    if callable(default):
        kwargs.pop('default')
        return ib(*args, default=Factory(default), **kwargs)
    else:
        return ib(*args, **kwargs)
