import attr

from reobject.models.manager import ManagerDescriptor, RelatedManagerDescriptor
from reobject.models.store import Store, ModelStoreMapping


class ModelBase(type):
    """
    Metaclass for all models, used to attach the objects class attribute
    to the model instance at runtime.
    """

    def __new__(cls, name, bases, attrs):
        attrs['objects'] = ManagerDescriptor()

        mod = attr.s(
            super(ModelBase, cls).__new__(cls, name, bases, attrs)
        )

        if 'Model' in [base.__name__ for base in bases]:
            ModelStoreMapping[mod.__name__] = Store()

        return mod


class Model(object, metaclass=ModelBase):
    def __attrs_post_init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        instance = super(Model, cls).__new__(cls)

        for field in attr.fields(cls):
            if field.metadata.get('related'):
                target = field.metadata['related']['target']

                setattr(
                    target,
                    cls.__name__.lower() + '_set',
                    RelatedManagerDescriptor(model=cls)
                )

        return cls.objects.add(instance)

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
