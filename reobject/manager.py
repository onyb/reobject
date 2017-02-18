from datetime import datetime

from reobject.exceptions import DoesNotExist, MultipleObjectsReturned
from reobject.query import Q, QuerySet, EmptyQuerySet


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
        return QuerySet(self._object_store)

    def count(self):
        return len(self._object_store)

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        obj.created = obj.updated = datetime.utcnow()

        self._object_store.add(obj)
        return obj

    def exclude(self, **kwargs):
        q = ~Q(**kwargs)

        return QuerySet(filter(
            q.comparator,
            self._object_store
        ))

    def filter(self, **kwargs):
        q = Q(**kwargs)

        return QuerySet(filter(
            q.comparator,
            self._object_store
        ))

    def get(self, **kwargs):
        result_set = self.filter(**kwargs)

        if len(result_set) == 0:
            raise DoesNotExist(
                '{model} object matching query does not exist.'.format(
                    model=self.model.__name__
                )
            )

        elif len(result_set) == 1:
            return result_set[0]
        else:
            raise MultipleObjectsReturned(
                'get() returned more than one {model} object '
                '-- it returned {num}!'.format(
                    model=self.model.__name__, num=len(result_set)
                )
            )

    def none(self):
        return EmptyQuerySet()

    def _clear(self):
        self._object_store.clear()

    def _delete(self, obj):
        self._object_store.remove(obj)
