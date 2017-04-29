from datetime import datetime

from reobject.manager import ManagerDescriptor


class ModelBase(type):
    """
    Metaclass for all models
    """

    def __new__(cls, name, bases, attrs):
        super_new = super(ModelBase, cls).__new__

        parents = [base for base in bases if isinstance(base, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)
        else:
            attrs['objects'] = ManagerDescriptor()
            return super_new(cls, name, bases, attrs)


class Model(object, metaclass=ModelBase):
    def __new__(cls, *args, **kwargs):
        instance = super(Model, cls).__new__(cls)
        instance.created = instance.updated = datetime.utcnow()
        cls.objects._object_store.add(instance)
        return instance

    @classmethod
    def _get_cls(cls):
        return cls

    @property
    def id(self):
        return id(self)

    @property
    def pk(self):
        return self.id

    def delete(self):
        type(self).objects._delete(self)

    @property
    def _attrs(self):
        return set(self.__dict__.keys()) | {'id'}

    def __repr__(self):
        return '<{model}: {id}>'.format(
            model=self.__class__.__name__, id=self.id
        )
