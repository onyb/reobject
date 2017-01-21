from reobject.query import QuerySet

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
        self._memory = set()
        self.model = model

    def __contains__(self, item):
        return bool(self.get(name=item))

    def filter(self, **kwargs):
        # Structure is inspired from Django ORM

        return QuerySet(filter(
            lambda x: all([getattr(x, k) == v for k, v in kwargs.items()]),
            self._memory
        ))

    def get(self, **kwargs):
        result_set = self.filter(**kwargs)

        if len(result_set) == 0:
            return None
        elif len(result_set) == 1:
            return result_set[0]
        else:
            raise Exception('MultipleObjectsReturned')

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        self._memory.add(obj)
        return obj

    def all(self):
        return QuerySet(self._memory)

    def clear(self):
        self._memory.clear()

    def _delete(self, obj):
        self._memory.remove(obj)
