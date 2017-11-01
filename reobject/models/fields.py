import attr


def Field(*args, default=attr.NOTHING, **kwargs):
    if callable(default):
        default = attr.Factory(default)

    return attr.ib(*args, default=default, **kwargs)


def ForeignKey(cls, *args, **kwargs):
    metadata = {
        'related': {
            'target': cls,
            'type': 'ForeignKey',
        }
    }

    return attr.ib(*args, metadata=metadata, **kwargs)
