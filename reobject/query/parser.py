from functools import reduce
from itertools import starmap
from operator import and_ as bitwise_and

from reobject.utils import cmp


class Q(object):
    verbs = (
        'contains', 'endswith', 'gt', 'gte', 'in', 'isnull', 'lt', 'lte',
        'startswith'
    )

    def __new__(cls, *args, **kwargs):
        base_Q_obj = super(Q, cls).__new__(cls)

        if len(kwargs) in [0, 1]:
            return base_Q_obj
        else:
            raise Exception('Multiple kwargs disallowed')

    def __init__(self, **kwargs):
        attr, self.value = list(kwargs.items())[0]

        self._comparator_func = None

        if attr.rsplit('__', 1)[-1] in self.verbs:
            self.attr, self.verb = attr.rsplit('__', 1)
        else:
            self.attr = attr
            self.verb = None

    def __and__(self, other):
        base_Q_obj = Q.__new__(type(self))
        base_Q_obj.comparator = lambda obj: self.comparator(obj) and \
                                            other.comparator(obj)
        return base_Q_obj

    def __or__(self, other):
        base_Q_obj = Q.__new__(type(self))
        base_Q_obj.comparator = lambda obj: self.comparator(obj) or \
                                            other.comparator(obj)
        return base_Q_obj

    def __invert__(self):
        base_Q_obj = Q.__new__(type(self))
        base_Q_obj.comparator = lambda obj: not self.comparator(obj)
        return base_Q_obj

    @property
    def comparator(self):
        if self._comparator_func:
            return self._comparator_func

        def g(obj):
            (value,) = cmp(self.attr)(obj)

            if self.verb:
                return self.apply_verb(value)
            else:
                return value == self.value

        self.comparator = g
        return g

    @comparator.setter
    def comparator(self, g):
        self._comparator_func = g

    def apply_verb(self, value):
        return {
            'contains': self.value in value,
            'endswith': value.endswith(self.value),
            'gt': value > self.value,
            'gte': value >= self.value,
            'in': value in self.value,
            'isnull': not value,
            'lt': value < self.value,
            'lte': value <= self.value,
            'startswith': value.startswith(self.value)
        }[self.verb]
