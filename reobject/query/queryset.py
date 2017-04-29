from collections import OrderedDict
from itertools import chain
import random

from reobject.exceptions import DoesNotExist, MultipleObjectsReturned
from reobject.query import Q
from reobject.utils import cmp, flatmap


class QuerySet(list):
    def __init__(self, *args, model, **kwargs):
        super(QuerySet, self).__init__(*args, **kwargs)
        self.model = model

    @property
    def _attrs(self):
        return self[0]._attrs if self.exists() else set()

    def __or__(self, other):
        return type(self)(
            chain(self, other),
            model=self.model
        ).distinct('id')

    def count(self):
        return len(self)

    def delete(self):
        for item in self:
            item.delete()

    def distinct(self, *attrs):
        if not attrs:
            attrs = self._attrs - {'created', 'updated'}

        meta = [
            (cmp(*attrs)(obj), obj)
            for obj in self.reverse()
            ]

        return type(self)(
            OrderedDict(meta).values(),
            model=self.model
        )

    def earliest(self, field_name=None):
        if not field_name:
            field_name = 'created'

        try:
            obj = self.filter(
                **{field_name + '__isnone': False}
            ).order_by(field_name)[0]
        except IndexError:
            return None
        else:
            return obj

    def exclude(self, **kwargs):
        q = ~Q(**kwargs)

        return type(self)(
            filter(q.comparator, self),
            model=self.model
        )

    def exists(self):
        return bool(self)

    def filter(self, **kwargs):
        q = Q(**kwargs)

        return type(self)(
            filter(q.comparator, self),
            model=self.model
        )

    def first(self):
        try:
            obj = self[0]
        except IndexError:
            return None
        else:
            return obj

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

    def get_or_create(self, defaults=None, **kwargs):
        try:
            obj = self.get(**kwargs)
        except DoesNotExist:
            params = {k: v for k, v in kwargs.items() if '__' not in k}

            if defaults:
                params.update(defaults)

            obj = self.model(**params)
            return obj, True
        else:
            return obj, False

    def last(self):
        try:
            obj = self[-1]
        except IndexError:
            return None
        else:
            return obj

    def latest(self, field_name=None):
        if not field_name:
            field_name = 'created'

        try:
            obj = self.filter(
                **{field_name + '__isnone': False}
            ).order_by(field_name)[-1]
        except IndexError:
            return None
        else:
            return obj

    def map(self, callable):
        return map(callable, self)

    def none(self):
        return EmptyQuerySet(model=self.model)

    def order_by(self, *attrs):
        if not attrs:
            raise AttributeError

        return type(self)(
            sorted(self, key=cmp(*attrs)),
            model=self.model
        )

    def random(self):
        try:
            obj = random.choice(self)
        except IndexError:
            return None
        else:
            return obj

    def reverse(self):
        return type(self)(
            reversed(self),
            model=self.model
        )

    def values(self, *attrs):
        if not attrs:
            attrs = self._attrs

        return type(self)(
            (
                dict(zip(attrs, obj))
                for obj in map(cmp(*attrs), self)
            ),
            model=self.model
        )

    def values_list(self, *attrs, flat=False):
        # TODO: Allow order_by on values_list

        if not attrs:
            attrs = self._attrs

        if len(attrs) > 1 and flat:
            raise TypeError(
                '/flat/ is not valid when values_list is called with more than '
                'one field.'
            )

        return type(self)(
            (flatmap if flat else map)(cmp(*attrs), self),
            model=self.model
        )


class EmptyQuerySet(QuerySet):
    def __init__(self, model, *args, **kwargs):
        super(QuerySet, self).__init__(*args, **kwargs)
        self.model = model
