import attr


def Field(*args, default=attr.NOTHING, **kwargs):
    if callable(default):
        default = attr.Factory(default)

    return attr.ib(*args, default=default, **kwargs)


def ManyToManyField(cls, *args, **kwargs):
    metadata = {
        'related': {
            'target': cls,
            'type': 'ManyToMany',
        }
    }

    return attr.ib(*args, **kwargs, metadata=metadata)
