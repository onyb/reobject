from datetime import datetime
import random

from reobject.query import QuerySet, EmptyQuerySet


class ManagerDescriptor(object):
    def __init__(self):
        self.manager = None

    def __get__(self, instance, owner):
        if instance is not None:
            raise AttributeError(
                "Manager isn't accessible via %s instances" % owner.__name__
            )
        else:
            if not self.manager:
                self.manager = Manager(model=owner)

            return self.manager


class Manager(object):
    def __init__(self, model):
        self._object_store = set()
        self.model = model

    def __contains__(self, item):
        return bool(self.get(name=item))

    def all(self):
        return QuerySet(
            self._object_store,
            model=self.model
        )

    def count(self):
        return self.all().count()

    def earliest(self, field_name=None):
        return self.all().earliest(field_name)

    def exclude(self, **kwargs):
        return self.all().exclude(**kwargs)

    def filter(self, **kwargs):
        return self.all().filter(**kwargs)

    def first(self):
        return self.all().earliest()

    def get(self, **kwargs):
        return self.all().get(**kwargs)

    def get_or_create(self, defaults=None, **kwargs):
        return self.all().get_or_create(defaults, **kwargs)

    def last(self):
        return self.all().latest()

    def latest(self, field_name=None):
        return self.all().latest(field_name)

    def none(self):
        return EmptyQuerySet(model=self.model)

    def random(self):
        return self.all().random()

    def _clear(self):
        self._object_store.clear()

    def _delete(self, obj):
        self._object_store.remove(obj)
