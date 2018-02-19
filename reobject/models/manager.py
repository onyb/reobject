from datetime import datetime

from reobject.models.store import ModelStoreMapping
from reobject.query import QuerySet, EmptyQuerySet


class ManagerDescriptor(object):
    """
    Descriptor class to deny access of Manager methods via model instances.
    """
    def __init__(self):
        self.manager = None

    def __get__(self, instance, owner) -> 'Manager':
        if instance is not None:
            raise AttributeError(
                "Manager isn't accessible via %s instances" % owner.__name__
            )
        else:
            if not self.manager:
                self.manager = Manager(model=owner)

            return self.manager


class RelatedManagerDescriptor(object):
    """
    Descriptor class to deny access to RelatedManager methods via model class.
    """
    def __init__(self, model):
        self.model = model

    def __get__(self, instance, owner)-> 'Manager':
        if instance is None:
            raise AttributeError(
                "RelatedManager isn't accessible via %s class" % owner.__name__
            )
        else:
            # RelatedManagerDescriptor is acting like a factory to dynamically
            # create a new RelatedManager class on every owner access via
            # the model instance.

            # [TODO] - Try to cache this manager object per unique model
            # instance.

            class RelatedManager(Manager):
                def get_queryset(related_manager_self):
                    cls_name = type(instance).__name__.lower()

                    return super(
                        RelatedManager, related_manager_self
                    ).get_queryset().filter(
                        **{'{}__pk'.format(cls_name): instance.pk}
                    )

            return RelatedManager(model=self.model)


class Manager(object):
    """
    Manager class holding the centralized object store, and providing proxies
    to various QuerySet methods.
    """

    def __init__(self, model):
        self.model = model

    @property
    def store(self):
        return ModelStoreMapping.get(self.model.__name__)

    def get_queryset(self) -> QuerySet:
        return QuerySet(
            self.store,
            model=self.model
        )

    def add(self, instance: 'Model') -> 'Model':
        if not isinstance(instance, self.model):
            raise TypeError(
                '{model} instance expected, got {obj}'.format(
                    model=self.model.__name__,
                    obj=instance
                )
            )

        instance.created = instance.updated = datetime.utcnow()
        self.store.append(instance)
        return instance

    def _delete(self, obj):
        self.store.remove(obj)

    def all(self) -> QuerySet:
        """
        Returns a QuerySet of all model instances.
        """
        return self.get_queryset()

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

    def exclude(self, *args, **kwargs):
        return self.all().exclude(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self.all().filter(*args, **kwargs)

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

    def random(self) -> 'Model':
        """
        Returns a random model instance.
        """
        return self.all().random()

    def map(self, func) -> object:
        """
        Returns a random model instance.
        """
        return self.all().map(func)

    def __repr__(self):
        return '<{manager}: {model}>'.format(
            manager=type(self).__name__, model=self.model.__name__
        )
