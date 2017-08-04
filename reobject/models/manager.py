from datetime import datetime

from reobject.query import QuerySet, EmptyQuerySet


class ManagerDescriptor(object):
    """
    Descriptor class to deny access of manager methods via model instances.
    """

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
    """
    Manager class holding the centralized object store, and providing proxies
    to various QuerySet methods.
    """

    def __init__(self, model):
        self._object_store = list()
        self.model = model

    def __contains__(self, item):
        return bool(self.get(name=item))

    def _add(self, instance: object) -> object:
        instance.created = instance.updated = datetime.utcnow()
        self._object_store.append(instance)
        return instance

    def _clear(self):
        self._object_store.clear()

    def _delete(self, obj):
        self._object_store.remove(obj)

    def all(self) -> QuerySet:
        """
        Returns a QuerySet of all model instances.
        """
        return QuerySet(
            self._object_store,
            model=self.model
        )

    def count(self) -> int:
        """
        Returns an integer representing the total number of model instances.

        Proxy to the QuerySet.count() method.
        """
        return self.all().count()

    def earliest(self, field_name: str = 'created') -> object:
        """
        Returns the earliest object, by date, using the field_name provided as
        the date field.

        Proxy to the QuerySet.earliest method.

        :param field_name: Name of attribute containing datetime object
        :return: Model instance if exists, None otherwise.
        """

        return self.all().earliest(field_name)

    def exclude(self, **kwargs):
        return self.all().exclude(**kwargs)

    def filter(self, **kwargs):
        return self.all().filter(**kwargs)

    def first(self) -> object:
        """
        Returns the first model instance created.
        """
        return self.all().earliest()

    def get(self, **kwargs):
        return self.all().get(**kwargs)

    def get_or_create(self, defaults=None, **kwargs):
        return self.all().get_or_create(defaults, **kwargs)

    def last(self) -> object:
        """
        Returns the last model instance created.
        """
        return self.all().latest()

    def latest(self, field_name: str = 'created') -> object:
        """
        Returns the latest object, by date, using the field_name provided as
        the date field.

        Proxy to the QuerySet.latest method.

        :param field_name: Name of attribute containing datetime object
        :return: Model instance if exists, None otherwise.
        """
        return self.all().latest(field_name)

    def none(self) -> EmptyQuerySet:
        """
        Returns an EmptyQuerySet.

        Useful in reduce operations on QuerySets.
        """
        return EmptyQuerySet(model=self.model)

    def random(self) -> object:
        """
        Returns a random model instance.
        """
        return self.all().random()
