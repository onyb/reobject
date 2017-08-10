from attr import attributes

from reobject.models.manager import ManagerDescriptor


class ModelBase(type):
    """
    Metaclass for all models, used to attach the objects class attribute
    to the model instance at runtime.
    """

    def __new__(cls, name, bases, attrs):
        attrs['objects'] = ManagerDescriptor()
        return attributes(
            super(ModelBase, cls).__new__(cls, name, bases, attrs)
        )


class Model(object, metaclass=ModelBase):
    def __attrs_post_init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        instance = super(Model, cls).__new__(cls)
        return cls.objects._add(instance)

    @property
    def id(self) -> int:
        """
        Returns a unique integer identifier for the object.
        """
        return id(self)

    @property
    def pk(self) -> int:
        """
        Returns a unique integer identifier for the object.

        Alias of the id property.
        """
        return self.id

    def delete(self) -> None:
        type(self).objects._delete(self)

    @property
    def _attrs(self):
        return set(self.__dict__.keys()) | {'id'}
